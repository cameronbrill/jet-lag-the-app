from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from jetlag.api.deps import ConnDep, StoreDep
from jetlag.core.game_engine import GameEngineError, GameRuntime
from jetlag.models.game import Game
from jetlag.models.player import Player

router = APIRouter(prefix="/games", tags=["games"])


class CreateGameBody(BaseModel):
    name: str


class AddPlayerBody(BaseModel):
    display_name: str


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_game(store: StoreDep, body: CreateGameBody) -> Game:
    game = Game(name=body.name)
    store.games[game.id] = GameRuntime(game=game)
    return game


@router.get("/{game_id}")
async def get_game(store: StoreDep, game_id: UUID) -> Game:
    rt = store.games.get(game_id)
    if rt is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return rt.game


@router.post("/{game_id}/players")
async def add_player(store: StoreDep, game_id: UUID, body: AddPlayerBody) -> Player:
    rt = store.games.get(game_id)
    if rt is None:
        raise HTTPException(status_code=404, detail="Game not found")
    player = Player(display_name=body.display_name, hide_order=len(rt.players))
    try:
        rt.add_player(player)
    except GameEngineError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return player


@router.post("/{game_id}/start")
async def start_game(store: StoreDep, game_id: UUID) -> Game:
    rt = store.games.get(game_id)
    if rt is None:
        raise HTTPException(status_code=404, detail="Game not found")
    try:
        rt.start_game()
    except GameEngineError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return rt.game


@router.get("/{game_id}/state")
async def game_state(store: StoreDep, connections: ConnDep, game_id: UUID) -> dict:
    rt = store.games.get(game_id)
    if rt is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return {
        "game": rt.game.model_dump(mode="json"),
        "players": [p.model_dump(mode="json") for p in rt.players],
        "rounds": [r.model_dump(mode="json") for r in rt.rounds],
        "connections": connections.connection_count(game_id),
    }
