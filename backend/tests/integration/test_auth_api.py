from __future__ import annotations

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio()
async def test_login_empty_password_returns_422(client: AsyncClient) -> None:
    resp = await client.post("/api/auth/login", json={"email": "any@example.com", "password": ""})
    assert resp.status_code == 422


@pytest.mark.asyncio()
async def test_login_short_wrong_password_returns_401_not_422(client: AsyncClient) -> None:
    await client.post("/api/auth/signup", json={"email": "short-pwd-login@test.com", "password": "password123"})
    resp = await client.post(
        "/api/auth/login",
        json={"email": "short-pwd-login@test.com", "password": "bad"},
    )
    assert resp.status_code == 401
    assert resp.json().get("detail") == "Invalid credentials"


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
async def test_signup_rejects_password_over_72_utf8_bytes(client: AsyncClient) -> None:
    # 36 times U+1F600: 36 code points but 144 UTF-8 bytes (over bcrypt limit)
    password = "\U0001f600" * 36
    assert len(password) == 36
    assert len(password.encode("utf-8")) == 144
    resp = await client.post("/api/auth/signup", json={"email": "emoji-bytes@test.com", "password": password})
    assert resp.status_code != 500
    assert resp.status_code == 422


@pytest.mark.asyncio()
async def test_duplicate_signup_returns_409(client: AsyncClient) -> None:
    body = {"email": "dup@test.com", "password": "password123"}
    first = await client.post("/api/auth/signup", json=body)
    assert first.status_code == 201
    second = await client.post("/api/auth/signup", json=body)
    assert second.status_code == 409
