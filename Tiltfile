docker_compose('./docker-compose.yml')

dc_resource('postgres', labels=['infra'])
dc_resource('valkey', labels=['infra'])

local_resource(
    'db-migrate',
    cmd='mise run //backend:migrate',
    resource_deps=['postgres'],
    labels=['infra'],
)

local_resource(
    'backend',
    cmd='mise run //backend:deps',
    serve_cmd='mise run //backend:start',
    deps=['backend/src/', 'backend/pyproject.toml'],
    resource_deps=['db-migrate', 'valkey'],
    labels=['app'],
)
