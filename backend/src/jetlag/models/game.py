from __future__ import annotations

from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class GamePhase(StrEnum):
    LOBBY = "LOBBY"
    PLAYING = "PLAYING"
    COMPLETED = "COMPLETED"


class GameSize(StrEnum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class Game(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    size: GameSize = GameSize.MEDIUM
    phase: GamePhase = GamePhase.LOBBY
    current_round_index: int = 0
