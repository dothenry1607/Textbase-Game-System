import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import boss


def test_boss_creation():
    b = boss.Boss("Dragon", 100, 100, 20, 50, reward_gold=100, reward_items=["Gem"])
    assert b.name == "Dragon"
    assert b.reward_gold == 100
    assert b.reward_items == ["Gem"]
