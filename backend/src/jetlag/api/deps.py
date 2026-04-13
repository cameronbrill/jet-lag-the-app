from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request

from jetlag.config import Settings, get_settings
from jetlag.core.connection_manager import ConnectionManager
from jetlag.core.game_engine import GameRuntime


@dataclass
class MemoryStore:
    games: dict[UUID, GameRuntime] = field(default_factory=dict)
    curses: dict[UUID, dict] = field(default_factory=dict)
    shortlinks: dict[str, str] = field(default_factory=dict)
    users: dict[str, str] = field(default_factory=dict)


def get_store(request: Request) -> MemoryStore:
    return request.app.state.store


def get_connections(request: Request) -> ConnectionManager:
    return request.app.state.connections


def resolve_settings(request: Request) -> Settings:
    s = getattr(request.app.state, "settings", None)
    if isinstance(s, Settings):
        return s
    return get_settings()


StoreDep = Annotated[MemoryStore, Depends(get_store)]
ConnDep = Annotated[ConnectionManager, Depends(get_connections)]
SettingsDep = Annotated[Settings, Depends(resolve_settings)]
