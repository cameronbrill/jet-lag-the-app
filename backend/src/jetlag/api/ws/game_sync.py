from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import jwt
from pydantic import BaseModel, ValidationError

from jetlag.config import Settings
from jetlag.core.game_engine import GameEngineError, GameRuntime
from jetlag.models.round import RoundPhase

router = APIRouter()


class JoinMessage(BaseModel):
    type: str = "join"
    game_id: UUID
    token: str | None = None


class ActionMessage(BaseModel):
    type: str = "action"
    action: str
    payload: dict[str, Any] | None = None


def _snapshot(rt: GameRuntime) -> dict[str, Any]:
    return {
        "type": "state",
        "game": rt.game.model_dump(mode="json"),
        "players": [p.model_dump(mode="json") for p in rt.players],
        "rounds": [r.model_dump(mode="json") for r in rt.rounds],
    }


def _verify_token(settings: Settings, token: str | None) -> None:
    if token is None:
        return
    try:
        jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as e:
        msg = "Invalid token"
        raise PermissionError(msg) from e


def _apply_action(rt: GameRuntime, action: str, payload: dict[str, Any] | None) -> None:
    payload = payload or {}
    if action == "transition":
        phase = RoundPhase(str(payload["phase"]))
        rt.transition_round_phase(phase)
    elif action == "advance_round":
        rt.advance_round_after_found()
    elif action == "pause":
        rt.pause()
    elif action == "resume":
        rt.resume()
    elif action == "tick":
        rt.tick_hider_timer(float(payload.get("delta_seconds", 0)))
    else:
        msg = "Unknown action"
        raise ValueError(msg)


@router.websocket("/ws/game")
async def game_sync(websocket: WebSocket) -> None:
    store = websocket.app.state.store
    connections = websocket.app.state.connections
    settings: Settings = websocket.app.state.settings

    await websocket.accept()
    raw = await websocket.receive_json()
    try:
        join = JoinMessage.model_validate(raw)
    except ValidationError:
        await websocket.close(code=4400)
        return

    try:
        _verify_token(settings, join.token)
    except PermissionError:
        await websocket.close(code=4401)
        return

    rt = store.games.get(join.game_id)
    if rt is None:
        await websocket.close(code=4404)
        return

    connections.register(join.game_id, websocket)
    try:
        await websocket.send_json(_snapshot(rt))
        while True:
            msg = await websocket.receive_json()
            try:
                action = ActionMessage.model_validate(msg)
            except ValidationError:
                await websocket.send_json({"type": "error", "detail": "invalid message"})
                continue
            try:
                _apply_action(rt, action.action, action.payload)
            except (GameEngineError, KeyError, ValueError) as e:
                await websocket.send_json({"type": "error", "detail": str(e)})
                continue
            await connections.broadcast_json(join.game_id, _snapshot(rt))
    except WebSocketDisconnect:
        connections.disconnect(join.game_id, websocket)
