# DPG — Do Playing Game (Text-based RPG Module)

**DPG** is a lightweight Python module for building terminal RPGs.  
It provides a modular foundation (UI, items, inventory, shop, audio) so you can focus on your story and game logic.

## Features
- **UI helpers:** typewriter text, pause, clear screen, menu helpers with validation; ``logic.run_sequence`` executes functions safely
- **Shop system:** currency-aware purchases with gold tracking
- **Inventory:** items with quantities and definable use effects
- **Items data:** register items with price and effects; shop and inventory
  reference the same registry
- **Audio:** BGM + SFX via `pygame.mixer`; modules fallback to no-ops if
  pygame isn't available
- **Modular:** import dpg

## Requirements
- Python 3.10+
- pygame
```bash
pip install pygame
```

## Project Structure (typical)
```
📂 dpg/           # if you are tester, don't touch this folder, open UI.py instead.
├── shop.py        # shop menu & purchase logic (numbered choices)
├── item.py        # item data & helpers (add/edit items)
├── inventory.py   # inventory storage & helpers (add/show items)
├── fight.py       # fighting (display fighting)
├── exp.py         # experience points, scaling and level-up logic (now class-based)
├── level.py       # manipulate level (level up)
├── enemy.py       # controlling the enemy (during the fight)
├── user.py        # user data handling (name, attack, health, etc.)
├── save.py        # save the game
├── load.py        # load the game
├── sfx.py         # sound effects helpers
├── soundtrack.py  # background music helpers
└── logic.py       # orchestration/entry points (e.g., start runner)
UI.py              # this is where you put your code.

```

## Quick Start

### 1) Import modules and display text
```python
import dpg

# basic narration
dpg.logic.display("Narrator", "Welcome to your adventure...")

# player setup
from dpg import user
user.set_up("Hero", gold=50)

# item & shop
from dpg import item
item.register_item("Potion", price=10, effect=lambda it: dpg.heal.heal_player(20))
dpg.shop.display_shop("General Store")

# events & quests
from DPG import events, quest

events.register_event(events.Event("Coin", "You found a coin!", lambda: user.add_gold(1), key="c"))
quest.register_quest(quest.Quest("q1", "Find a coin", ["found_coin"], rewards={"gold":5}))
quest.start_quest("q1")

# chest & loot
import random
c = dpg.chest.create_chest("Wooden Chest", [("Potion", 0.5)])
loot = c.open()
print("Looted", [i.name for i in loot])
for i in loot:
    dpg.inventory.add_item(i.name)

# gamble
from DPG import gamble
print(gamble.gamble(10))

# inventory use
dpg.inventory.open_inventory()
```
### 2) Add items and open a shop
```python

item.shop_items = [
    {"name": "Potion", "price": 25},
    {"name": "Sword",  "price": 150},
]

dpg.shop.display_shop("General Store")
dpg.inventory.open_inventory("Player1")
```

### 3) Play SFX and BGM
```python
from DPG import sfx, soundtrack

# soundtrack.play_bgm("assets/music/intro.mp3", loop=True, volume=0.6)
# sfx.play("assets/sfx/confirm.wav", volume=0.8)
```

> **Note:** Some environments need `pygame.mixer.init()` before playback.

## Usage Pattern
```python
import dpg

def intro():
    dpg.logic.display("Guide", "A quiet wind… a choice awaits you.", 0.03)

def open_store():
    dpg.item.shop_items = [
        {"name": "Potion", "price": 25},
        {"name": "Sword",  "price": 150},
    ]
    dpg.shop.display_shop("Blacksmith")
    dpg.inventory.open_inventory("Player1")

def main():
    intro()
    open_store()
    dpg.logic.display("Narrator", "Thanks for trying DPG!", 0.02, clear_after=False)

if __name__ == "__main__":
    main()
```

## Extending the Module
### Interactive stories and choices

The `UI.py` file shipped alongside the library is a simple text adventure that
demonstrates how to give the player freedom to choose their path.  It uses the
menu helpers (`logic.options`, `logic.yes_no_prompt`) to present a list of
locations (shop, tavern, dungeon, blacksmith, etc.) and yes/no decisions.  The
story also shows how to register multiple quests, offer them, and allow the
player to view active quests along with a hint about what to do next:

```python
from dpg import logic, quest

# register and offer
quest.register_quest(quest.Quest("q1", "Bring me a health potion",
                               ["got_potion"], rewards={"gold":20}))
if logic.yes_no_prompt("A villager asks for help, accept the quest?"):
    quest.start_quest("q1")

# later, when the player asks to see their quests
for q in quest.get_active():
    print(q.description)
    print("Hint:", quest.get_hint(q.id))
```

The tavern has a **job board** that lists available tasks; players can accept
or decline each job.  Guild quests (kill‑X style) are handled via
`quest.register_guild_quest` and may optionally be offered from other places.

