
player = {"name": None, "level": None, "health": None, "attack": None, "max_health": None}

def set_up(name : str, level : int = 1, health : int = 100, attack : int = 10, max_health: int = 100):
    player_update = {
        "name": name,
        "level": level,
        "health": health,
        "attack": attack,
        "max_health": max_health
    }
    player.update(player_update)

def get_name():
    return player['name']

def display_status():
    print(f"Player: {player['name']} \n Level: {player['level']}\n Health: {player['health']}/{player['max_health']}\n Attack: {player['attack']}")

