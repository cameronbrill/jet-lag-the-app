from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from jetlag.api.deps import StoreDep

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


class LeaderboardEntry(BaseModel):
    player_id: UUID
    display_name: str
    best_hiding_seconds: float


@router.get("/{game_id}")
async def leaderboard(store: StoreDep, game_id: UUID) -> list[LeaderboardEntry]:
    rt = store.games.get(game_id)
    if rt is None:
        raise HTTPException(status_code=404, detail="Game not found")
    best: dict[UUID, tuple[str, float]] = {}
    for p in rt.players:
        best[p.id] = (p.display_name, 0.0)
    for rnd in rt.rounds:
        name_seconds = best.get(rnd.hider_player_id)
        if name_seconds is None:
            continue
        display_name, prev = name_seconds
        best[rnd.hider_player_id] = (display_name, max(prev, rnd.hider_elapsed_seconds))
    return [LeaderboardEntry(player_id=pid, display_name=v[0], best_hiding_seconds=v[1]) for pid, v in best.items()]
