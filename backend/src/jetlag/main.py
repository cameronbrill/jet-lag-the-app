from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from jetlag.api.deps import MemoryStore
from jetlag.api.routes import auth, curses, games, leaderboard, shortlinks
from jetlag.api.ws import game_sync
from jetlag.config import Settings, get_settings
from jetlag.core.connection_manager import ConnectionManager
from jetlag.logging import configure_logging


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.state.settings = settings
    app.state.store = MemoryStore()
    app.state.connections = ConnectionManager()

    app.include_router(games.router, prefix="/api")
    app.include_router(curses.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")
    app.include_router(leaderboard.router, prefix="/api")
    app.include_router(shortlinks.router, prefix="/api")
    app.include_router(game_sync.router)
    return app


app = create_app()
