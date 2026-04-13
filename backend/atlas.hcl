env "local" {
  src = "file://db/schema.sql"
  dev = "docker://postgres/18/dev?search_path=public"
  migration {
    dir = "file://db/migrations"
  }
}
