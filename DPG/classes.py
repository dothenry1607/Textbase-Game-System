from DPG import user
classes = {
    "Warrior": {"health": 150, "attack": 15},
    "Mage": {"health": 100, "attack": 25},
    "Assassin": {"health": 120, "attack": 20}
}
def class_select(class_name: str):
    user.player["classes"] = class_name
    if class_name in classes:
        user.player["health"] = classes[class_name]["health"]
        user.player["attack"] = classes[class_name]["attack"]
        user.player["max_health"] = classes[class_name]["health"]
    else:
        raise ValueError("Invalid class name")