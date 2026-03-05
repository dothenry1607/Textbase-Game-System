import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from DPG import shop, user, item, inventory


def test_shop_purchase():
    # prepare environment
    inventory.inventory_list.clear()
    user.set_up("Test", gold=50)
    item.shop_items.clear()
    item.register_item("Cheap", price=10)
    item.register_item("Expensive", price=100)

    # simulate buying cheap item
    assert user.player.gold == 50
    assert user.spend_gold(10)
    inventory.add_item("Cheap")
    assert user.player.gold == 40
    assert inventory.inventory_list[0]['name'] == "Cheap"

    # cannot buy too expensive
    assert not user.spend_gold(100)
    assert user.player.gold == 40

