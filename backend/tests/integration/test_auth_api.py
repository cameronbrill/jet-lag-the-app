from __future__ import annotations

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio()
async def test_signup_login(client: AsyncClient) -> None:
    body = {"email": "a@example.com", "password": "secret"}
    s = await client.post("/api/auth/signup", json=body)
    assert s.status_code == 201
    t = await client.post("/api/auth/login", json=body)
    assert t.status_code == 200
    assert "access_token" in t.json()
