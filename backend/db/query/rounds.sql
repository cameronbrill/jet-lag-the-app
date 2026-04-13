-- name: CreateRound :one
INSERT INTO rounds (game_id, index, hider_player_id, phase)
VALUES ($1, $2, $3, $4)
RETURNING *;

-- name: GetRound :one
SELECT * FROM rounds WHERE game_id = $1 AND index = $2;

-- name: ListRoundsByGame :many
SELECT * FROM rounds WHERE game_id = $1 ORDER BY index;

-- name: UpdateRoundPhase :exec
UPDATE rounds SET phase = $2 WHERE id = $1;

-- name: UpdateRoundTimer :exec
UPDATE rounds SET hider_elapsed_seconds = $2, is_paused = $3 WHERE id = $1;
