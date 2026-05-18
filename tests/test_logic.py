import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import logic

# simple helper to temporarily override builtins.input
import builtins


def run_with_input(inputs, func, *args, **kwargs):
    it = iter(inputs)
    orig = builtins.input
    builtins.input = lambda prompt="": next(it)
    try:
        return func(*args, **kwargs)
    finally:
        builtins.input = orig


def test_options():
    # first invalid then valid
    result = run_with_input(["x", "2"], logic.options, "Choose", ["a", "b", "c"])
    assert result == 2


def test_yes_no_prompt():
    assert run_with_input(["maybe", "y"], logic.yes_no_prompt, "Proceed?")
    assert not run_with_input(["n"], logic.yes_no_prompt, "Proceed?")


def test_get_number_input():
    assert run_with_input(["foo", "42"], logic.get_number_input, "Number?") == 42


def test_time_cycle():
    # reset to morning
    logic.reset_time()
    assert logic.current_time() == "morning"
    logic.advance_time()
    assert logic.current_time() == "afternoon"
    logic.advance_time()
    assert logic.current_time() == "evening"
    logic.advance_time()
    assert logic.current_time() == "night"
    logic.advance_time()
    assert logic.current_time() == "morning"
