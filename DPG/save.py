from . import user, exp, inventory, enemy
import json

name = user.get_name()
def save_game(username):
    # start with player data, then merge in other game state
    save_data = user.player.to_dict()
    # also keep legacy name/level/etc for older loaders
    save_data.update({
        "name": user.player.name,
        "level": user.player.level,
        "health": user.player.health,
        "attack": user.player.attack,
        "gold": user.player.gold,
        # new fields no longer strictly necessary but include for clarity
        "mana": user.player.mana,
        "max_mana": user.player.max_mana,
        "kills": user.player.kills,
    })
    save_data.update({
        "exp": exp.xp.current,
        "exp_to_level_up": exp.xp.to_level,
        "exp_scale": exp.xp.scale,
    })
    save_data["inventory_list"] = inventory.inventory_list
    save_data["enemy_list"] = [e.to_dict() if hasattr(e, 'to_dict') else e for e in enemy.enemy_list]

    with open(f"{username}_savefile.json", 'w') as f:
        json.dump(save_data, f)
    print("Game saved successfully.")