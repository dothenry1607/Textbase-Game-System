import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dpg import gamble


def test_gamble():
    # depend on randomness; override random
    import random
    random.random = lambda: 0.0
    assert gamble.gamble(10, win_chance=0.5, payout=2.0) == 10
    random.random = lambda: 1.0
    assert gamble.gamble(10, win_chance=0.5, payout=2.0) == -10


def test_blackjack(monkeypatch, capsys):
    # simulate drawing small cards and standing
    import random
    # control card values by patching randint
    seq = iter([5, 6, 10, 5, 10, 7])
    monkeypatch.setattr(random, 'randint', lambda a, b: next(seq))
    # simulate hitting once then standing
    inputs = iter(['y', 'n'])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    result = gamble.blackjack(20)
    # first two cards 5+6=11; then stand -> dealer draws 10+5+10=25 bust -> win
    assert result == 20
