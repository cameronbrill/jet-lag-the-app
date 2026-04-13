from __future__ import annotations

from starlette.testclient import TestClient

from jetlag.config import Settings
from jetlag.main import create_app


def test_ws_join_and_action_snapshot() -> None:
    settings = Settings(jwt_secret="x" * 32, database_url="sqlite+aiosqlite:///:memory:")
    app = create_app(settings)
    client = TestClient(app)
    r = client.post("/api/games", json={"name": "g"})
    game_id = r.json()["id"]
    for n in ("a", "b"):
        client.post(f"/api/games/{game_id}/players", json={"display_name": n})
    client.post(f"/api/games/{game_id}/start")

    with client.websocket_connect("/ws/game") as ws:
        ws.send_json({"type": "join", "game_id": game_id})
        first = ws.receive_json()
        assert first["type"] == "state"
        ws.send_json({"type": "action", "action": "tick", "payload": {"delta_seconds": 2}})
        nxt = ws.receive_json()
        assert nxt["type"] == "state"
        assert nxt["rounds"][0]["hider_elapsed_seconds"] == 2.0
