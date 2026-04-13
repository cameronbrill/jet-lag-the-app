from __future__ import annotations

import html
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator

from jetlag.api.deps import DbConn
from jetlag.db.generated.shortlinks import AsyncQuerier as ShortlinkQuerier

router = APIRouter(prefix="/shortlinks", tags=["shortlinks"])

_ALLOWED_SHORTLINK_SCHEMES = frozenset({"https", "myapp"})


def safe_href_for_html(url: str) -> str:
    """Escape URL for use in an HTML href; drop disallowed schemes (defense at render time)."""
    parsed = urlparse(url)
    scheme = (parsed.scheme or "").lower()
    if scheme not in _ALLOWED_SHORTLINK_SCHEMES:
        return "#"
    return html.escape(url, quote=True)


class RegisterShortlinkBody(BaseModel):
    slug: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    target_url: str

    @field_validator("target_url")
    @classmethod
    def target_url_allowed_scheme(cls, value: str) -> str:
        parsed = urlparse(value)
        scheme = (parsed.scheme or "").lower()
        if scheme not in _ALLOWED_SHORTLINK_SCHEMES:
            msg = "target_url must use https or myapp scheme"
            raise ValueError(msg)
        return value


@router.post("")
async def register_shortlink(conn: DbConn, body: RegisterShortlinkBody) -> dict[str, str]:
    await ShortlinkQuerier(conn).create_shortlink(slug=body.slug, target_url=body.target_url)
    return {"slug": body.slug}


@router.get("/{slug}")
async def resolve_shortlink(conn: DbConn, slug: str) -> dict[str, str]:
    result = await ShortlinkQuerier(conn).get_shortlink(slug=slug)
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return {"url": result.target_url}


@router.get("/{slug}/html", response_class=HTMLResponse)
async def resolve_shortlink_html(conn: DbConn, slug: str) -> HTMLResponse:
    result = await ShortlinkQuerier(conn).get_shortlink(slug=slug)
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    safe_url = safe_href_for_html(result.target_url)
    document = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Open in app</title></head>
<body><p><a href="{safe_url}">Continue</a></p></body></html>"""
    return HTMLResponse(content=document)
