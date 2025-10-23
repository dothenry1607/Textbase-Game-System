from DPG import user

def level_up():
    user.player["level"] += 1
    print(f"Congratulations! You've reached level {user.player['level']}!")

