-- name: CreateShortlink :one
INSERT INTO shortlinks (slug, target_url)
VALUES ($1, $2)
ON CONFLICT (slug) DO UPDATE SET target_url = EXCLUDED.target_url
RETURNING *;

-- name: GetShortlink :one
SELECT * FROM shortlinks WHERE slug = $1;
