import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import inventory, item, user


def test_inventory_add_and_use():
    # reset user and inventory
    inventory.inventory_list.clear()
    user.set_up("Test", gold=0)

    # register a dummy item with effect
    called = []
    def eff(it):
        called.append(it.name)
    item.register_item("TestItem", price=0, effect=eff)

    inventory.add_item("TestItem", 2)
    assert inventory.inventory_list == [{"name": "TestItem", "quantity": 2}]

    # use one
    inventory._use_entry(inventory.inventory_list[0])
    assert inventory.inventory_list[0]["quantity"] == 1
    assert called == ["TestItem"]

    # use last one
    inventory._use_entry(inventory.inventory_list[0])
    assert inventory.inventory_list == []


def test_add_unknown_raises():
    inventory.inventory_list.clear()
    try:
        inventory.add_item("NoSuchItem")
        raise AssertionError("expected ValueError")
    except ValueError:
        pass

