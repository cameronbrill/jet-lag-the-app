from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, Request, status
import jwt
from sqlalchemy.ext.asyncio import AsyncConnection

from jetlag.config import Settings, get_settings
from jetlag.core.connection_manager import ConnectionManager
from jetlag.core.game_engine import GameRuntime


@dataclass
class MemoryStore:
    """In-memory store retained for game engine runtime state (not persisted yet)."""

    games: dict[UUID, GameRuntime] = field(default_factory=dict)


def get_store(request: Request) -> MemoryStore:
    return request.app.state.store


async def get_connection(request: Request) -> AsyncIterator[AsyncConnection]:
    engine = request.app.state.engine
    async with engine.connect() as conn:
        yield conn
        await conn.commit()


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
DbConn = Annotated[AsyncConnection, Depends(get_connection)]


async def get_bearer_subject(
    settings: SettingsDep,
    authorization: Annotated[str | None, Header()] = None,
) -> str:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials") from None
    sub = payload.get("sub")
    if not isinstance(sub, str) or not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return sub


CurrentUserEmail = Annotated[str, Depends(get_bearer_subject)]
