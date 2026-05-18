"""Chest/loot mechanics."""

from typing import List, Tuple
import random

from . import item


class Chest:
    def __init__(self, name: str, loot_table: List[Tuple[str, float]]):
        """Create a chest with a list of (item_name, probability) pairs.

        Probabilities should sum to <=1; remaining mass means "nothing".
        """
        self.name = name
        self.loot_table = loot_table

    def open(self) -> List[item.Item]:
        """Return list of items obtained."""
        dropped: List[item.Item] = []
        for name, prob in self.loot_table:
            if random.random() < prob:
                it = item.get_item_by_name(name)
                if it:
                    dropped.append(it)
        return dropped


# convenience constructor

def create_chest(name: str, loot: List[Tuple[str, float]]) -> Chest:
    return Chest(name, loot)
