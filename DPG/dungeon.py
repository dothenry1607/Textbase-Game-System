"""Dungeon generation and traversal helpers."""

from typing import List

from DPG import enemy, generator


class Dungeon:
    def __init__(self, floors: int = 3):
        self.floors = floors
        self.current = 0

    def next_floor(self) -> List[enemy.Enemy]:
        """Generate enemies for the next floor and advance floor counter."""
        if self.current >= self.floors:
            return []
        self.current += 1
        # simple: one more enemy each floor
        return [generator.random_enemy(self.current, self.current) for _ in range(self.current)]

    def is_complete(self) -> bool:
        return self.current >= self.floors
