import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import quest


def test_quest_lifecycle():
    quest.quests.clear()
    quest.active.clear()
    q = quest.Quest(id="q1", description="Test", objectives=["a"], rewards={"gold":10})
    quest.register_quest(q)
    assert quest.start_quest("q1")
    assert q in quest.active
    # hint should mention the task
    assert "a" in quest.get_hint("q1")
    assert not quest.complete_quest("q1", ["b"])
    assert quest.complete_quest("q1", ["a"])
    assert q not in quest.active

    # kill quest
    quest.quests.clear()
    quest.active.clear()
    quest.register_guild_quest("g1", "Goblin", 2, {"gold": 30})
    assert quest.start_quest("g1")
    # no kills yet
    assert not quest.complete_quest("g1", [])
    from dpg import user
    user.record_kill("Goblin", 2)
    assert quest.complete_quest("g1", [])
    assert "g1" not in [qq.id for qq in quest.active]

    # inventory objective
    quest.quests.clear()
    quest.active.clear()
    q2 = quest.Quest("m1", "Collect ore", ["have_Ore_3"], rewards={"gold":10})
    quest.register_quest(q2)
    assert quest.start_quest("m1")
    from dpg import inventory
    inventory.inventory_list.clear()
    inventory.add_item("Ore", 2)
    assert not quest.complete_quest("m1", [])
    inventory.add_item("Ore", 1)
    assert quest.complete_quest("m1", [])
