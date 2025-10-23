from DPG import user 

def heal_player(amount: int):
    user.player['health'] += amount
    if user.player['health'] > user.player['max_health']:
        user.player['health'] = user.player['max_health']
    print(f"{user.player['name']} healed for {amount} points! Current health: {user.player['health']}/{user.player['max_health']}")