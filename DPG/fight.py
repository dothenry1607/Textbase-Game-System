from DPG import enemy, user, logic, exp, inventory


def display():
    # determine skill parameters from player's class
    cls = user.player.pclass
    SKILL_COST = 0
    skill_type = None
    skill_name = ""
    if cls in user.CLASSES:
        data = user.CLASSES[cls]
        SKILL_COST = data.get("skill_cost", 0)
        skill_type = data.get("skill_type")
        skill_name = data.get("skill", "Skill")

    while True:
        if not enemy.enemy_list:
            # nothing left to fight
            return
        print(f"{user.player.name} - health : {user.player.health}/{user.player.max_health} mana: {user.player.mana}/{user.player.max_mana}")
        print("\nvs\n")
        for i, it in enumerate(enemy.enemy_list, 1):
            print(f"[{i}] {it.name} - {it.health}/{it.max_health} health")
        print("[i] Use item   [s] Skill   [r] Run")

        choice = input("Choose action or enemy number: ").strip().lower()
        if choice == 'i':
            inventory.open_inventory()
        elif choice == 's':
            if SKILL_COST and not user.use_mana(SKILL_COST):
                print("Not enough mana!")
            else:
                # apply skill based on type
                if skill_type == 'single':
                    foe = enemy.enemy_list[0]
                    dmg = user.player.attack * 2
                    foe.health -= dmg
                    print(f"You use {skill_name} on {foe.name} for {dmg} damage!")
                    if foe.health <= 0:
                        _handle_defeat(0)
                elif skill_type == 'aoe':
                    print(f"You cast {skill_name} at all enemies!")
                    for idx in range(len(enemy.enemy_list) - 1, -1, -1):
                        foe = enemy.enemy_list[idx]
                        dmg = user.player.attack * 1.5
                        foe.health -= dmg
                        if foe.health <= 0:
                            _handle_defeat(idx)
                elif skill_type == 'buff':
                    print(f"You focus, boosting your attack!")
                    user.player.attack += 5
                elif skill_type == 'heal':
                    healed = user.player.heal(30)
                    print(f"You heal yourself for {healed} health.")
                else:
                    print("You flail about ineffectively.")
        elif choice == 'r':
            import random
            if random.random() < 0.5:
                print("You escaped!")
                return
            else:
                print("You failed to run!")
        elif choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(enemy.enemy_list):
                foe = enemy.enemy_list[idx - 1]
                foe.health -= user.player.attack
                print(f"You attacked {foe.name} for {user.player.attack} damage!")
                if foe.health <= 0:
                    _handle_defeat(idx - 1)
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Invalid input.")

        # enemies take their turn if any remain
        for foe in list(enemy.enemy_list):
            user.player.health -= foe.attack
            print(f"{foe.name} attacked you for {foe.attack} damage!")
            logic.pause()
            if user.player.health <= 0:
                print("You have been defeated!")
                logic.pause()
                return
        logic.clear_screen()


def _handle_defeat(index: int) -> None:
    foe = enemy.enemy_list.pop(index)
    print(f"You defeated {foe.name}!")
    # record kill for quest purposes
    user.record_kill(foe.name)
    # drop items
    import random
    for name, prob in getattr(foe, 'drops', []):
        if random.random() < prob:
            print(f"{foe.name} dropped {name}!")
            inventory.add_item(name)
    exp.add_exp(foe.exp)
    print(f"You gained {foe.exp} exp!")
    logic.pause()
    if not enemy.enemy_list:
        print("All enemies defeated!")
        logic.pause()
        return


        

