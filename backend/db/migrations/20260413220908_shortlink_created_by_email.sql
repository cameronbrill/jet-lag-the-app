-- Create enum type "game_phase"
CREATE TYPE "game_phase" AS ENUM ('LOBBY', 'PLAYING', 'COMPLETED');
-- Create enum type "game_size"
CREATE TYPE "game_size" AS ENUM ('SMALL', 'MEDIUM', 'LARGE');
-- Create enum type "round_phase"
CREATE TYPE "round_phase" AS ENUM ('HIDING_PERIOD', 'SEEKING', 'END_GAME', 'FOUND');
-- Create enum type "curse_block_kind"
CREATE TYPE "curse_block_kind" AS ENUM ('TRANSIT', 'QUESTION');
-- Create "curse_definitions" table
CREATE TABLE "curse_definitions" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "name" text NOT NULL,
  "duration_rounds" integer NOT NULL DEFAULT 1,
  "blocks_transit" boolean NOT NULL DEFAULT false,
  "blocks_questions" boolean NOT NULL DEFAULT false,
  "video_instruction_url" text NULL,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY ("id")
);
-- Create "shortlinks" table
CREATE TABLE "shortlinks" (
  "slug" text NOT NULL,
  "target_url" text NOT NULL,
  "created_by_email" text NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY ("slug")
);
-- Create "users" table
CREATE TABLE "users" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "email" text NOT NULL,
  "password_hash" text NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY ("id"),
  CONSTRAINT "users_email_key" UNIQUE ("email")
);
-- Create "games" table
CREATE TABLE "games" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "name" text NOT NULL,
  "size" "game_size" NOT NULL DEFAULT 'MEDIUM',
  "phase" "game_phase" NOT NULL DEFAULT 'LOBBY',
  "current_round_index" integer NOT NULL DEFAULT 0,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY ("id")
);
-- Create "players" table
CREATE TABLE "players" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "game_id" uuid NOT NULL,
  "display_name" text NOT NULL,
  "hide_order" integer NULL,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY ("id"),
  CONSTRAINT "players_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "games" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);
-- Create index "idx_players_game_id" to table: "players"
CREATE INDEX "idx_players_game_id" ON "players" ("game_id");
-- Create "active_curses" table
CREATE TABLE "active_curses" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "game_id" uuid NOT NULL,
  "curse_id" uuid NOT NULL,
  "target_player_id" uuid NOT NULL,
  "remaining_rounds" integer NOT NULL,
  "block_kind" "curse_block_kind" NULL,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY ("id"),
  CONSTRAINT "active_curses_curse_id_fkey" FOREIGN KEY ("curse_id") REFERENCES "curse_definitions" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "active_curses_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "games" ("id") ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT "active_curses_target_player_id_fkey" FOREIGN KEY ("target_player_id") REFERENCES "players" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);
-- Create index "idx_active_curses_game_id" to table: "active_curses"
CREATE INDEX "idx_active_curses_game_id" ON "active_curses" ("game_id");
-- Create "rounds" table
CREATE TABLE "rounds" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "game_id" uuid NOT NULL,
  "index" integer NOT NULL,
  "hider_player_id" uuid NOT NULL,
  "phase" "round_phase" NOT NULL DEFAULT 'HIDING_PERIOD',
  "hider_elapsed_seconds" double precision NOT NULL DEFAULT 0.0,
  "is_paused" boolean NOT NULL DEFAULT false,
  "created_at" timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY ("id"),
  CONSTRAINT "rounds_game_id_index_key" UNIQUE ("game_id", "index"),
  CONSTRAINT "rounds_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "games" ("id") ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT "rounds_hider_player_id_fkey" FOREIGN KEY ("hider_player_id") REFERENCES "players" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);
-- Create index "idx_rounds_game_id" to table: "rounds"
CREATE INDEX "idx_rounds_game_id" ON "rounds" ("game_id");
