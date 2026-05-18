import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import save, load, user, exp, inventory, enemy


def test_save_and_load(tmp_path, monkeypatch):
    user.set_up("Hero", gold=25)
    exp.xp.reset()
    exp.xp.add(60)
    inventory.inventory_list.clear()
    inventory.add_item("Health Potion", 1)
    enemy.enemy_list.clear()
    enemy.add("Slime", 10, 2, 5)

    # ensure object type as expected
    assert isinstance(enemy.enemy_list[0], enemy.Enemy)

    filename = tmp_path / "savefile.json"
    # monkeypatch get_name to avoid writing to disk in home
    monkeypatch.setattr(save, "name", "test")
    save.save_game(str(filename))

    # change state
    user.player.name = "Other"
    user.player.gold = 0
    exp.xp.reset()
    inventory.inventory_list.clear()
    enemy.enemy_list.clear()

    load.load_game(str(filename))
    assert user.player.name == "Hero"
    assert user.player.gold == 25
    assert exp.xp.current == 60
    assert inventory.inventory_list[0]['name'] == "Health Potion"
    assert enemy.enemy_list[0].name == "Slime"

