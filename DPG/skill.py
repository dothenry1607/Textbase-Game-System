from DPG import user, classes

mage_skills = {
    "Fireball": {"damage": 30, "mana_cost": 20},
    "Ice Spike": {"damage": 25, "mana_cost": 15}
}

knight_skills = {
    "Shield Bash": {"damage": 20, "stun_chance": 0.2},
    "Power Strike": {"damage": 35, "stamina_cost": 25}
}

assasin_skills = {
    "Backstab": {"damage": 40, "critical_chance": 0.3},
    "Poison Dart": {"damage": 15, "poison_duration": 5}
}

def get_skills():
    class_name = user.player.get("classes")
    if class_name == "Mage":
        return mage_skills
    elif class_name == "Warrior":
        return knight_skills
    elif class_name == "Assassin:":
        return assasin_skills
    else:
        return {}
    
def use_skill(skill_name: str):
    skills = get_skills()
    if skill_name in skills:
        skill = skills[skill_name]
        print(f"You used {skill_name}!")
        # Here you would implement the actual effect of the skill
        
    else:
        print("Skill not found or not available for your class.")