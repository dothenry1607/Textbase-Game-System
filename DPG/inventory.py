from DPG import user, heal
inventory_list = []

def open_inventory():
    print(f"------------- {user.player['name']}'s Inventory -------------")
    if not inventory_list:
        print("Inventory is empty.")
    else:
        for i, item in enumerate(inventory_list, 1):
            print(f"- [{i}] {item['name']} - Quantity: {item['quantity']}")
    choice = input("Enter the number of the item you want to use or '3' to leave: ").strip()
    if choice == "3":
        return
    if not choice.isdigit():
        print("Invalid input. Please enter a number.")
        return
    idx = int(choice)
    if 1 <= idx <= len(inventory_list):
        it = inventory_list[idx - 1]
        use_item(it)


def add_item(name: str, quantity: int = 1):
    if any(it for it in inventory_list if it["name"] == name):
        for it in inventory_list:
            if it["name"] == name:
                it["quantity"] += quantity
                return
    else:
        inventory_list.append({"name": name, "quantity": quantity})

def remove_item(name: str):
    inventory_list.remove(next((it for it in inventory_list if it["name"] == name), None))


def use_item(id):
    print(f"You used {id['name']}!")
    if id['quantity'] > 1:
        id['quantity'] -= 1
    else:
        remove_item(id['name'])
    item_effect(id)
    
    
def item_effect(id):
    if id['name'] == "Health Potion":
        heal.heal_player(50)
