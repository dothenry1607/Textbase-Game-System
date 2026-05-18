import sys
import os
# ensure repository root is on import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import exp, level

# simple helper to simulate level_up calls
class DummyLevel:
    def __init__(self):
        self.count = 0
    def level_up(self, times: int = 1):
        # mimic the behaviour of the real function by incrementing count
        self.count += times


def assert_equal(a, b, msg=None):
    if a != b:
        raise AssertionError(msg or f"{a!r} != {b!r}")

# reset state
exp.xp.reset()
assert_equal(exp.xp.current, 0)
assert_equal(exp.xp.to_level, 100)

# negative amount
try:
    exp.xp.add(-1)
    raise AssertionError("did not raise on negative")
except ValueError:
    pass

# simple gain
exp.xp.add(50)
assert_equal(exp.xp.current, 50)
assert_equal(exp.xp.to_level, 100)
assert_equal(exp.xp.remaining, 50)
assert_equal(exp.xp.percent, 0.5)

# level up once
exp.xp.reset()
dummy = DummyLevel()
level.level_up = dummy.level_up
exp.xp.add(150)
assert_equal(dummy.count, 1)
assert_equal(exp.xp.current, 50)

# multiple levels
exp.xp.reset()
dummy = DummyLevel()
level.level_up = dummy.level_up
exp.xp.scale = 1
ep = 305
exp.xp.add(ep)
assert_equal(dummy.count, 3)
# leftover = 305 - (100+101+102) = 2
assert_equal(exp.xp.current, 2)

# callback
exp.xp.reset()
called = []
def cb(c):
    called.append(c)
exp.xp.on_level_up = cb
level.level_up = DummyLevel().level_up
exp.xp.add(250)
assert_equal(called, [2])

print("all exp tests passed")
