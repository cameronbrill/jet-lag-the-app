from __future__ import annotations

from jetlag.models.curse import CurseDefinition
from jetlag.models.game import Game, GamePhase, GameSize
from jetlag.models.round import RoundPhase, RoundState


def test_game_defaults() -> None:
    g = Game(name="x")
    assert g.phase is GamePhase.LOBBY
    assert g.size is GameSize.MEDIUM


def test_round_state_json_roundtrip() -> None:
    from uuid import uuid4

    r = RoundState(index=0, hider_player_id=uuid4(), phase=RoundPhase.SEEKING)
    data = r.model_dump(mode="json")
    r2 = RoundState.model_validate(data)
    assert r2.phase is RoundPhase.SEEKING


def test_curse_optional_video() -> None:
    c = CurseDefinition(name="n", video_instruction_url=None)
    assert c.video_instruction_url is None
