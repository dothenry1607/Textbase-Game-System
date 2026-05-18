import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import generator, enemy


def test_random_enemy():
    e = generator.random_enemy(1,1)
    assert isinstance(e, enemy.Enemy)
    assert 'Goblin' in e.name


def test_populate_encounter():
    generator.populate_encounter(3, 1, 2)
    assert len(enemy.enemy_list) == 3
    for e in enemy.enemy_list:
        assert isinstance(e, enemy.Enemy)
