from DPG import user


def heal_player(amount: int) -> int:
    """Heal the current player via ``Player.heal`` and print a message."""
    healed = user.player.heal(amount)
    print(
        f"{user.player.name} healed for {healed} points! "
        f"Current health: {user.player.health}/{user.player.max_health}"
    )
    return healed