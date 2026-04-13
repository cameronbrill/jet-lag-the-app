from __future__ import annotations

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio()
async def test_signup_login(client: AsyncClient) -> None:
    body = {"email": "a@example.com", "password": "secret123"}
    s = await client.post("/api/auth/signup", json=body)
    assert s.status_code == 201
    t = await client.post("/api/auth/login", json=body)
    assert t.status_code == 200
    assert "access_token" in t.json()


@pytest.mark.asyncio()
async def test_signup_rejects_short_password(client: AsyncClient) -> None:
    resp = await client.post("/api/auth/signup", json={"email": "short@test.com", "password": "abc"})
    assert resp.status_code == 422


@pytest.mark.asyncio()
async def test_signup_rejects_long_password(client: AsyncClient) -> None:
    resp = await client.post("/api/auth/signup", json={"email": "long@test.com", "password": "a" * 73})
    assert resp.status_code == 422


@pytest.mark.asyncio()
async def test_duplicate_signup_returns_409(client: AsyncClient) -> None:
    body = {"email": "dup@test.com", "password": "password123"}
    first = await client.post("/api/auth/signup", json=body)
    assert first.status_code == 201
    second = await client.post("/api/auth/signup", json=body)
    assert second.status_code == 409
