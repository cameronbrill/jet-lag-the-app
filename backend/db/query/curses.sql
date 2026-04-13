-- name: CreateCurseDefinition :one
INSERT INTO curse_definitions (name, duration_rounds, blocks_transit, blocks_questions, video_instruction_url)
VALUES ($1, $2, $3, $4, $5)
RETURNING *;

-- name: GetCurseDefinition :one
SELECT * FROM curse_definitions WHERE id = $1;

-- name: ListCurseDefinitions :many
SELECT * FROM curse_definitions ORDER BY created_at DESC;

-- name: CreateActiveCurse :one
INSERT INTO active_curses (game_id, curse_id, target_player_id, remaining_rounds, block_kind)
VALUES ($1, $2, $3, $4, $5)
RETURNING *;

-- name: ListActiveCursesByGame :many
SELECT * FROM active_curses WHERE game_id = $1;

-- name: DecrementActiveCurses :exec
UPDATE active_curses SET remaining_rounds = remaining_rounds - 1 WHERE game_id = $1;

-- name: DeleteExpiredCurses :exec
DELETE FROM active_curses WHERE game_id = $1 AND remaining_rounds <= 0;
