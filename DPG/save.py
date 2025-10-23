from DPG import user, exp, inventory, enemy
import json

def save_game(username= f"{user.player['name']}_savefile.json"):
    save_data = {
        "name" : user.player['name'],
        "level" : user.player['level'],
        "health" : user.player['health'],
        "attack" : user.player['attack'],
        "exp" : exp.exp,
        "exp_to_level_up" : exp.exp_to_level_up,
        "inventory_list" : inventory.inventory_list,
        "enemy_list" : enemy.enemy_list
    }

    with open(username, 'w') as f:
        json.dump(save_data, f)
    print("Game saved successfully.")