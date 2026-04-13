from __future__ import annotations

from collections import defaultdict
from typing import Any
from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self._game_connections: dict[UUID, list[WebSocket]] = defaultdict(list)

    async def connect(self, game_id: UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self.register(game_id, websocket)

    def register(self, game_id: UUID, websocket: WebSocket) -> None:
        self._game_connections[game_id].append(websocket)

    def disconnect(self, game_id: UUID, websocket: WebSocket) -> None:
        conns = self._game_connections.get(game_id, [])
        if websocket in conns:
            conns.remove(websocket)

    def connection_count(self, game_id: UUID) -> int:
        return len(self._game_connections.get(game_id, []))

    async def broadcast_json(self, game_id: UUID, message: dict[str, Any]) -> None:
        dead: list[WebSocket] = []
        for ws in list(self._game_connections.get(game_id, [])):
            try:
                await ws.send_json(message)
            except OSError:
                dead.append(ws)
        for ws in dead:
            self.disconnect(game_id, ws)
