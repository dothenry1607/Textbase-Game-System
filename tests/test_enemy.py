import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import enemy


def assert_equal(a, b):
    if a != b:
        raise AssertionError(f"{a!r} != {b!r}")


def test_enemy_registry():
    enemy.enemy_list.clear()
    enemy.add("Bat", 20, 4, 5)
    assert len(enemy.enemy_list) == 1
    assert_equal(enemy.enemy_list[0].name, "Bat")
    assert enemy.find("Bat") is enemy.enemy_list[0]

    enemy.add("Bat", 30, 6, 10)
    assert len(enemy.enemy_list) == 2
    enemy.remove("Bat")
    assert len(enemy.enemy_list) == 1

    # test to_dict/from_dict round‑trip
    e = enemy.enemy_list[0]
    d = e.to_dict()
    e2 = enemy.Enemy.from_dict(d)
    assert_equal(e2.name, e.name)
    assert_equal(e2.health, e.health)
