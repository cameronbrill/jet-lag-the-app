from __future__ import annotations

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio()
async def test_shortlink_roundtrip(client: AsyncClient) -> None:
    r = await client.post("/api/shortlinks", json={"slug": "c1", "target_url": "myapp://curse/1"})
    assert r.status_code == 200
    g = await client.get("/api/shortlinks/c1")
    assert g.json()["url"] == "myapp://curse/1"


@pytest.mark.asyncio()
async def test_shortlink_upsert(client: AsyncClient) -> None:
    first = await client.post("/api/shortlinks", json={"slug": "s1", "target_url": "https://old.example.com"})
    assert first.status_code == 200
    second = await client.post("/api/shortlinks", json={"slug": "s1", "target_url": "https://new.example.com"})
    assert second.status_code == 200
    resolve = await client.get("/api/shortlinks/s1")
    assert resolve.json()["url"] == "https://new.example.com"


@pytest.mark.asyncio()
async def test_shortlink_html_escapes_url(client: AsyncClient) -> None:
    # Ampersands in query must be escaped in HTML attributes
    await client.post(
        "/api/shortlinks",
        json={"slug": "xss", "target_url": "https://example.com/?x=1&y=2&z=3"},
    )
    resp = await client.get("/api/shortlinks/xss/html")
    assert resp.status_code == 200
    assert "&amp;" in resp.text
    assert "javascript:" not in resp.text


@pytest.mark.asyncio()
async def test_shortlink_rejects_javascript_scheme(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/shortlinks",
        json={"slug": "js1", "target_url": "javascript:alert(1)"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio()
async def test_shortlink_rejects_invalid_slug_characters(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/shortlinks",
        json={"slug": "bad/slug", "target_url": "https://example.com/"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio()
async def test_shortlink_rejects_slug_over_max_length(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/shortlinks",
        json={"slug": "a" * 129, "target_url": "https://example.com/"},
    )
    assert resp.status_code == 422
