from __future__ import annotations

from collections.abc import AsyncIterator
import os
from pathlib import Path

from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from jetlag.config import Settings
from jetlag.main import create_app

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "db" / "schema.sql"
TEST_DB_URL = os.environ.get(
    "JETLAG_TEST_DATABASE_URL",
    "postgresql+asyncpg://jetlag:jetlag-dev@localhost:5432/jetlag_test",
)


@pytest.fixture()
def settings() -> Settings:
    return Settings(
        jwt_secret="test-secret-" + ("x" * 24),
        database_url=TEST_DB_URL,
        debug=True,
    )


def _split_sql(sql: str) -> list[str]:
    """Split SQL by semicolons, preserving multi-line statements."""
    return [s.strip() for s in sql.split(";") if s.strip()]


@pytest.fixture()
async def _setup_test_db(settings: Settings) -> AsyncIterator[None]:
    """Create tables from schema.sql before each test, drop after."""
    engine = create_async_engine(settings.database_url, echo=False)
    schema_sql = SCHEMA_PATH.read_text()

    async with engine.begin() as conn:
        for type_name in ("game_phase", "game_size", "round_phase", "curse_block_kind"):
            await conn.execute(text(f"DROP TYPE IF EXISTS {type_name} CASCADE"))
        for table in ("active_curses", "rounds", "players", "games", "curse_definitions", "shortlinks", "users"):
            await conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
        for stmt in _split_sql(schema_sql):
            if stmt.strip():
                await conn.execute(text(stmt))

    yield

    async with engine.begin() as conn:
        for table in ("active_curses", "rounds", "players", "games", "curse_definitions", "shortlinks", "users"):
            await conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
        for type_name in ("game_phase", "game_size", "round_phase", "curse_block_kind"):
            await conn.execute(text(f"DROP TYPE IF EXISTS {type_name} CASCADE"))
    await engine.dispose()


@pytest.fixture()
async def client(settings: Settings, _setup_test_db: None) -> AsyncIterator[AsyncClient]:
    app = create_app(settings)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
