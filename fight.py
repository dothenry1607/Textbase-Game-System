import enemy, user, logic, exp


def display():
    while True:
        print(f"{user.player['name']} - health : {user.player['health']}")
        print("\nvs\n")
        for i, it in enumerate(enemy.enemy_list, 1):
            print(f"[{i}] {it['name']} - {it['health']}")

        choice = input("Choose the enemy number to attack them: ").strip()

        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            return

        idx = int(choice)
        if 1 <= idx <= len(enemy.enemy_list):
            it = enemy.enemy_list[idx - 1]
            it["health"] -= user.player["attack"]
            if it["health"] <= 0:
                enemy.enemy_list.pop(idx - 1)
                print(f"You defeated {it['name']}!")
                exp.add_exp(it["exp"])
                print(f"You gained {it['exp']} exp!")
                
            else:
                print(f"You attacked {it['name']} for {user.player['attack']} damage!")
        else:
            print("Invalid choice. Please try again.")
        for i in enemy.enemy_list:
            user.player["health"] -= i["attack"]
            print(f"{i['name']} attacked you for {i['attack']} damage!")
            if user.player["health"] <= 0:
                print("You have been defeated!")
                return
        logic.clear_screen()


        

