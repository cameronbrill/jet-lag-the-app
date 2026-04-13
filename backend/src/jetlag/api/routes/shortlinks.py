from __future__ import annotations

import html

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from jetlag.api.deps import DbConn
from jetlag.db.generated.shortlinks import AsyncQuerier as ShortlinkQuerier

router = APIRouter(prefix="/shortlinks", tags=["shortlinks"])


class RegisterShortlinkBody(BaseModel):
    slug: str
    target_url: str


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
    safe_url = html.escape(result.target_url, quote=True)
    document = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Open in app</title></head>
<body><p><a href="{safe_url}">Continue</a></p></body></html>"""
    return HTMLResponse(content=document)
