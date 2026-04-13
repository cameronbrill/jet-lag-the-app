from __future__ import annotations

from collections.abc import AsyncIterator

from httpx import ASGITransport, AsyncClient
import pytest

from jetlag.config import Settings
from jetlag.main import create_app


@pytest.fixture()
def settings() -> Settings:
    return Settings(jwt_secret="test-secret-" + ("x" * 24), database_url="sqlite+aiosqlite:///:memory:", debug=True)


@pytest.fixture()
async def client(settings: Settings) -> AsyncIterator[AsyncClient]:
    app = create_app(settings)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
