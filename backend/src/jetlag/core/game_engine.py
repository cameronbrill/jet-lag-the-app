from __future__ import annotations

from dataclasses import dataclass, field

from jetlag.models.game import Game, GamePhase
from jetlag.models.player import Player
from jetlag.models.round import RoundPhase, RoundState


class GameEngineError(Exception):
    pass


def _allowed_transitions(phase: RoundPhase) -> set[RoundPhase]:
    graph: dict[RoundPhase, set[RoundPhase]] = {
        RoundPhase.HIDING_PERIOD: {RoundPhase.SEEKING},
        RoundPhase.SEEKING: {RoundPhase.END_GAME},
        RoundPhase.END_GAME: {RoundPhase.FOUND},
        RoundPhase.FOUND: set(),
    }
    return graph[phase]


@dataclass
class GameRuntime:
    game: Game
    players: list[Player] = field(default_factory=list)
    rounds: list[RoundState] = field(default_factory=list)

    def add_player(self, player: Player) -> None:
        if self.game.phase is not GamePhase.LOBBY:
            msg = "Cannot add players outside lobby"
            raise GameEngineError(msg)
        self.players.append(player)

    def _ensure_round_for_current_index(self) -> None:
        idx = self.game.current_round_index
        if not self.players:
            msg = "No players"
            raise GameEngineError(msg)
        while len(self.rounds) <= idx:
            hider = self.players[len(self.rounds) % len(self.players)]
            self.rounds.append(
                RoundState(index=len(self.rounds), hider_player_id=hider.id, phase=RoundPhase.HIDING_PERIOD),
            )

    def start_game(self) -> None:
        if len(self.players) < 2:
            msg = "Need at least two players"
            raise GameEngineError(msg)
        ordered = sorted(self.players, key=lambda p: p.hide_order if p.hide_order is not None else 0)
        self.players = ordered
        self.game.phase = GamePhase.PLAYING
        self.game.current_round_index = 0
        self.rounds.clear()
        self._ensure_round_for_current_index()

    def _current_round(self) -> RoundState:
        if not self.rounds:
            msg = "No active round"
            raise GameEngineError(msg)
        idx = self.game.current_round_index
        if idx < 0 or idx >= len(self.rounds):
            msg = "Round index out of range"
            raise GameEngineError(msg)
        return self.rounds[idx]

    def transition_round_phase(self, new_phase: RoundPhase) -> None:
        r = self._current_round()
        allowed = _allowed_transitions(r.phase)
        if new_phase not in allowed:
            msg = f"Illegal transition {r.phase} -> {new_phase}"
            raise GameEngineError(msg)
        r.phase = new_phase
        if (
            new_phase is RoundPhase.FOUND
            and self.game.phase is GamePhase.PLAYING
            and self.game.current_round_index >= len(self.players) - 1
        ):
            self.game.phase = GamePhase.COMPLETED

    def advance_round_after_found(self) -> None:
        r = self._current_round()
        if r.phase is not RoundPhase.FOUND:
            msg = "Round must be FOUND to advance"
            raise GameEngineError(msg)
        if self.game.phase is GamePhase.COMPLETED:
            return
        self.game.current_round_index += 1
        self._ensure_round_for_current_index()

    def pause(self) -> None:
        r = self._current_round()
        if r.phase in {RoundPhase.HIDING_PERIOD, RoundPhase.SEEKING}:
            r.is_paused = True

    def resume(self) -> None:
        r = self._current_round()
        r.is_paused = False

    def tick_hider_timer(self, delta_seconds: float) -> None:
        if delta_seconds < 0:
            msg = "delta must be non-negative"
            raise GameEngineError(msg)
        r = self._current_round()
        if r.is_paused or r.phase is not RoundPhase.HIDING_PERIOD:
            return
        r.hider_elapsed_seconds += delta_seconds
