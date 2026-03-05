import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from DPG import user


def assert_equal(a, b):
    if a != b:
        raise AssertionError(f"{a!r} != {b!r}")


def test_player_basics():
    user.set_up("Hero", level=2, health=50, attack=15, max_health=50, gold=30)
    assert_equal(user.player.name, "Hero")
    assert_equal(user.player.level, 2)
    assert_equal(user.player.gold, 30)

    user.player.add_gold(20)
    assert_equal(user.player.gold, 50)
    assert user.player.spend_gold(40)
    assert_equal(user.player.gold, 10)
    assert not user.player.spend_gold(100)

    healed = user.player.heal(20)
    assert_equal(healed, 20)
    healed = user.player.heal(100)
    assert_equal(healed, 30)    # to max_health

    # mana usage and regen
    user.player.mana = 10
    assert user.use_mana(5)
    assert user.player.mana == 5
    assert not user.use_mana(10)
    user.player.regen()
    assert user.player.health == user.player.max_health
    assert user.player.mana == user.player.max_mana

    # kill tracking
    user.record_kill("Goblin")
    user.record_kill("Goblin", 2)
    assert user.get_kills("Goblin") == 3

    # class selection applies stats and weapon
    user.set_up("Classtester", pclass="Warrior")
    assert user.player.pclass == "Warrior"
    assert user.player.weapon == "Greatsword"
    assert user.player.attack == user.CLASSES["Warrior"]["attack"]
