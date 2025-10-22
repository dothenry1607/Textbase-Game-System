import item          
import inventory    

def display_shop(shop_name: str = "Shop"):
    print(f"------------- {shop_name} -------------")
    for i, it in enumerate(item.shop_items, 1):
        print(f"[{i}] {it['name']} - ${it['price']}")

    choice = input("Enter the number of the item you want to buy: ").strip()

    if not choice.isdigit():
        print("Invalid input. Please enter a number.")
        return

    idx = int(choice)
    if 1 <= idx <= len(item.shop_items):
        it = item.shop_items[idx - 1]
        inventory.add_item(it["name"])
        print(f"{it['name']} has been added to your inventory!")
    else:
        print("Invalid choice. Please try again.")
