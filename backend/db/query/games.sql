-- name: CreateGame :one
INSERT INTO games (name, size)
VALUES ($1, $2)
RETURNING *;

-- name: GetGame :one
SELECT * FROM games WHERE id = $1;

-- name: UpdateGamePhase :exec
UPDATE games SET phase = $2, current_round_index = $3 WHERE id = $1;

-- name: ListGames :many
SELECT * FROM games ORDER BY created_at DESC;
