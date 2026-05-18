from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Callable, List, Optional

from . import heal


@dataclass
class Item:
    """Represents an item that can be bought or used.

    ``effect`` is an optional callable that receives the ``Item`` instance when
    the item is consumed; it may perform side effects such as healing the
    player.

    ``enchantments`` and ``runes`` are lists of strings representing any
    magical modifiers applied to the item.  These are purely descriptive at
    the moment and do not change behaviour unless the game logic checks for
    them.
    """

    name: str
    price: int
    effect: Optional[Callable[[Item], None]] = None
    enchantments: List[str] = field(default_factory=list)
    runes: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        # serialise basic data and modifiers; effects are not saved
        return {
            "name": self.name,
            "price": self.price,
            "enchantments": list(self.enchantments),
            "runes": list(self.runes),
        }

    def add_enchantment(self, ench: str) -> None:
        if ench not in self.enchantments:
            self.enchantments.append(ench)

    def add_rune(self, rune: str) -> None:
        if rune not in self.runes:
            self.runes.append(rune)


# list of items currently available in the shop
shop_items: List[Item] = []


def register_item(name: str, price: int,
                  effect: Optional[Callable[[Item], None]] = None,
                  enchantments: Optional[List[str]] = None,
                  runes: Optional[List[str]] = None) -> Item:
    """Register a new item and return the created ``Item`` instance."""
    item = Item(name=name, price=price, effect=effect,
                enchantments=enchantments or [], runes=runes or [])
    shop_items.append(item)
    return item


def get_item_by_name(name: str) -> Optional[Item]:
    return next((i for i in shop_items if i.name == name), None)


# register the default items
register_item("Health Potion", price=10, effect=lambda it: heal.heal_player(50))