Entering a dungeon now gives you the option to turn back between floors – you
aren't forced to fight all the way to the boss.  Random events such as chests
or mining caves may occur on any floor.

Combat features class‑based skills (`[s]` in battle) with effects like
single‑target smash, area‑of‑effect fireball, or temporary buffs.  Classes are
chosen at character creation and determine your starting weapon, stats, and
skill behaviour.

You can copy the structure of `UI.py` to build longer, branching adventures using
all of the features provided by DPG.

### Extending the Module
### Experience system improvements

The experience system was refactored into an ``Experience`` class to make it
reusable and testable. Example usage:

```python
from DPG import exp

exp.xp.add(50)          # gain 50 XP, automatically handles level ups
print(exp.xp.current)    # 50
print(exp.xp.to_level)   # 100
print(exp.xp.percent)    # 0.5
print(exp.xp.remaining)  # 50 more XP needed

# customize progression
exp.xp.scale = 1.1      # next threshold will be multiplied by 1.1 each level

# hook into level-up events
exp.xp.on_level_up = lambda n: print(f"leveled up {n} times!")
```

### Currency and shops

The core player state has been encapsulated in a ``Player`` dataclass
(``DPG.user.Player``) with fields for name, level, health, attack, max_health,
and gold.  Utility methods such as ``heal``, ``add_gold`` and ``spend_gold``
make interacting with the player convenient.  Access the singleton via
``DPG.user.player`` or through the helpers in ``DPG.user``.

Players now have a ``gold`` field; shops display your current balance and
require sufficient funds to purchase items.  Use ``user.add_gold`` and
``user.spend_gold`` to manipulate money.

Items are defined in ``DPG.item`` using ``register_item``; each item may
optionally specify an ``effect`` callable that runs when the item is consumed.

Enemies are now modelled by the ``Enemy`` dataclass (`DPG.enemy.Enemy`),
which tracks health, attack and EXP.  Encounters manipulate a list of
``Enemy`` instances and the save system serialises them automatically.

A simple procedural generator (`DPG.generator`) can produce random enemies
or populate an encounter with a specified number of foes.  Use
``generator.random_enemy()`` or ``generator.populate_encounter()`` to add
variety to combat.

### Events & quests

Register arbitrary game events with ``DPG.events.Event`` and fire them
by key or randomly.  Quests (`DPG.quest`) track objectives and rewards;
start them with ``start_quest`` and mark completion once goals are achieved.

### Chests & loot

Use ``DPG.chest.Chest`` to create treasure chests with probabilistic loot
tables.  Opening a chest returns any items that dropped.  Recipes can
include existing shop items.

### Gambling

The ``DPG.gamble`` module offers a simple ``gamble(bet)`` helper that
returns the net gain or loss based on a win chance and payout multiplier.

### Bosses

Boss enemies extend ``DPG.enemy.Enemy`` via ``DPG.boss.Boss`` and can carry
additional rewards like gold or items when defeated.

### Dungeons

``DPG.dungeon.Dungeon`` models a multi-floor dungeon, generating progressively
stronger enemies with each floor.

### Blacksmith, enchantments & runes

Visit the blacksmith (`DPG.blacksmith`) to repair items, apply enchantments,
or socket runes (each action costs gold).  Enchantments and runes are
stored on ``Item`` objects and can be checked by game logic for special
effects.


### Inventory enhancements

Inventory entries are persisted as simple dictionaries:

```python
inventory.add_item("Health Potion", 2)
print(inventory.inventory_list)
# [{"name": "Health Potion", "quantity": 2}]
```

The interactive inventory screen supports using items and shows quantities.
Item effects are looked up automatically based on the registered item.


The module still exposes helper functions ``add_exp`` for backwards
compatibility; ``exp.check_level_up()`` is a no-op since the check happens
automatically.

### Add new items
```python
# item.py
shop_items = [
  {"name": "Potion", "price": 25, "rarity": "common"},
  {"name": "Sword",  "price": 150, "rarity": "rare"},
]

def add_item(name, price, **extra):
    shop_items.append({"name": name, "price": price, **extra})
```

### Customize shop behavior
- Validate currency before purchase (add `player_gold`).
- Add quantities/stock limits: `{"stock": 5}`.
- Show item details (rarity, description).

### Enhance UI
- Add a “skip typing” option.
- Add colors with `colorama` or ASCII frames.

## FAQ
**Q:** Is this a finished game?  
**A:** No, it’s a **module** for building text RPGs.

**Q:** Can I remove audio?  
**A:** Yes, import only what you need.

**Q:** Where do I put assets?  
**A:** Use `assets/music/` and `assets/sfx/` folders.

## License
MIT — free to use and modify.

## Author
Do (Do Playing Game — DPG)
