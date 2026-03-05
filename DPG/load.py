from DPG import user, exp, inventory, enemy
import json
def load_game(username: str | None = None):
    if username is None:
        username = f"{user.player.name}_savefile.json"
    try:
        with open(username, 'r') as f:
            save_data = json.load(f)
        
        # load player data (use dataclass helper)
        user.player.load_dict(save_data)
        # insure mana/max_mana exist for older saves
        if not hasattr(user.player, 'mana'):
            user.player.mana = user.player.max_mana
        if not hasattr(user.player, 'kills'):
            user.player.kills = {}

        # experience
        xp_data = {
            "current": save_data.get("exp", exp.xp.current),
            "to_level": save_data.get("exp_to_level_up", exp.xp.to_level),
            "scale": save_data.get("exp_scale", exp.xp.scale),
        }
        exp.xp.load_dict(xp_data)

        # inventory and enemies
        inventory.inventory_list = save_data.get("inventory_list", inventory.inventory_list)
        raw_enemies = save_data.get("enemy_list", [])
        # convert dicts back to Enemy objects if necessary
        enemy.enemy_list = [enemy.Enemy(**e) if isinstance(e, dict) else e for e in raw_enemies]
        
        print("Game loaded successfully.")
    except FileNotFoundError:
        print("Save file not found.")
    except json.JSONDecodeError:
        print("Error loading save file. The file may be corrupted.")