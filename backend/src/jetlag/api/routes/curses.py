from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl

from jetlag.api.deps import DbConn
from jetlag.db.generated.curses import AsyncQuerier as CurseQuerier, CreateCurseDefinitionParams
from jetlag.db.generated.models import CurseDefinition

router = APIRouter(prefix="/curses", tags=["curses"])


class CurseCreateBody(BaseModel):
    name: str
    duration_rounds: int = 1
    blocks_transit: bool = False
    blocks_questions: bool = False
    video_instruction_url: HttpUrl | None = None


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_curse(conn: DbConn, body: CurseCreateBody) -> CurseDefinition:
    params = CreateCurseDefinitionParams(
        name=body.name,
        duration_rounds=body.duration_rounds,
        blocks_transit=body.blocks_transit,
        blocks_questions=body.blocks_questions,
        video_instruction_url=str(body.video_instruction_url) if body.video_instruction_url else None,
    )
    result = await CurseQuerier(conn).create_curse_definition(arg=params)
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to create curse")
    return result


@router.get("/{curse_id}")
async def get_curse(conn: DbConn, curse_id: UUID) -> CurseDefinition:
    result = await CurseQuerier(conn).get_curse_definition(id=curse_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Curse not found")
    return result


@router.get("")
async def list_curses(conn: DbConn) -> list[CurseDefinition]:
    return [c async for c in CurseQuerier(conn).list_curse_definitions()]
