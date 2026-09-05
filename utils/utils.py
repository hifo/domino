from __future__ import annotations

from urllib.parse import quote
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


def fetch_spell_detail(spell_name: str, timeout: int = 10) -> dict[str, Any]:
    """Fetch the upstream spell detail payload for a specific spell name."""
    encoded_spell_name = quote(spell_name, safe="")
    request_url = f"{BASE_URL}/antioch/api/v1.0/spell/{encoded_spell_name}"

    response = requests.get(request_url, timeout=timeout)
    response.raise_for_status()

    payload = response.json()

    if isinstance(payload, dict):
        return payload

    raise ValueError(f"Expected a dictionary response from {spell_name}, got {type(payload).__name__}")
