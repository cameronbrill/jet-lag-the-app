from __future__ import annotations

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio()
async def test_create_list_curse(client: AsyncClient) -> None:
    r = await client.post(
        "/api/curses",
        json={"name": "No trains", "duration_rounds": 2, "blocks_transit": True},
    )
    assert r.status_code == 201
    lst = await client.get("/api/curses")
    assert lst.status_code == 200
    assert len(lst.json()) == 1
