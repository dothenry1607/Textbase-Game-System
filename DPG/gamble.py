"""Simple gambling utility."""

import random


def gamble(bet: int, win_chance: float = 0.5, payout: float = 2.0) -> int:
    """Return net gain/loss from a simple coin-flip style bet.

    Remains for backwards compatibility; use ``blackjack`` for the
    more interactive game.
    """
    if bet <= 0:
        return 0
    if random.random() < win_chance:
        return int(bet * (payout - 1))
    else:
        return -bet


def blackjack(bet: int) -> int:
    """Play a trimmed down blackjack against a dealer.

    Returns net gain (+bet) or loss (-bet); the player automatically draws
    cards until they stand or busts.  The dealer draws to at least 17.
    Interaction is textual and uses :func:`input`.
    """
    def draw_card() -> int:
        return random.randint(1, 11)

    total = 0
    print("Blackjack! Try to reach 21 without going over.")
    while True:
        card = draw_card()
        total += card
        print(f"You drew a {card}.  Total {total}.")
        if total > 21:
            print("Busted!")
            return -bet
        cont = input("Hit again? (y/n)\n> ").strip().lower()
        if cont not in ('y', 'yes'):
            break
    # dealer turn
    dealer = 0
    while dealer < 17:
        dealer += draw_card()
    print(f"Dealer has {dealer}.")
    if dealer > 21 or total > dealer:
        print("You win!")
        return bet
    else:
        print("You lose.")
        return -bet
