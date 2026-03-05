from DPG import item, inventory, user, logic


def display_shop(shop_name: str = "Shop"):
    """Simple shop interface that lets the player buy items using gold.

    Items are defined in ``item.shop_items``, each of which must contain at
    least ``name`` and ``price`` keys. The player's gold balance is shown at
    the top. Buying deducts gold via ``user.spend_gold`` and adds the item to
    the inventory if successful.
    """
    while True:
        print(f"------------- {shop_name} -------------")
        print(f"You have {user.player.gold} gold.")
        for i, it in enumerate(item.shop_items, 1):
            print(f"[{i}] {it.name} - {it.price}g")
        print("[0] Leave shop")

        choice = input("Enter the number of the item you want to buy: ").strip()
        if choice == "0":
            return
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            logic.pause()
            logic.clear_screen()
            continue

        idx = int(choice)
        if 1 <= idx <= len(item.shop_items):
            it = item.shop_items[idx - 1]
            if user.spend_gold(it.price):
                inventory.add_item(it.name)
                print(f"You bought {it.name}!")
            else:
                print("You don't have enough gold.")
        else:
            print("Invalid choice. Please try again.")
        logic.pause()
        logic.clear_screen()
