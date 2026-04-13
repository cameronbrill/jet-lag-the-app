-- name: CreateShortlink :one
INSERT INTO shortlinks (slug, target_url)
VALUES ($1, $2)
RETURNING *;

-- name: GetShortlink :one
SELECT * FROM shortlinks WHERE slug = $1;
