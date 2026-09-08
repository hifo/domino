import threading
from pathlib import Path

import pytest
from werkzeug.serving import make_server

from app import create_app
from utils.utils import fetch_api_list, fetch_spell_detail

pytest.importorskip("playwright")
from playwright.sync_api import sync_playwright


class DummyResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


def test_fetch_api_list_accepts_plain_list(monkeypatch):
    def fake_get(url, params=None, timeout=10):
        assert url == "https://example.com/items"
        assert params == {"page": 1}
        assert timeout == 5
        return DummyResponse([{"name": "fireball"}, {"name": "magic missile"}])

    monkeypatch.setattr("requests.get", fake_get)

    assert fetch_api_list("https://example.com/items", {"page": 1}, timeout=5) == [
        {"name": "fireball"},
        {"name": "magic missile"},
    ]


def test_fetch_api_list_extracts_list_from_dict(monkeypatch):
    def fake_get(url, params=None, timeout=10):
        assert url in {
            "https://example.com/items",
            "https://example.com/results",
            "https://example.com/spells",
        }
        if url == "https://example.com/items":
            assert params is None
            assert timeout == 10
            return DummyResponse({"items": [{"name": "shield"}, {"name": "heal"}]})
        if url == "https://example.com/results":
            assert params is None
            assert timeout == 10
            return DummyResponse({"results": ["a", "b"]})
        if url == "https://example.com/spells":
            assert params is None
            assert timeout == 10
            return DummyResponse({"spells": ["cure disease", "light"]})
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr("requests.get", fake_get)

    assert fetch_api_list("https://example.com/items") == [{"name": "shield"}, {"name": "heal"}]
    assert fetch_api_list("https://example.com/results") == ["a", "b"]
    assert fetch_api_list("https://example.com/spells") == ["cure disease", "light"]


def test_fetch_api_list_raises_for_non_list_payload(monkeypatch):
    def fake_get(url, params=None, timeout=10):
        assert url == "https://example.com/unsupported"
        assert params is None
        assert timeout == 10
        return DummyResponse({"status": "ok"})

    monkeypatch.setattr("requests.get", fake_get)

    with pytest.raises(ValueError):
        fetch_api_list("https://example.com/unsupported")


def test_fetch_spell_detail_uses_encoded_spell_name(monkeypatch):
    def fake_get(url, params=None, timeout=10):
        assert url == "https://antioch-production.up.railway.app/antioch/api/v1.0/spell/Cure%20Disease"
        assert params is None
        assert timeout == 10
        return DummyResponse({"spells": {"name": "Cure Disease", "circle": 1}})

    monkeypatch.setattr("requests.get", fake_get)

    assert fetch_spell_detail("Cure Disease") == {"spells": {"name": "Cure Disease", "circle": 1}}


def test_caveats_upload_has_unique_ids_and_spell_list_container():
    html = Path("app/templates/index.html").read_text(encoding="utf-8")

    assert 'id="caveats-upload-button"' in html
    assert 'id="caveats-upload-json-input"' in html
    assert 'id="caveats-spell-list"' in html
    assert "fetch(`/spell/${encodeURIComponent(spellName)}`)" in html


def test_app_smoke_loads_caveats_upload_controls():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Caveats" in html
    assert 'id="caveats-upload-button"' in html
    assert 'id="caveats-upload-json-input"' in html
    assert 'id="caveats-spell-list-wrapper"' in html


def test_spellbook_details_include_caveats_field():
    html = Path("app/templates/index.html").read_text(encoding="utf-8")

    assert 'id="spell-caveats-value"' in html
    assert "setDetailValue('caveats'" in html


def test_spell_detail_parser_accepts_string_caveats_value():
    html = Path("app/templates/index.html").read_text(encoding="utf-8")

    assert "typeof spell.caveats === 'string'" in html
    assert "spell.caveats" in html


def test_browser_smoke_clicks_caveats_upload_button():
    app = create_app()
    server = make_server("127.0.0.1", 5001, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://127.0.0.1:5001/", wait_until="domcontentloaded")
            page.locator('[data-tab-target="caveats-panel"]').click()
            page.evaluate(
                """
                () => {
                    const input = document.getElementById('caveats-upload-json-input');
                    window.__caveatsInputClicked = 0;
                    input.click = () => {
                        window.__caveatsInputClicked += 1;
                    };
                }
                """
            )

            page.locator('#caveats-upload-button').click()

            assert page.evaluate("() => window.__caveatsInputClicked") == 1
            browser.close()
    finally:
        server.shutdown()
        thread.join(timeout=5)
