from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Player(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    display_name: str
    hide_order: int | None = None
