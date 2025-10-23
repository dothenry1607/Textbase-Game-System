enemy_list = [{"name": "Goblin", "health": 30, "attack": 5, "exp": 10}]

def add(name : str, health : int, attack : int, exp : int):
    enemy_list.append({"name": name, "health" : health, "attack": attack, "exp" : exp})

def remove(name : str):
    enemy_list.remove(next((it for it in enemy_list if it["name"] == name), None))