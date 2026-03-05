from DPG import user


def level_up(times: int = 1) -> None:
    """Increase the player's level by ``times`` and adjust stats accordingly.

    Parameters
    ----------
    times : int
        Number of levels to gain. Must be at least 1.
    """
    if times < 1:
        raise ValueError("times must be >= 1")

    for _ in range(times):
        user.player["level"] += 1
        user.player["max_health"] += 20
        user.player["attack"] += 5

    # restore health to max after leveling
    user.player["health"] = user.player["max_health"]
    print(
        f"Congratulations! You've reached level {user.player.level}! "
        "Your health and attack have increased."
    )

