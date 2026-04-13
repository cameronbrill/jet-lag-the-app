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
    await client.post(
        "/api/shortlinks",
        json={"slug": "xss", "target_url": "\"><script>alert(1)</script>"},
    )
    resp = await client.get("/api/shortlinks/xss/html")
    assert resp.status_code == 200
    assert "<script>" not in resp.text
    assert "&lt;script&gt;" in resp.text or "&#x27;" in resp.text or "&quot;" in resp.text
