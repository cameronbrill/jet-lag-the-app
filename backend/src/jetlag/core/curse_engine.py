from __future__ import annotations

from uuid import UUID

from jetlag.models.curse import ActiveCurse, CurseBlockKind, CurseDefinition


class CurseEngineError(Exception):
    pass


def apply_curse_to_target(
    definitions: dict[UUID, CurseDefinition],
    active: list[ActiveCurse],
    curse_id: UUID,
    target_player_id: UUID,
) -> list[ActiveCurse]:
    if curse_id not in definitions:
        msg = "Unknown curse"
        raise CurseEngineError(msg)
    definition = definitions[curse_id]
    block_kind: CurseBlockKind | None = None
    if definition.blocks_transit:
        block_kind = CurseBlockKind.TRANSIT
    elif definition.blocks_questions:
        block_kind = CurseBlockKind.QUESTION

    if definition.blocks_transit:
        for c in active:
            if c.target_player_id == target_player_id and c.block_kind == CurseBlockKind.TRANSIT:
                msg = "At most one transit-blocking curse"
                raise CurseEngineError(msg)
    if definition.blocks_questions:
        for c in active:
            if c.target_player_id == target_player_id and c.block_kind == CurseBlockKind.QUESTION:
                msg = "At most one question-blocking curse"
                raise CurseEngineError(msg)

    active.append(
        ActiveCurse(
            curse_id=curse_id,
            target_player_id=target_player_id,
            remaining_rounds=definition.duration_rounds,
            block_kind=block_kind,
        ),
    )
    return active


def tick_curses_for_round_end(active: list[ActiveCurse]) -> list[ActiveCurse]:
    updated: list[ActiveCurse] = []
    for c in active:
        remaining = c.remaining_rounds - 1
        if remaining > 0:
            updated.append(c.model_copy(update={"remaining_rounds": remaining}))
    return updated
