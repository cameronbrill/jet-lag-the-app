from __future__ import annotations

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio()
async def test_leaderboard_empty(client: AsyncClient) -> None:
    r = await client.post("/api/games", json={"name": "g"})
    game_id = r.json()["id"]
    await client.post(f"/api/games/{game_id}/players", json={"display_name": "a"})
    await client.post(f"/api/games/{game_id}/players", json={"display_name": "b"})
    await client.post(f"/api/games/{game_id}/start")
    lb = await client.get(f"/api/leaderboard/{game_id}")
    assert lb.status_code == 200
    rows = lb.json()
    assert len(rows) == 2
