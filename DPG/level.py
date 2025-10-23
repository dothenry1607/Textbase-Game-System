from DPG import user

def level_up():
    user.player["level"] += 1
    user.player["max_health"] += 20
    user.player["attack"] += 5
    user.player["health"] = user.player["max_health"]
    print(f"Congratulations! You've reached level {user.player['level']}!, your health and attack have increased.")

