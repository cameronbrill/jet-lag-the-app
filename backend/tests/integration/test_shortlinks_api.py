from __future__ import annotations

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio()
async def test_shortlink_roundtrip(client: AsyncClient) -> None:
    r = await client.post("/api/shortlinks", json={"slug": "c1", "target_url": "myapp://curse/1"})
    assert r.status_code == 200
    g = await client.get("/api/shortlinks/c1")
    assert g.json()["url"] == "myapp://curse/1"
