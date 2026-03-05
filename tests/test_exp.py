import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from DPG import exp, level


# simple helper to simulate level_up calls
class DummyLevel:
    def __init__(self):
        self.count = 0
    def level_up(self, times: int = 1):
        self.count += times


def assert_equal(a, b, msg=None):
    if a != b:
        raise AssertionError(msg or f"{a!r} != {b!r}")


# reset state
exp.xp.reset()

# negative amount
try:
    exp.xp.add(-5)
    raise AssertionError("did not raise on negative")
except ValueError:
    pass

# simple gain
exp.xp.add(50)
assert_equal(exp.xp.current, 50)
assert_equal(exp.xp.to_level, 100)

# level up once
exp.xp.reset()
dummy = DummyLevel()
level.level_up = dummy.level_up
exp.xp.add(150)  # 100 for level + 50 carry
assert_equal(dummy.count, 1)
assert_equal(exp.xp.current, 50)

# multiple levels
exp.xp.reset()
dummy = DummyLevel()
level.level_up = dummy.level_up
exp.xp.scale = 1  # +1 flat
exp.xp.add(305)  # thresholds:100->101->102->103
assert_equal(dummy.count, 3)
assert_equal(exp.xp.current, 2)  # leftover

# callback
exp.xp.reset()
called = []
exp.xp.on_level_up = lambda c: called.append(c)
level.level_up = DummyLevel().level_up
exp.xp.add(250)
assert_equal(called, [2])

print("exp module tests passed")
