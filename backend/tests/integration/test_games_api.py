from __future__ import annotations

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio()
async def test_create_and_fetch_game(client: AsyncClient) -> None:
    r = await client.post("/api/games", json={"name": "Lobby"})
    assert r.status_code == 201
    game_id = r.json()["id"]
    g = await client.get(f"/api/games/{game_id}")
    assert g.status_code == 200
    assert g.json()["name"] == "Lobby"


@pytest.mark.asyncio()
async def test_start_requires_two_players(client: AsyncClient) -> None:
    r = await client.post("/api/games", json={"name": "x"})
    game_id = r.json()["id"]
    await client.post(f"/api/games/{game_id}/players", json={"display_name": "solo"})
    s = await client.post(f"/api/games/{game_id}/start")
    assert s.status_code == 400
