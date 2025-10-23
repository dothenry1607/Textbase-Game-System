
shop_items = []

existed_items = [
    {"name": "Health Potion", "price": 10},
]

def add_shop(id):
    shop_items.append(existed_items[id])

def remove_shop(name : str):
    shop_items.remove(next((it for it in shop_items if it["name"] == name), None))

def exist_item_check(id):
    return existed_items[id]
