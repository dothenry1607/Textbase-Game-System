"""Utility for procedurally generating game content like enemies."""

from random import randint
from typing import Optional

from . import enemy


def random_enemy(min_level: int = 1, max_level: int = 3) -> enemy.Enemy:
    """Return a randomly sized enemy within the given level range.

    The enemy's health, attack and exp scale with the randomly chosen level.
    """
    lvl = randint(min_level, max_level)
    name = f"Goblin Lv{lvl}"
    health = 20 + lvl * 10
    attack = 3 + lvl * 2
    exp_value = 5 + lvl * 3
    return enemy.Enemy(name=name, health=health, max_health=health,
                       attack=attack, exp=exp_value)


def populate_encounter(count: int, min_level: int = 1, max_level: int = 3) -> None:
    """Clear current encounter and add ``count`` random enemies."""
    enemy.enemy_list.clear()
    for _ in range(count):
        enemy.enemy_list.append(random_enemy(min_level, max_level))
