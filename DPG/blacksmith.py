"""Blacksmith service for repairing and enchanting items."""

from typing import Optional
from . import user, item


def repair(item_obj: item.Item, cost: int) -> bool:
    """Spend gold to "repair" an item (dummy operation returning True if paid)."""
    if user.spend_gold(cost):
        # in a full game we might restore durability; here it's a no-op
        return True
    return False


def enchant(item_obj: item.Item, enchantment: str, cost: int) -> bool:
    """Apply an enchantment to an item if the player can pay the cost."""
    if user.spend_gold(cost):
        item_obj.add_enchantment(enchantment)
        return True
    return False


def add_rune(item_obj: item.Item, rune: str, cost: int) -> bool:
    """Embed a rune into the item for a price."""
    if user.spend_gold(cost):
        item_obj.add_rune(rune)
        return True
    return False
