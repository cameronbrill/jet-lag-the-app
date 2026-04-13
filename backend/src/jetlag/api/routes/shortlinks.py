from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from jetlag.api.deps import StoreDep

router = APIRouter(prefix="/shortlinks", tags=["shortlinks"])


class RegisterShortlinkBody(BaseModel):
    slug: str
    target_url: str


@router.post("")
async def register_shortlink(store: StoreDep, body: RegisterShortlinkBody) -> dict[str, str]:
    store.shortlinks[body.slug] = body.target_url
    return {"slug": body.slug}


@router.get("/{slug}")
async def resolve_shortlink(store: StoreDep, slug: str) -> dict[str, str]:
    url = store.shortlinks.get(slug)
    if url is None:
        raise HTTPException(status_code=404, detail="Not found")
    return {"url": url}


@router.get("/{slug}/html", response_class=HTMLResponse)
async def resolve_shortlink_html(store: StoreDep, slug: str) -> HTMLResponse:
    url = store.shortlinks.get(slug)
    if url is None:
        raise HTTPException(status_code=404, detail="Not found")
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Open in app</title></head>
<body><p><a href="{url}">Continue</a></p></body></html>"""
    return HTMLResponse(content=html)
