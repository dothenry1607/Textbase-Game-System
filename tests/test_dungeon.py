import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import dungeon


def test_dungeon_progress():
    d = dungeon.Dungeon(2)
    f1 = d.next_floor()
    assert len(f1) == 1
    f2 = d.next_floor()
    assert len(f2) == 2
    assert d.is_complete()
    assert d.next_floor() == []
