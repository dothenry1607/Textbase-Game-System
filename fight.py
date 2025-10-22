enemy_list = []

def display():
    for i, it in enumerate(enemy_list, 1):
        print(f"{[i]} {it["name"]} - {it["health"]}")

def add(name : str, health : int):
    enemy_list.append({"name": name, "health" : health})