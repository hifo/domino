from __future__ import annotations

from typing import Any

import requests

BASE_URL = "https://antioch-production.up.railway.app"


def fetch_api_list(url: str | None = None, params: dict[str, Any] | None = None, spell_level: int = 1, timeout: int = 10) -> list[Any]:
    """Fetch JSON from an API and return the first list payload found."""
    request_url = url or f"{BASE_URL}/antioch/api/v1.0/spells_by_circle/{spell_level}"
    if request_url.startswith("/"):
        request_url = f"{BASE_URL}{request_url}"

    response = requests.get(request_url, params=params, timeout=timeout)
    response.raise_for_status()

    payload = response.json()

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in ("spells", "items", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return value

        for value in payload.values():
            if isinstance(value, list):
                return value

    raise ValueError(f"Expected a list response from {url}, got {type(payload).__name__}")
