import user, exp, inventory, enemy, json
def load_game(username= f"{user.player['name']}_savefile.json"):
    try:
        with open(username, 'r') as f:
            save_data = json.load(f)
        
        user.player['name'] = save_data.get("name", user.player['name'])
        user.player['level'] = save_data.get("level", user.player['level'])
        user.player['health'] = save_data.get("health", user.player['health'])
        user.player['attack'] = save_data.get("attack", user.player['attack'])
        exp.exp = save_data.get("exp", exp.exp)
        exp.exp_to_level_up = save_data.get("exp_to_level_up", exp.exp_to_level_up)
        inventory.inventory = save_data.get("inventory", inventory.inventory)
        enemy.enemy_list = save_data.get("enemy_list", enemy.enemy_list)
        
        print("Game loaded successfully.")
    except FileNotFoundError:
        print("Save file not found.")
    except json.JSONDecodeError:
        print("Error loading save file. The file may be corrupted.")