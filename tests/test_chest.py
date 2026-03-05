import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from DPG import chest, item


def test_chest_loot():
    item.shop_items.clear()
    potion = item.register_item("Potion", price=1)
    c = chest.Chest("Test", [("Potion", 1.0)])
    loot = c.open()
    assert potion in loot

    c2 = chest.create_chest("Empty", [])
    assert c2.open() == []
