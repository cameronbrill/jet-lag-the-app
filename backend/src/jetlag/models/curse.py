from __future__ import annotations

from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CurseBlockKind(StrEnum):
    TRANSIT = "TRANSIT"
    QUESTION = "QUESTION"


class CurseDefinition(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    duration_rounds: int = 1
    blocks_transit: bool = False
    blocks_questions: bool = False
    video_instruction_url: str | None = None


class ActiveCurse(BaseModel):
    curse_id: UUID
    target_player_id: UUID
    remaining_rounds: int
    block_kind: CurseBlockKind | None = None
