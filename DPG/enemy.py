"""Enemy management and simple object model."""

from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Tuple


@dataclass
class Enemy:
    name: str
    health: int
    max_health: int
    attack: int
    exp: int
    # optional drops: list of (item_name, probability)
    drops: List[Tuple[str, float]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Enemy":
        return cls(**data)


# list of enemies in the current encounter
enemy_list: List[Enemy] = [Enemy("Goblin", 30, 30, 5, 10)]


def add(name: str, health: int, attack: int, exp: int, drops=None) -> None:
    """Add an enemy to the encounter.

    ``drops`` may be a list of ``(item_name, probability)`` tuples.
    """
    enemy_list.append(Enemy(name, health, health, attack, exp, drops or []))


def remove(name: str) -> None:
    """Remove first enemy with matching name."""
    for e in enemy_list:
        if e.name == name:
            enemy_list.remove(e)
            break


def find(name: str) -> Optional[Enemy]:
    """Return first matching enemy or ``None``."""
    for e in enemy_list:
        if e.name == name:
            return e
    return None
