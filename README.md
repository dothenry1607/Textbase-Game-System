# DPG — Do Playing Game (Text-based RPG Module)

**DPG** is a lightweight Python module for building terminal RPGs.  
It provides a modular foundation (UI, items, inventory, shop, audio) so you can focus on your story and game logic.

## Features
- **UI helpers:** typewriter text, pause, clear screen, simple 2-option menus
- **Shop system:** numbered selection, purchase flow
- **Inventory:** dictionary-based items; easy to print/manage
- **Items data:** simple in-code “database” (list/dicts) you can extend
- **Audio:** BGM + SFX via `pygame.mixer`
- **Modular:** import only what you need

## Requirements
- Python 3.10+
- pygame
```bash
pip install pygame
```

## Project Structure (typical)
```
📂 dpg/
├── UI.py          # text UI helpers (display, pause, clear, simple menus)
├── shop.py        # shop menu & purchase logic (numbered choices)
├── item.py        # item data & helpers (add/edit items)
├── inventory.py   # inventory storage & helpers (add/show items)
├── sfx.py         # sound effects helpers
├── soundtrack.py  # background music helpers
└── logic.py       # orchestration/entry points (e.g., start runner)
```

## Quick Start

### 1) Import modules and display text
```python
import dpg

dpg.logic.display("Narrator", "Welcome to your adventure...")
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
