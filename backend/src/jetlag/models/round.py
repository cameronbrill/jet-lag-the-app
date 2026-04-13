from __future__ import annotations

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class RoundPhase(StrEnum):
    HIDING_PERIOD = "HIDING_PERIOD"
    SEEKING = "SEEKING"
    END_GAME = "END_GAME"
    FOUND = "FOUND"


class RoundState(BaseModel):
    index: int
    hider_player_id: UUID
    phase: RoundPhase = RoundPhase.HIDING_PERIOD
    hider_elapsed_seconds: float = 0.0
    is_paused: bool = False
