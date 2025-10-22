inventory_list = []

def open_inventory(user):
    print(f"------------- {user}'s Inventory -------------")
    if not inventory_list:
        print("Inventory is empty.")
    else:
        for item in inventory_list:
            print(f"- {item['name']}")


def add_item(name: str):
    inventory_list.append({"name": name})
