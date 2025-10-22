# 🧰 DPG — Do Playing Game RPG Module

A lightweight **text-based RPG module** written in Python, designed for creating terminal RPG experiences with expandable systems for UI, items, inventory, shops, and audio.  
Rather than being a complete game, **DPG** provides developers with a clean and modular foundation to **build their own RPG projects**.

---

## ✨ Core Features

- 🖥️ **Modular UI System** — Typewriter-style text display, optional skip function, clear screen handling.  
- 🛒 **Shop System** — Easily configurable shops where players can purchase items by number selection.  
- 🧳 **Inventory Management** — Add, display, and organize player items with dictionary-based structure.  
- 💰 **Item Data Structure** — Centralized item definitions for easy balancing and expansion.  
- 🔊 **Audio System (SFX + BGM)** — Powered by `pygame.mixer` for sound effects and background music.  
- 🧠 **Modular Architecture** — Each system is contained in its own file, making it simple to reuse or extend.

---

## 📁 Project Structure

```
📂 DPG
├── UI.py             # Handles text UI and display logic
├── shop.py           # Shop menu and purchasing system
├── item.py           # Item database and adding new items
├── inventory.py      # Inventory storage and functions
├── sfx.py            # Sound effects logic
├── soundtrack.py     # Background music handling
├── logic.py          # Core engine functions and game flow
```

---

## 🧰 Requirements

- Python 3.10+
- Pygame library

```bash
pip install pygame
```

---

## 🕹️ How to Use

### 1. Clone the repo
```bash
git clone https://github.com/YourUsername/YourRepoName.git
cd YourRepoName
```

### 2. Import the modules in your own Python project
```python
import UI
import inventory
import shop
import item
import sfx
import soundtrack
```

### 3. Start building your own RPG logic
You can structure your game loop or story progression and plug in these modules.

Example:
```python
# main.py
import UI
import shop
import inventory
import item

UI.display("Narrator", "Welcome to your adventure!", 0.05)

shop.display_shop("Blacksmith", ("Sword", 100), ("Potion", 25))
inventory.open_inventory("Player1")
```

---

## 🧱 Extending the System

- 🪙 **Add new items** → edit `item.py` or use `add_item()`  
- 🏪 **Create new shops** → use `display_shop()` with custom parameters  
- 🧭 **Customize UI** → change speed, skip behavior, or add animations  
- 🎧 **Add music** → drop your `.wav` or `.mp3` files into the project and load via `soundtrack.py`  

This structure is designed so that anyone can:
- Build story-driven text RPGs
- Prototype narrative games
- Create terminal-based battle systems

---

## 🧑‍💻 Author

- **Name:** Do  
- **GitHub:** [YourUsername](https://github.com/YourUsername)  
- **Project:** DPG (Do Playing Game)

---

## 📜 License

MIT License — free to use and modify.

---

✨ *DPG aims to make building RPG systems fun and modular — so you can focus on storytelling and gameplay instead of reinventing basic systems.*
