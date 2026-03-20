# DPG — Do Playing Game

A minimal, modular **text‑based RPG framework** for Python.  Build
terminal/console adventures by focusing on story and logic; DPG handles the
boilerplate for menus, items, inventory, shops, combat, audio and more.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements & Installation](#requirements--installation)
4. [Quick Start](#quick-start)
5. [API Overview](#api-overview)
6. [Advanced Topics](#advanced-topics)
   * [Experience & Leveling](#experience--leveling)
   * [Currency & Shops](#currency--shops)
   * [Events & Quests](#events--quests)
   * [Combat & Enemies](#combat--enemies)
   * [Dungeons, Bosses & Loot](#dungeons-bosses--loot)
   * [Audio (BGM & SFX)](#audio-bgm--sfx)
   * [Persistence (Save/Load)](#persistence-saveload)
7. [Extending DPG](#extending-dpg)
8. [Project Structure](#project-structure)
9. [FAQ](#faq)
10. [License](#license)
11. [Author](#author)

## Overview

DPG is a lightweight Python package designed as a **foundation for text
role‑playing games**.  It abstracts common systems (menus, inventory,
currency, combat) so you can rapidly prototype or ship interactive stories
without reinventing the wheel.

> The module can be imported into any script; `UI.py` in the repository is an
> example adventure demonstrating many of the features.

## Features

- Modular architecture – import only what you need.
- Menu helpers with validation and typewriter text effects.
- Inventory and item registry with consumables and custom effects.
- Shop system with gold tracking and purchase logic.
- Experience, leveling and enemy dataclasses.
- Random generators for enemies, encounters and dungeons.
- Events, quests and interactive choices.
- Chests, loot tables and gambling mechanics.
- Blacksmith, enchantments and runes.
- Audio support (BGM + SFX) via `pygame.mixer` with no‑op fallbacks.
- Save/load helpers for player state, enemies and dungeons.
- Fully covered by unit tests (see `tests/`).

## Requirements & Installation

- Python **3.8+**

Install with `pip`:

```bash
pip install doplayinggame
```

This includes `pygame` as a dependency for audio features.

Then import the module:

```python
import DPG
```

## Quick Start

Create a simple script:

```python
import DPG

# display formatted text
DPG.logic.display("Narrator", "Welcome to your adventure…")

# configure the player
from DPG import user
user.set_up("Hero", gold=50)

# register an item and open a shop
from DPG import item
item.register_item(
    "Potion", price=10, effect=lambda it: DPG.heal.heal_player(20)
)
DPG.shop.display_shop("General Store")

# simple event and quest example
from DPG import events, quest
events.register_event(
    events.Event("Coin", "You found a coin!", lambda: user.add_gold(1), key="c")
)
quest.register_quest(
    quest.Quest("q1", "Find a coin", ["found_coin"], rewards={"gold": 5})
)
quest.start_quest("q1")

# open inventory and use items
DPG.inventory.open_inventory()

# place this in a file and run: python mygame.py
```

## API Overview

Below is a high‑level map of the primary modules and their responsibilities.

| Module              | Description |
|---------------------|-------------|
| `DPG.logic`         | Text helpers, menus, option prompts, `run_sequence`. |
| `DPG.ui` (UI.py)    | Example game entry point / simple adventure. |
| `DPG.user`          | `Player` dataclass, gold/health manipulation. |
| `DPG.item`          | Registry and helpers for game items. |
| `DPG.inventory`     | Player inventory management. |
| `DPG.shop`          | Shop display and purchase logic. |
| `DPG.exp`           | XP tracking and leveling (`Experience` class). |
| `DPG.level`         | Level manipulation utilities. |
| `DPG.enemy`         | `Enemy` dataclass and combat helpers. |
| `DPG.boss`          | `Boss` subclass with extra rewards. |
| `DPG.generator`     | Random enemy/encounter/dungeon generators. |
| `DPG.dungeon`       | `Dungeon` class modelling multi‑floor areas. |
| `DPG.events`        | Event registration and firing. |
| `DPG.quest`         | Quest tracking and rewards. |
| `DPG.chest`         | Chests with probability loot tables. |
| `DPG.gamble`        | Simple gambling mechanic. |
| `DPG.blacksmith`    | Item repair, enchant, rune systems. |
| `DPG.save`, `DPG.load` | Serialization helpers for game state. |
| `DPG.sfx`, `DPG.soundtrack` | Audio helpers (require pygame). |
| ...                 | See modules under `DPG/` for more details. |

Each module exposes functions and dataclasses; refer to the docstrings in the
source for full signatures.

## Advanced Topics

### Experience & Leveling

```python
from DPG import exp
exp.xp.add(50)            # gain XP, auto level‑ups
print(exp.xp.current, exp.xp.to_level, exp.xp.percent)
exp.xp.scale = 1.1        # customize progression
exp.xp.on_level_up = lambda n: print(f"Leveled up {n} times!")
```

The old `add_exp` helper remains for compatibility.

### Currency & Shops

Player state is encapsulated in `DPG.user.Player`.  Access via
`DPG.user.player`.

```python
DPG.user.player.add_gold(100)
DPG.user.player.spend_gold(25)
```

Shops automatically check balance and display the current gold amount.  You
can customise shop inventories:

```python
DPG.item.shop_items = [
    {"name": "Potion", "price": 25},
    {"name": "Sword",  "price": 150, "stock": 5, "rarity": "rare"},
]
```

### Events & Quests

```python
from DPG import events, quest
events.register_event(events.Event("Coin", "Found a coin!", callback, key="c"))
quest.register_quest(quest.Quest(
    "q1","Find a coin",["found_coin"], rewards={"gold":5}
))
quest.start_quest("q1")
```

Quests track objectives and provide hints via `quest.get_hint()`.

### Combat & Enemies

Enemies use the `Enemy` dataclass with health, attack and XP values.  Bosses
inherit from `Boss`.

### Dungeons, Bosses & Loot

`Dungeon` generates enemies floor by floor.  Use
`generator.random_enemy()` and `generator.populate_encounter()` for random
encounters.  Chests employ `Chest` objects with loot tables; opening returns
items which can be added to inventory.

### Audio (BGM & SFX)

```python
from dpg import sfx, soundtrack
soundtrack.play_bgm("assets/music/intro.mp3", loop=True, volume=0.6)
sfx.play("assets/sfx/confirm.wav", volume=0.8)
```

Call `pygame.mixer.init()` manually if required; modules degrade gracefully
when `pygame` is absent.

### Persistence (Save/Load)

Use `dpg.save.save_game(filename)` and `dpg.load.load_game(filename)` to
serialize the player, enemies, and dungeon state.

## Extending DPG

- Copy `UI.py` as a starting point for your own adventure.
- Add new items via `item.register_item` or by editing `shop_items`.
- Customize shop behavior (stock, descriptions, purchase validators).
- Enhance UI (skip typing, colors with `colorama`, ASCII frames).
- Add new event types, quests, or procedural generators.

For more detailed examples, see the repository’s tests under `tests/`.

## Project Structure

```
dpg/           # core library (do not modify when packaging)
├── blacksmith.py
├── boss.py
├── chest.py
├── dungeon.py
├── enchant.py
├── enemy.py
├── events.py
├── exp.py
├── fight.py
├── gamble.py
├── generator.py
├── heal.py
├── inventory.py
├── item.py
├── level.py
├── load.py
├── logic.py
├── quest.py
├── rune.py
├── save.py
├── sfx.py
├── shop.py
├── soundtrack.py
└── user.py
UI.py            # example game entry point / template
tests/           # unit tests covering functionality
```

> 📁 If you are testing or extending the module, work in `UI.py` or your own
> script – avoid editing files inside `dpg/`.

## FAQ

**Q:** Is this a finished game?  
**A:** No.  It’s a **library** you can use to build games.

**Q:** Do I need audio?  
**A:** No.  Import only `sfx`/`soundtrack` when you want sound.  Modules will
silently no‑op if `pygame` isn’t installed.

**Q:** Where should I keep assets?  
**A:** Typically `assets/music/` and `assets/sfx/`.

**Q:** How do I run the tests?  
**A:** `python -m unittest` or run individual test files in the `tests/`
directory.

## License

MIT – free to use, modify and redistribute.

## Author

Do (Do Playing Game — DPG)

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
