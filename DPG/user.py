player = {"name": None, "level": None, "health": None, "attack": None}

def set_up(name : str, level : int = 1, health : int = 100, attack : int = 10):
    player["name"] = name
    player["level"] = level 
    player["health"] = health
    player["attack"] = attack


def display_status():
    print(f"Player: {player['name']}\n Level: {player['level']}\n Health: {player['health']}\n Attack: {player['attack']}")
