from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Dict


# predefined character classes; weapons are just flavour and not used by logic
CLASSES: Dict[str, Dict] = {
    "Warrior": {"attack": 15, "max_mana": 30, "skill": "Smash", "skill_type": "single", "skill_cost": 5, "weapon": "Greatsword"},
    "Mage":    {"attack": 8,  "max_mana": 100, "skill": "Fireball", "skill_type": "aoe", "skill_cost": 20, "weapon": "Staff"},
    "Rogue":   {"attack": 12, "max_mana": 50, "skill": "Focus", "skill_type": "buff", "skill_cost": 10, "weapon": "Dagger"},
}


@dataclass
class Player:
    """Represents the current player state."""
    name: str = ""
    pclass: str = ""                # character class name
    weapon: str = ""               # starting/primary weapon
    level: int = 1
    health: int = 100
    mana: int = 50
    attack: int = 10
    max_health: int = 100
    max_mana: int = 50
    gold: int = 0
    # keep track of how many of each monster type the player has killed
    kills: Dict[str, int] = field(default_factory=dict)

    def add_gold(self, amount: int) -> None:
        self.gold = max(0, self.gold + amount)

    def spend_gold(self, cost: int) -> bool:
        if self.gold >= cost:
            self.gold -= cost
            return True
        return False

    def heal(self, amount: int) -> int:
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - before

    def use_mana(self, amount: int) -> bool:
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def regen(self) -> None:
        """Restore health and mana to maximum."""
        self.health = self.max_health
        self.mana = self.max_mana

    def add_kill(self, monster: str, count: int = 1) -> None:
        self.kills[monster] = self.kills.get(monster, 0) + count

    def to_dict(self) -> dict:
        # asdict handles new fields automatically
        return asdict(self)

    def load_dict(self, data: dict) -> None:
        # load known fields, but allow older save files to remain compatible
        self.name = data.get("name", self.name)
        self.level = data.get("level", self.level)
        self.health = data.get("health", self.health)
        self.mana = data.get("mana", self.mana)
        self.attack = data.get("attack", self.attack)
        self.max_health = data.get("max_health", self.max_health)
        self.max_mana = data.get("max_mana", self.max_mana)
        self.gold = data.get("gold", self.gold)
        self.kills = data.get("kills", self.kills)


# module-level player instance for convenience
player = Player()


def set_up(name: str, level: int = 1, health: int = 100, attack: int = 10,
           max_health: int = 100, gold: int = 0, pclass: str = "") -> None:
    """Initialize the player instance and apply class bonuses if provided."""
    player.name = name
    player.level = level
    player.health = health
    player.attack = attack
    player.max_health = max_health
    player.gold = gold
    player.pclass = pclass
    player.weapon = ""
    # apply class defaults
    if pclass in CLASSES:
        data = CLASSES[pclass]
        player.attack = data.get("attack", player.attack)
        player.max_mana = data.get("max_mana", player.max_mana)
        player.mana = player.max_mana
        player.weapon = data.get("weapon", "")
        # if the player has a weapon, give it to inventory later via UI

def get_name():
    return player.name


def add_gold(amount: int) -> None:
    """Increase the player's gold (can be negative)."""
    player.add_gold(amount)


def spend_gold(cost: int) -> bool:
    """Attempt to spend gold; returns ``True`` on success."""
    return player.spend_gold(cost)


def use_mana(cost: int) -> bool:
    """Attempt to consume mana for a skill or spell."""
    return player.use_mana(cost)


def regen() -> None:
    """Restore player's health and mana to full."""
    player.regen()


def record_kill(monster: str, count: int = 1) -> None:
    """Increment the kill counter for a given monster."""
    player.add_kill(monster, count)


def get_kills(monster: str) -> int:
    return player.kills.get(monster, 0)


def display_status():
    print(
        f"Player: {player.name} \n Level: {player.level}\n "
        f"Health: {player.health}/{player.max_health}\n "
        f"Mana: {player.mana}/{player.max_mana}\n "
        f"Attack: {player.attack}"
    )

