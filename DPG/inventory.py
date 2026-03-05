from typing import List, Dict

from DPG import user, logic, item

# inventory_list is persisted in save files; each entry is a dict with keys
# "name" and "quantity".  Using simple dicts keeps compatibility with
# existing saves.
inventory_list: List[Dict[str, int]] = []


def list_items() -> List[str]:
    """Return a list of item names currently in the inventory."""
    return [entry["name"] for entry in inventory_list]


def open_inventory() -> None:
    """Interactive inventory screen.  The player may use or drop items."""
    while True:
        print(f"------------- {user.player.name}'s Inventory -------------")
        if not inventory_list:
            print("Inventory is empty.")
            logic.pause()
            return

        for i, entry in enumerate(inventory_list, 1):
            print(f"[{i}] {entry['name']} (x{entry['quantity']})")
        print("[0] Leave inventory")

        choice = logic.get_number_input("Select an item to use/drop")
        if choice == 0:
            return
        if 1 <= choice <= len(inventory_list):
            entry = inventory_list[choice - 1]
            _use_entry(entry)
        else:
            print("Invalid selection.")
            logic.pause()
            logic.clear_screen()


def _use_entry(entry: Dict[str, int]) -> None:
    """Handle using an inventory entry."""
    item_obj = item.get_item_by_name(entry["name"])
    print(f"You used {entry['name']}!")
    if entry["quantity"] > 1:
        entry["quantity"] -= 1
    else:
        remove_item(entry["name"])

    if item_obj and item_obj.effect:
        item_obj.effect(item_obj)


def add_item(name: str, quantity: int = 1) -> None:
    """Add ``quantity`` of ``name`` to the inventory.

    Raises ``ValueError`` if the item is not registered.
    """
    if not item.get_item_by_name(name):
        raise ValueError(f"unknown item '{name}'")

    for entry in inventory_list:
        if entry["name"] == name:
            entry["quantity"] += quantity
            return

    inventory_list.append({"name": name, "quantity": quantity})


def remove_item(name: str) -> None:
    """Remove an item entirely from inventory (no checks)."""
    inventory_list.remove(next((it for it in inventory_list if it["name"] == name), None))
