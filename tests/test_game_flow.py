import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from DPG import fight

# run UI.main with stubbed fight.display and input sequence

def test_game_runs_without_error(monkeypatch):
    import UI
    # stub fight.display to avoid interactive combat
    monkeypatch.setattr(fight, 'display', lambda: None)
    # make deterministic random results if necessary
    import random
    random.seed(0)
    # stub input to simulate a sequence of player choices:
    # name, visit shop, leave, visit tavern, view quests, open inventory, gamble, enter dungeon, quit
    inputs = iter([
        'Hero',    # choose name
        '1',        # pick Warrior class (first option)
        '1', '0',  # shop: open then leave inside shop code
        '2',       # visit tavern (show job board)
        '1', 'y',  # accept first job
        '7', '',   # view quests then press enter
        '3', '0',  # open inventory then exit
        '4', 'n',  # gamble but decline
        '5', 'n',  # enter dungeon decline
        '9',       # sleep
        '10'       # quit
    ])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs, ''))
    UI.main()

    # also test leaving dungeon mid-run
    # stub fight.display to avoid interactive combat
    monkeypatch.setattr(fight, 'display', lambda: None)
    inputs2 = iter([
        'Hero', '1',            # name and class
        '5', 'y',               # enter dungeon
        # dungeon asks proceed deeper before second floor, we say no
        'n',
        '10'                    # quit
    ])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs2, ''))
    UI.main()
