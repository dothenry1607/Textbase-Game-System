import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from DPG import blacksmith, item, user


def test_blacksmith():
    user.set_up("Smith", gold=100)
    i = item.register_item("Sword", price=50)
    assert blacksmith.enchant(i, "Flame", cost=20)
    assert "Flame" in i.enchantments
    assert user.player.gold == 80
    assert blacksmith.add_rune(i, "Ruby", cost=10)
    assert "Ruby" in i.runes
    assert user.player.gold == 70
    # repair with insufficient funds
    user.player.gold = 5
    assert not blacksmith.repair(i, cost=10)
