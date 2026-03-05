from dpg import *

# track first-time events
_has_visited_blacksmith = False
_has_visited_tavern = False


def intro():
    logic.display("Narrator", "In the quiet village of Oakham, a young adventurer dreams of glory.", clear_after=True)


def choose_name():
    name = logic.get_input("What is your name, traveler?")
    if not name:
        name = "Adventurer"
    # choose a class
    cls_choices = list(user.CLASSES.keys())
    idx = logic.options("Choose your class:", cls_choices)
    picked = cls_choices[idx-1]
    user.set_up(name, gold=50, pclass=picked)


def visit_shop():
    logic.display("Narrator", "You step into the Rusty Blade Shop, the bell above the door jingling.", clear_after=True)
    shop.display_shop("Rusty Blade Shop")



# pool of potential tavern jobs; tuples are (qid, monster, count, reward)
_tavern_pool = [
    ("gob1", "Goblin", 3, {"gold": 30}),
    ("wolf1", "Wolf", 2, {"gold": 20}),
]


def visit_tavern():
    """Show a job board and let the player accept or decline quests."""
    global _has_visited_tavern
    logic.display("Narrator", "You enter the smoky tavern; voices murmur over ale.", clear_after=True)
    from DPG import quest
    # ensure all jobs are registered so hints work
    for qid, monster, count, reward in _tavern_pool:
        # only register once
        if qid not in quest.quests:
            quest.register_guild_quest(qid, monster, count, reward)
    # only show jobs that are not active and not already completed
    available = [t for t in _tavern_pool if not any(aq.id == t[0] for aq in quest.get_active())]
    if not available:
        logic.display("Guild Master", "No jobs right now, come back later.", clear_after=True)
        return
    print("Job board:")
    for idx, (qid, monster, count, reward) in enumerate(available, 1):
        print(f"[{idx}] Hunt {count} {monster}(s) for {reward.get('gold',0)} gold")
    print("[0] Leave tavern")
    choice = logic.get_number_input("Choose a job number")
    if choice == 0 or choice > len(available):
        logic.display("Guild Master", "Maybe next time.", clear_after=True)
        return
    sel = available[choice-1]
    if logic.yes_no_prompt(f"Accept job to hunt {sel[2]} {sel[1]}(s)?"):
        quest.start_quest(sel[0])
        logic.display("Guild Master", "Good luck out there!", clear_after=True)
    else:
        logic.display("Guild Master", "Suit yourself.", clear_after=True)


def visit_blacksmith():
    """Blacksmith location; may offer a mining quest initially."""
    global _has_visited_blacksmith
    logic.display("Blacksmith", "The forge roars as the smith hammers away.", clear_after=True)
    if not _has_visited_blacksmith:
        _has_visited_blacksmith = True
        from DPG import quest
        quest.register_quest(quest.Quest("mine1", "Bring me 2 ore", ["have_Ore_2"], rewards={"gold":20}))
        quest.start_quest("mine1")
        logic.display("Blacksmith", "Hey there! Mine two ore from the caves and I'll pay you 20 gold.", clear_after=True)
    # enchant as before
    for entry in inventory.inventory_list:
        if entry['name'] == "Sword":
            it = item.get_item_by_name("Sword")
            if it:
                blacksmith.enchant(it, "Sharp", cost=20)
                print("Your sword has been enchanted with Sharp!")
            break



def show_quests():
    """Print active quests along with simple hints."""
    from DPG import quest
    active = quest.get_active()
    if not active:
        logic.display("Narrator", "You have no active quests.", clear_after=True)
        return
    print("Active quests:")
    for q in active:
        print(f"- {q.description}")
        print("  Hint:", quest.get_hint(q.id))
    logic.pause()


def check_quests():
    """Evaluate and complete any active quests and hand out rewards."""
    from DPG import quest
    for q in list(quest.get_active()):
        if quest.complete_quest(q.id, []):
            # grant whatever rewards are specified
            for kind, amt in q.rewards.items():
                if kind == "gold":
                    user.add_gold(amt)
                elif kind == "exp":
                    exp.add_exp(amt)
            logic.display("Narrator", f"Quest '{q.description}' completed!", clear_after=True)



# chest demo is now unused; chest events occur randomly inside the dungeon

def sleep():
    """Player sleeps to restore health/mana and advance time to morning."""
    logic.display("Narrator", "You curl up and sleep as the world turns.", clear_after=True)
    user.regen()
    logic.reset_time()
    logic.display("Narrator", "You wake feeling refreshed.", clear_after=True)


def gamble_demo():
    from DPG import gamble
    logic.display("Narrator", "A lurker in the corner beckons you with a crooked grin.", clear_after=True)
    engage = logic.yes_no_prompt("A shady gambler offers you a 10‑gold bet.  Play?")
    if not engage:
        logic.display("Gambler", "Maybe next time.", clear_after=True)
        return
    logic.display("Gambler", "Care to try your luck?", clear_after=True)
    g = gamble.gamble(10)
    if g >= 0:
        user.add_gold(g)
        print(f"You won {g} gold!")
    else:
        print(f"You lost {-g} gold...")


