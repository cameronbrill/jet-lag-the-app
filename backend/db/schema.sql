-- Authoritative schema for jet-lag-the-app backend.
-- Edit this file, then run: mise run //backend:db-diff <name>

CREATE TYPE game_phase AS ENUM ('LOBBY', 'PLAYING', 'COMPLETED');
CREATE TYPE game_size AS ENUM ('SMALL', 'MEDIUM', 'LARGE');
CREATE TYPE round_phase AS ENUM ('HIDING_PERIOD', 'SEEKING', 'END_GAME', 'FOUND');
CREATE TYPE curse_block_kind AS ENUM ('TRANSIT', 'QUESTION');

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE games (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  size game_size NOT NULL DEFAULT 'MEDIUM',
  phase game_phase NOT NULL DEFAULT 'LOBBY',
  current_round_index INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE players (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
  display_name TEXT NOT NULL,
  hide_order INT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_players_game_id ON players(game_id);

CREATE TABLE rounds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
  index INT NOT NULL,
  hider_player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  phase round_phase NOT NULL DEFAULT 'HIDING_PERIOD',
  hider_elapsed_seconds DOUBLE PRECISION NOT NULL DEFAULT 0.0,
  is_paused BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (game_id, index)
);

CREATE INDEX idx_rounds_game_id ON rounds(game_id);

CREATE TABLE curse_definitions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  duration_rounds INT NOT NULL DEFAULT 1,
  blocks_transit BOOLEAN NOT NULL DEFAULT false,
  blocks_questions BOOLEAN NOT NULL DEFAULT false,
  video_instruction_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE active_curses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
  curse_id UUID NOT NULL REFERENCES curse_definitions(id),
  target_player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  remaining_rounds INT NOT NULL,
  block_kind curse_block_kind,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_active_curses_game_id ON active_curses(game_id);

CREATE TABLE shortlinks (
  slug TEXT PRIMARY KEY,
  target_url TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
