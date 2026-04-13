from __future__ import annotations

from uuid import uuid4

import pytest

from jetlag.core.curse_engine import CurseEngineError, apply_curse_to_target, tick_curses_for_round_end
from jetlag.models.curse import ActiveCurse, CurseBlockKind, CurseDefinition


def test_blocks_duplicate_transit() -> None:
    cid = uuid4()
    pid = uuid4()
    defs = {cid: CurseDefinition(name="t", duration_rounds=2, blocks_transit=True)}
    active: list[ActiveCurse] = []
    apply_curse_to_target(defs, active, cid, pid)
    with pytest.raises(CurseEngineError):
        apply_curse_to_target(defs, active, cid, pid)


def test_tick_reduces_duration() -> None:
    c = ActiveCurse(
        curse_id=uuid4(),
        target_player_id=uuid4(),
        remaining_rounds=2,
        block_kind=CurseBlockKind.TRANSIT,
    )
    nxt = tick_curses_for_round_end([c])
    assert len(nxt) == 1
    assert nxt[0].remaining_rounds == 1
    assert tick_curses_for_round_end(nxt) == []
