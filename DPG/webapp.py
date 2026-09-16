"""FastAPI adapter for running DPG games in a browser.

The terminal API intentionally keeps its module-level state for backwards
compatibility.  The web adapter does not use that state: every browser
session owns a separate :class:`GameState` and uses the same engine model
classes and player methods.
"""

from __future__ import annotations

import copy
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .enemy import Enemy
from .item import get_item_by_name
from .user import CLASSES, Player

try:  # Keep importing ``dpg`` useful when optional web dependencies are absent.
    from fastapi import Cookie, Depends, FastAPI, HTTPException, Request
    from fastapi.responses import FileResponse
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover - exercised only in minimal installs
    FastAPI = None  # type: ignore
    BaseModel = object  # type: ignore

    def Field(*args, **kwargs):  # type: ignore
        return kwargs.get("default")


@dataclass
class GameState:
    player: Player = field(default_factory=Player)
    inventory: List[dict] = field(default_factory=list)
    enemies: List[Enemy] = field(
        default_factory=lambda: [Enemy("Goblin", 30, 30, 5, 10)]
    )

    def status(self) -> dict:
        return {
            "player": self.player.to_dict(),
            "inventory": copy.deepcopy(self.inventory),
            "enemies": [enemy.to_dict() for enemy in self.enemies],
        }

    def setup(self, name: str, pclass: str = "", gold: int = 0) -> None:
        if pclass and pclass not in CLASSES:
            raise ValueError("unknown class")
        self.player = Player(name=name, gold=gold, pclass=pclass)
        if pclass:
            data = CLASSES[pclass]
            self.player.attack = data["attack"]
            self.player.max_mana = data["max_mana"]
            self.player.mana = data["max_mana"]
            self.player.weapon = data["weapon"]
        self.inventory.clear()
        self.enemies = [Enemy("Goblin", 30, 30, 5, 10)]

    def use_item(self, name: str) -> int:
        entry = next((item for item in self.inventory if item["name"] == name), None)
        if not entry or entry["quantity"] < 1:
            raise ValueError("item is not in inventory")
        item = get_item_by_name(name)
        if item is None:
            raise ValueError("unknown item")
        entry["quantity"] -= 1
        if entry["quantity"] == 0:
            self.inventory.remove(entry)
        before = self.player.health
        if item.effect:
            # Built-in effects target the CLI singleton, so implement the
            # supported healing item against this session's player directly.
            if name == "Health Potion":
                self.player.heal(50)
        return self.player.health - before


class _Setup(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    pclass: str = ""
    gold: int = Field(default=0, ge=0)


class _Action(BaseModel):
    action: str
    target: Optional[int] = None
    item: Optional[str] = None


def _make_app() -> "FastAPI":
    app = FastAPI(title="DPG Web", version="0.1.0")
    sessions: Dict[str, GameState] = {}
    static_dir = Path(__file__).with_name("static")

    def state(
        session_id: Optional[str] = Cookie(default=None, alias="dpg_session")
    ) -> tuple[str, GameState]:
        sid = session_id or uuid.uuid4().hex
        sessions.setdefault(sid, GameState())
        return sid, sessions[sid]

    def response(data: dict, sid: str):
        # Returning the cookie on every API response also supports clients
        # which do not preserve cookies between the initial HTML request and
        # their first API request.
        from fastapi.responses import JSONResponse
        result = JSONResponse(data)
        result.set_cookie("dpg_session", sid, httponly=True, samesite="lax")
        return result

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(static_dir / "index.html")

    @app.get("/static/{path:path}", include_in_schema=False)
    def static(path: str):
        file = (static_dir / path).resolve()
        if static_dir.resolve() not in file.parents:
            raise HTTPException(status_code=404, detail="not found")
        return FileResponse(file)

    @app.get("/api/status")
    def status(session=Depends(state)):
        sid, game = session
        return response(game.status(), sid)

    @app.post("/api/setup")
    @app.post("/api/new-game")
    def setup(payload: _Setup, session=Depends(state)):
        sid, game = session
        if not payload.name.strip():
            raise HTTPException(status_code=422, detail="name must not be blank")
        try:
            game.setup(payload.name.strip(), payload.pclass, payload.gold)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        return response(game.status(), sid)

    @app.get("/api/inventory")
    def inventory(session=Depends(state)):
        sid, game = session
        return response({"inventory": copy.deepcopy(game.inventory)}, sid)

    @app.post("/api/action")
    @app.post("/api/actions")
    def action(payload: _Action, session=Depends(state)):
        sid, game = session
        action_name = payload.action.lower()
        message = ""
        if action_name in {"rest", "regen"}:
            game.player.regen()
            message = "You recovered your health and mana."
        elif action_name in {"heal", "use-item", "use_item"}:
            name = payload.item or "Health Potion"
            try:
                healed = game.use_item(name)
            except ValueError as exc:
                raise HTTPException(status_code=400, detail=str(exc))
            message = f"You recovered {healed} health."
        elif action_name == "attack":
            if not game.enemies:
                raise HTTPException(status_code=400, detail="no enemies remain")
            index = payload.target if payload.target is not None else 0
            if not 0 <= index < len(game.enemies):
                raise HTTPException(status_code=400, detail="invalid target")
            foe = game.enemies[index]
            damage = game.player.attack
            foe.health -= damage
            message = f"You attacked {foe.name} for {damage} damage."
            if foe.health <= 0:
                game.enemies.pop(index)
                game.player.add_kill(foe.name)
                game.player.add_gold(foe.exp)
                message += f" {foe.name} was defeated."
            for remaining in game.enemies:
                game.player.health = max(0, game.player.health - remaining.attack)
        else:
            raise HTTPException(status_code=400, detail="unsupported action")
        return response({"message": message, **game.status()}, sid)

    return app


if FastAPI is not None:
    app = _make_app()
else:  # pragma: no cover
    app = None


def create_app():
    """Return a fresh app (useful for tests and multiple independent servers)."""
    if FastAPI is None:
        raise RuntimeError("Install the 'web' extra to use the FastAPI adapter")
    return _make_app()


def run() -> None:
    """Start the development web server (the ``dpg-web`` console script)."""
    import uvicorn

    uvicorn.run("DPG.webapp:app", host="127.0.0.1", port=8000, reload=False)
