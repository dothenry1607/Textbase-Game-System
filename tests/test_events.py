import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import events

called = []

def sample_action():
    called.append(True)


def test_key_event():
    events.events.clear()
    ev = events.Event("Test", "desc", sample_action, key="x")
    events.register_event(ev)
    assert events.trigger_key("x")
    assert called == [True]
    called.clear()
    assert not events.trigger_key("no")


def test_random_event():
    events.events.clear()
    ev = events.Event("R", "r", sample_action)
    events.register_event(ev)
    # monkeypatch random to guarantee event triggers
    import random
    random.random = lambda: 0.0
    r = events.trigger_random(0.5)
    assert r is ev
    assert called == [True]
