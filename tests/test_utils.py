from types import SimpleNamespace

import pytest

from utils.utils import fetch_api_list


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
        if url == "https://example.com/items":
            return DummyResponse({"items": [{"name": "shield"}, {"name": "heal"}]})
        if url == "https://example.com/results":
            return DummyResponse({"results": ["a", "b"]})
        if url == "https://example.com/spells":
            return DummyResponse({"spells": ["cure disease", "light"]})
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr("requests.get", fake_get)

    assert fetch_api_list("https://example.com/items") == [{"name": "shield"}, {"name": "heal"}]
    assert fetch_api_list("https://example.com/results") == ["a", "b"]
    assert fetch_api_list("https://example.com/spells") == ["cure disease", "light"]


def test_fetch_api_list_raises_for_non_list_payload(monkeypatch):
    def fake_get(url, params=None, timeout=10):
        return DummyResponse({"status": "ok"})

    monkeypatch.setattr("requests.get", fake_get)

    with pytest.raises(ValueError):
        fetch_api_list("https://example.com/unsupported")