def embark_dungeon():
    from DPG import dungeon, generator
    logic.display("Narrator", "A dark maw yawns in the hillside, echoing with distant cries.", clear_after=True)
    go = logic.yes_no_prompt("Do you wish to enter the dungeon to the north?")
    if not go:
        logic.display("Guide", "Perhaps another day.", clear_after=True)
        return False
    logic.display("Guide", "The dungeon lies to the north; prepare yourself.", clear_after=True)
    d = dungeon.Dungeon(3)
    while not d.is_complete():
        # if we've already cleared at least one floor, ask whether to continue
        if d.current > 0:
            cont = logic.yes_no_prompt("Proceed deeper into the dungeon (no returns once you go)?")
            if not cont:
                logic.display("Narrator", "You head back to the surface.", clear_after=True)
                return False
        enemies = d.next_floor()
        enemy.enemy_list[:] = enemies
        print(f"Floor {d.current}:")
        fight.display()
        # after fight we might trigger a random event
        import random
        # chest spawn chance
        if random.random() < 0.3:
            from DPG import chest
            logic.display("Narrator", "You notice a hidden treasure chest on the floor.", clear_after=True)
            c = chest.create_chest("Dungeon Chest", [("Health Potion", 0.5), ("Ore", 0.3), ("Monster Claw", 0.2)])
            loot = c.open()
            if loot:
                print("You found:", ", ".join(i.name for i in loot))
                for i in loot:
                    inventory.add_item(i.name)
        # cave mining chance
        if random.random() < 0.2:
            logic.display("Narrator", "You discover a small cave with mineral veins.", clear_after=True)
            if logic.yes_no_prompt("Mine for ore?"):
                # grant random amount of ore
                qty = random.randint(1, 3)
                inventory.add_item("Ore", qty)
                print(f"You mined {qty} ore.")
        if user.player.health <= 0:
            logic.display("Narrator", "You have fallen... game over.")
            return False
        logic.display("Narrator", "You survived the floor.", clear_after=True)
        logic.advance_time()
    # boss encounter
    boss_enemy = boss.Boss("Ogre King", 150, 150, 25, 100, reward_gold=100, reward_items=["Sword"])
    enemy.enemy_list[:] = [boss_enemy]
    logic.display("Narrator", "A fearsome boss appears!", clear_after=True)
    fight.display()
    if user.player.health <= 0:
        logic.display("Narrator", "The boss has defeated you.")
        return False
    user.add_gold(boss_enemy.reward_gold)
    for it in boss_enemy.reward_items:
        inventory.add_item(it)
    logic.display("Narrator", f"You defeated {boss_enemy.name} and earned rewards!", clear_after=True)
    return True



def main():
    intro()
    choose_name()
    # register basic items
    item.register_item("Health Potion", price=5, effect=lambda it: heal.heal_player(30))
    item.register_item("Sword", price=25)
    # weapons for classes (may not be buyable but should exist)
    item.register_item("Greatsword", price=100)
    item.register_item("Staff", price=80)
    item.register_item("Dagger", price=50)
    # resource items
    item.register_item("Ore", price=0)
    item.register_item("Monster Claw", price=0)
    # give starting weapon now that items exist
    if user.player.weapon:
        inventory.add_item(user.player.weapon)
        print(f"You start with a {user.player.weapon}.")

    # nothing to start; quests are awarded via locations/events

    # main loop gives player options until they quit or die
    while True:
        # display time-of-day in prompt
        current = logic.current_time()
        choice = logic.options(
            f"[{current.capitalize()}] What will you do?",
            ["Visit shop", "Visit tavern", "Open inventory", "Gamble", "Enter dungeon",
             "Visit blacksmith", "View quests", "Check status", "Sleep", "Quit"]
        )
        if choice == 1:
            visit_shop()
        elif choice == 2:
            visit_tavern()
        elif choice == 3:
            inventory.open_inventory()
        elif choice == 4:
            gamble_demo()
        elif choice == 5:
            success = embark_dungeon()
            if success:
                visit_blacksmith()
        elif choice == 6:
            visit_blacksmith()
        elif choice == 7:
            show_quests()
        elif choice == 8:
            # display a brief recap of player stats
            logic.display("Narrator", f"{user.player.name}: level {user.player.level}, gold {user.player.gold}", clear_after=True)
        elif choice == 9:
            sleep()
        elif choice == 10:
            break

        # after every action we check whether quests can be completed
        check_quests()
        # also bail out if the player died during an action
        if user.player.health <= 0:
            break

    logic.display("Narrator", "Your journey ends here for now...", clear_after=False)


if __name__ == "__main__":
    main()
 