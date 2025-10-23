inventory_list = []

def open_inventory(user):
    print(f"------------- {user}'s Inventory -------------")
    if not inventory_list:
        print("Inventory is empty.")
    else:
        for item in inventory_list:
            print(f"- {item['name']}")
    choice = input("Enter the name of the item you want to use or 'exit' to leave: ").strip()
    if choice.lower() == 'exit':
        return
    for it in inventory_list:
        if it['name'].lower() == choice.lower():
            use_item(it)
            return


def add_item(name: str):
    inventory_list.append({"name": name})

def remove_item(name: str):
    inventory_list.remove(next((it for it in inventory_list if it["name"] == name), None))

def use_item(id):
    print(f"You used {id['name']}!")
    remove_item(id['name'])