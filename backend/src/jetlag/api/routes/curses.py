from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl

from jetlag.api.deps import StoreDep
from jetlag.models.curse import CurseDefinition

router = APIRouter(prefix="/curses", tags=["curses"])


class CurseCreateBody(BaseModel):
    name: str
    duration_rounds: int = 1
    blocks_transit: bool = False
    blocks_questions: bool = False
    video_instruction_url: HttpUrl | None = None


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_curse(store: StoreDep, body: CurseCreateBody) -> CurseDefinition:
    curse = CurseDefinition(
        name=body.name,
        duration_rounds=body.duration_rounds,
        blocks_transit=body.blocks_transit,
        blocks_questions=body.blocks_questions,
        video_instruction_url=str(body.video_instruction_url) if body.video_instruction_url else None,
    )
    store.curses[curse.id] = curse.model_dump(mode="json")
    return curse


@router.get("/{curse_id}")
async def get_curse(store: StoreDep, curse_id: UUID) -> CurseDefinition:
    raw = store.curses.get(curse_id)
    if raw is None:
        raise HTTPException(status_code=404, detail="Curse not found")
    return CurseDefinition.model_validate(raw)


@router.get("")
async def list_curses(store: StoreDep) -> list[CurseDefinition]:
    return [CurseDefinition.model_validate(v) for v in store.curses.values()]
