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
