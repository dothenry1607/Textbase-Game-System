"""Boss-specific logic extending the base Enemy."""

from __future__ import annotations
from dataclasses import dataclass
from .enemy import Enemy


@dataclass
class Boss(Enemy):
    reward_gold: int = 0
    reward_items: list[str] = None

    def __post_init__(self):
        if self.reward_items is None:
            self.reward_items = []
