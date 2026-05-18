import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import fight, enemy, user, inventory

# helper for input override
import builtins

def run_with_inputs(inputs, func, *args, **kwargs):
    it = iter(inputs)
    orig = builtins.input
    builtins.input = lambda prompt="": next(it)
    try:
        return func(*args, **kwargs)
    finally:
        builtins.input = orig


def test_basic_attack_and_kill():
    # prepare player and single enemy
    user.set_up("Hero", health=100, attack=50)
    enemy.enemy_list.clear()
    enemy.add("Goblin", 30, 5, 10)
    # run fight: choose enemy '1' to kill instantly
    run_with_inputs(["1"], fight.display)
    assert not enemy.enemy_list
    assert user.get_kills("Goblin") >= 1


def test_skill_uses_mana():
    user.set_up("Mage", health=100, attack=10, max_health=100, gold=0)
    user.player.mana = 20
    enemy.enemy_list.clear()
    enemy.add("Imp", 50, 5, 5)
    # choose skill twice (s) then run (r) to exit
    run_with_inputs(["s", "r"], fight.display)
    assert user.player.mana < 20


def test_run_may_fail(monkeypatch):
    user.set_up("Rogue", health=100, attack=10)
    enemy.enemy_list.clear()
    enemy.add("Wolf", 20, 5, 5)
    import random
    monkeypatch.setattr(random, 'random', lambda: 0.6)
    run_with_inputs(["r", "r"], fight.display)
    assert user.player.health < user.player.max_health or not enemy.enemy_list


def test_multiple_enemies_exit():
    user.set_up("Warrior", health=100, attack=20)
    enemy.enemy_list.clear()
    enemy.add("Goblin", 30, 5, 10)
    enemy.add("Goblin", 30, 5, 10)
    # attack enemy 1 then enemy 1 again
    run_with_inputs(["1", "1"], fight.display)
    assert enemy.enemy_list == []


def test_skill_variation():
    # mage should damage all enemies
    user.set_up("Mage", health=100, attack=10, pclass="Mage")
    enemy.enemy_list.clear()
    enemy.add("Skeleton", 20, 5, 5)
    enemy.add("Skeleton", 20, 5, 5)
    # use skill then run
    run_with_inputs(["s", "r"], fight.display)
    # after skill both enemies should have reduced health or be gone
    assert all(e.health < e.max_health for e in enemy.enemy_list) or not enemy.enemy_list
