-- name: CreatePlayer :one
INSERT INTO players (game_id, display_name, hide_order)
VALUES ($1, $2, $3)
RETURNING *;

-- name: ListPlayersByGame :many
SELECT * FROM players WHERE game_id = $1 ORDER BY hide_order;

-- name: CountPlayersByGame :one
SELECT count(*) FROM players WHERE game_id = $1;
