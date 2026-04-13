from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from jetlag.config import Settings


def create_db_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(settings.database_url, echo=settings.debug)


async def get_connection(engine: AsyncEngine) -> AsyncConnection:
    return engine.connect()
