from __future__ import annotations

from httpx import AsyncClient
import pytest


async def _auth_headers(client: AsyncClient, email: str, password: str) -> dict[str, str]:
    s = await client.post("/api/auth/signup", json={"email": email, "password": password})
    assert s.status_code == 201, s.text
    t = await client.post("/api/auth/login", json={"email": email, "password": password})
    assert t.status_code == 200, t.text
    token = t.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio()
async def test_shortlink_register_requires_auth(client: AsyncClient) -> None:
    r = await client.post("/api/shortlinks", json={"slug": "n1", "target_url": "myapp://curse/1"})
    assert r.status_code == 401


@pytest.mark.asyncio()
async def test_shortlink_roundtrip(client: AsyncClient) -> None:
    headers = await _auth_headers(client, "roundtrip@test.com", "password123")
    r = await client.post("/api/shortlinks", json={"slug": "c1", "target_url": "myapp://curse/1"}, headers=headers)
    assert r.status_code == 200
    g = await client.get("/api/shortlinks/c1")
    assert g.json()["url"] == "myapp://curse/1"


@pytest.mark.asyncio()
async def test_shortlink_same_user_updates_target(client: AsyncClient) -> None:
    headers = await _auth_headers(client, "upsert-owner@test.com", "password123")
    first = await client.post(
        "/api/shortlinks",
        json={"slug": "s1", "target_url": "https://old.example.com"},
        headers=headers,
    )
    assert first.status_code == 200
    second = await client.post(
        "/api/shortlinks",
        json={"slug": "s1", "target_url": "https://new.example.com"},
        headers=headers,
    )
    assert second.status_code == 200
    resolve = await client.get("/api/shortlinks/s1")
    assert resolve.json()["url"] == "https://new.example.com"


@pytest.mark.asyncio()
async def test_shortlink_other_user_cannot_steal_slug(client: AsyncClient) -> None:
    h1 = await _auth_headers(client, "owner-slug@test.com", "password123")
    h2 = await _auth_headers(client, "other-slug@test.com", "password123")
    first = await client.post(
        "/api/shortlinks",
        json={"slug": "shared", "target_url": "https://first.example.com"},
        headers=h1,
    )
    assert first.status_code == 200
    hijack = await client.post(
        "/api/shortlinks",
        json={"slug": "shared", "target_url": "https://evil.example.com"},
        headers=h2,
    )
    assert hijack.status_code == 409
    assert hijack.json().get("detail") == "Slug already exists"
    resolve = await client.get("/api/shortlinks/shared")
    assert resolve.json()["url"] == "https://first.example.com"


@pytest.mark.asyncio()
async def test_shortlink_html_escapes_url(client: AsyncClient) -> None:
    headers = await _auth_headers(client, "html-esc@test.com", "password123")
    reg = await client.post(
        "/api/shortlinks",
        json={"slug": "xss", "target_url": "https://example.com/?x=1&y=2&z=3"},
        headers=headers,
    )
    assert reg.status_code == 200, reg.text
    resp = await client.get("/api/shortlinks/xss/html")
    assert resp.status_code == 200
    assert "&amp;" in resp.text
    assert "javascript:" not in resp.text


@pytest.mark.asyncio()
async def test_shortlink_rejects_javascript_scheme(client: AsyncClient) -> None:
    headers = await _auth_headers(client, "js-scheme@test.com", "password123")
    resp = await client.post(
        "/api/shortlinks",
        json={"slug": "js1", "target_url": "javascript:alert(1)"},
        headers=headers,
    )
    assert resp.status_code == 422


@pytest.mark.asyncio()
async def test_shortlink_rejects_invalid_slug_characters(client: AsyncClient) -> None:
    headers = await _auth_headers(client, "bad-slug@test.com", "password123")
    resp = await client.post(
        "/api/shortlinks",
        json={"slug": "bad/slug", "target_url": "https://example.com/"},
        headers=headers,
    )
    assert resp.status_code == 422


@pytest.mark.asyncio()
async def test_shortlink_rejects_slug_over_max_length(client: AsyncClient) -> None:
    headers = await _auth_headers(client, "long-slug@test.com", "password123")
    resp = await client.post(
        "/api/shortlinks",
        json={"slug": "a" * 129, "target_url": "https://example.com/"},
        headers=headers,
    )
    assert resp.status_code == 422
