-- name: InsertShortlink :one
INSERT INTO shortlinks (slug, target_url, created_by_email)
VALUES ($1, $2, $3)
RETURNING *;

-- name: GetShortlink :one
SELECT * FROM shortlinks WHERE slug = $1;

-- name: UpdateShortlinkTarget :execrows
UPDATE shortlinks
SET target_url = $2
WHERE slug = $1 AND created_by_email = $3;
