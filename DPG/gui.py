"""Small Tkinter client for the DPG game engine.

The web adapter is preferable for multiplayer or browser deployment.  This
client provides a dependency-free desktop option using the same GameState
model, without importing Tkinter when the core package is used as a library.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .user import CLASSES
from .webapp import GameState


class DPGWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("DPG Adventure")
        self.root.minsize(520, 420)
        self.game = GameState()

        setup = ttk.LabelFrame(root, text="New game", padding=10)
        setup.pack(fill="x", padx=10, pady=10)
        ttk.Label(setup, text="Name").grid(row=0, column=0, sticky="w")
        self.name = ttk.Entry(setup, width=24)
        self.name.insert(0, "Adventurer")
        self.name.grid(row=0, column=1, padx=6)
        ttk.Label(setup, text="Class").grid(row=0, column=2, sticky="w")
        self.pclass = ttk.Combobox(
            setup, values=[""] + list(CLASSES), state="readonly", width=12
        )
        self.pclass.current(0)
        self.pclass.grid(row=0, column=3, padx=6)
        ttk.Button(setup, text="Start", command=self.start_game).grid(
            row=0, column=4
        )

        self.status = tk.Text(root, height=14, state="disabled", wrap="word")
        self.status.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        actions = ttk.Frame(root, padding=(10, 0, 10, 10))
        actions.pack(fill="x")
        ttk.Button(actions, text="Attack", command=self.attack).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(actions, text="Rest", command=self.rest).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(
            actions, text="Use health potion", command=self.use_potion
        ).pack(side="left")
        self.render("Create a game to begin.")

    def start_game(self) -> None:
        try:
            self.game.setup(self.name.get(), self.pclass.get())
        except ValueError as exc:
            messagebox.showerror("Could not start game", str(exc))
            return
        self.render("A new adventure begins.")

    def attack(self) -> None:
        if not self.game.enemies:
            self.render("There are no enemies remaining.")
            return
        foe = self.game.enemies[0]
        damage = self.game.player.attack
        foe.health -= damage
        message = f"You attacked {foe.name} for {damage} damage."
        if foe.health <= 0:
            self.game.enemies.pop(0)
            self.game.player.add_kill(foe.name)
            self.game.player.add_gold(foe.exp)
            message += f" {foe.name} was defeated."
        else:
            self.game.player.health = max(
                0, self.game.player.health - foe.attack
            )
        self.render(message)

    def rest(self) -> None:
        self.game.player.regen()
        self.render("You recovered your health and mana.")

    def use_potion(self) -> None:
        try:
            healed = self.game.use_item("Health Potion")
        except ValueError:
            self.render("You do not have a Health Potion.")
            return
        self.render(f"You recovered {healed} health.")

    def render(self, message: str) -> None:
        player = self.game.player
        enemies = ", ".join(
            f"{enemy.name} ({enemy.health}/{enemy.max_health})"
            for enemy in self.game.enemies
        ) or "none"
        inventory = ", ".join(
            f"{entry['name']} x{entry['quantity']}"
            for entry in self.game.inventory
        ) or "empty"
        text = (
            f"{message}\n\n"
            f"Player: {player.name or 'Adventurer'}\n"
            f"Class: {player.pclass or 'Adventurer'}\n"
            f"Health: {player.health}/{player.max_health}  "
            f"Mana: {player.mana}/{player.max_mana}\n"
            f"Attack: {player.attack}  Gold: {player.gold}\n"
            f"Inventory: {inventory}\n"
            f"Enemies: {enemies}\n"
        )
        self.status.configure(state="normal")
        self.status.delete("1.0", "end")
        self.status.insert("1.0", text)
        self.status.configure(state="disabled")


def run() -> None:
    """Start the desktop GUI."""
    root = tk.Tk()
    DPGWindow(root)
    root.mainloop()


if __name__ == "__main__":
    run()
