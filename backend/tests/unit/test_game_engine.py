from __future__ import annotations

import pytest

from jetlag.core.game_engine import GameEngineError, GameRuntime
from jetlag.models.game import Game, GamePhase
from jetlag.models.player import Player
from jetlag.models.round import RoundPhase


def test_start_game_requires_two_players() -> None:
    g = Game(name="t")
    rt = GameRuntime(game=g)
    rt.add_player(Player(display_name="a", hide_order=0))
    with pytest.raises(GameEngineError):
        rt.start_game()


def test_happy_path_round_transitions() -> None:
    g = Game(name="t")
    rt = GameRuntime(game=g)
    rt.add_player(Player(display_name="a", hide_order=0))
    rt.add_player(Player(display_name="b", hide_order=1))
    rt.start_game()
    assert g.phase is GamePhase.PLAYING
    rt.transition_round_phase(RoundPhase.SEEKING)
    rt.transition_round_phase(RoundPhase.END_GAME)
    rt.transition_round_phase(RoundPhase.FOUND)
    assert g.phase is GamePhase.PLAYING
    rt.advance_round_after_found()
    rt.transition_round_phase(RoundPhase.SEEKING)
    rt.transition_round_phase(RoundPhase.END_GAME)
    rt.transition_round_phase(RoundPhase.FOUND)
    assert g.phase is GamePhase.COMPLETED


def test_timer_pauses() -> None:
    g = Game(name="t")
    rt = GameRuntime(game=g)
    rt.add_player(Player(display_name="a", hide_order=0))
    rt.add_player(Player(display_name="b", hide_order=1))
    rt.start_game()
    rt.pause()
    rt.tick_hider_timer(5.0)
    assert rt.rounds[0].hider_elapsed_seconds == 0.0
    rt.resume()
    rt.tick_hider_timer(3.0)
    assert rt.rounds[0].hider_elapsed_seconds == 3.0


def test_illegal_transition() -> None:
    g = Game(name="t")
    rt = GameRuntime(game=g)
    rt.add_player(Player(display_name="a", hide_order=0))
    rt.add_player(Player(display_name="b", hide_order=1))
    rt.start_game()
    with pytest.raises(GameEngineError):
        rt.transition_round_phase(RoundPhase.FOUND)
