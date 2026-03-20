import dpg
import sys
def game_over():
    sys.exit()
dpg.logic.display("???", "God is watching you.", delay= 0.1)
dpg.logic.display("???", "Every choice has consequences.", delay= 0.1)
dpg.logic.display("???", "Choose wisely.", delay= 0.1)
dpg.logic.display("", "You wake up in a dark room, with no memory of how you got there.", delay= 0.02)
while True:
    option_1 = dpg.logic.options("What do you do?", ["Close your eyes", "Look around", "Stand up"])
    if option_1 == 1:
        dpg.logic.display("", "You close your eyes, trying to forget where you are. But the darkness is overwhelming, and you feel a sense of panic rising within you.", delay= 0.02)
        dpg.logic.display("", "You decided to open your eyes again, as a way to tell the darkness that you are not defeated.")
    elif option_1 == 2:
        dpg.logic.display("", "You look around, but all you see is darkness. You can't make out any shapes or objects.", delay= 0.02)
        dpg.logic.display("", "You feel a sense of hopelessness, as if you are trapped in this darkness forever.")
    elif option_1 == 3:
        dpg.logic.display("", "You stand up, trying to get a better sense of your surroundings. But the darkness is so thick that you can't see anything.", delay= 0.02)
        dpg.logic.display("", "You feel a sense of determination, as if you are ready to face whatever challenges lie ahead.")
        break 
dpg.logic.display("", "You decided to walk forward, hoping to find a way out of the darkness. As you walk, you start to hear faint sounds in the distance, like whispers or footsteps.", delay= 0.02)
dpg.logic.display("", "You can't tell where the sounds are coming from, but they seem to be getting louder. You feel a sense of unease, as if something is following you.", delay= 0.02)
dpg.logic.display("", "You keep walking, trying to ignore the sounds. But they keep getting louder, until you can hear them clearly. You realize that they are coming from behind you.")
dpg.logic.display("", "You sense an object that large enough that you could hide behind it.")
while True:
    option_2 = dpg.logic.options("What do you do?", ["Keep walking", "Turn around", "Hide"])
    if option_2 == 1:
        dpg.logic.display("", "You keep walking, trying to ignore the sounds. But they keep getting louder, until you can hear them clearly. You realize that they are coming from behind you.", delay= 0.02)
        dpg.logic.display("", "You feel a sense of dread, as if something is about to attack you.")
        dpg.logic.display("", "Suddenly, you feel a cold hand grab your shoulder, and you are pulled into the darkness. You scream, but no one can hear you.", delay= 0.02)
        dpg.logic.display("", "You have been caught by the darkness, and you are trapped forever.")
        game_over()
    elif option_2 == 2:
        dpg.logic.display("", "You turn around, and see a shadowy figure standing in the darkness. You can't make out any details, but you can feel its presence.", delay= 0.02)
        dpg.logic.display("", "You feel a sense of fear, as if the figure is going to harm you.")
        dpg.logic.display("", "The figure starts to move towards you, and you realize that you have to do something quickly.", delay= 0.02)
        while True:
            option_3 = dpg.logic.options("What do you do?", ["Run", "Fight", "Hide"])
            if option_3 == 1:
                dpg.logic.display("", "You try to run, but the darkness is so thick that you can't see where you're going. You stumble and fall, and the figure catches up to you.", delay= 0.02)
                dpg.logic.display("", "You scream, but no one can hear you. You have been caught by the darkness, and you are trapped forever.")
                game_over()
            elif option_3 == 2:
                dpg.logic.display("", "You try to fight the figure, but it's too strong. It easily overpowers you, and you are thrown to the ground.", delay= 0.02)
                dpg.logic.display("", "You scream, but no one can hear you. You have been caught by the darkness, and you are trapped forever.")
                game_over()
            elif option_3 == 3:
                dpg.logic.display("", "You hide behind a nearby object, trying to stay out of sight. The sounds get louder, and you can feel the figure getting closer.", delay= 0.02)
                dpg.logic.display("", "You hold your breath, hoping that the figure won't find you.")
                dpg.logic.display("", "The figure gets closer and closer, until it's right next to you. You can feel its breath on your skin, and you know that it can sense you.", delay= 0.02)
                dpg.logic.display("", "It's too late, the figure already found you, it grabs you and pulls you into the darkness. You scream, but no one can hear you. You have been caught by the darkness, and you are trapped forever.")
                game_over()
    elif option_2 == 3:
        dpg.logic.display("", "You hide behind the nearby object, trying to stay out of sight. The sounds get louder, and you can feel the figure getting closer.", delay= 0.02)
        dpg.logic.display("", "You hold your breath, hoping that the figure won't find you.")
        dpg.logic.display("", "The figure gets closer and closer, until it's right next to you. You can feel its breath on your skin, but it doesn't seem to notice you.", delay= 0.02)
        dpg.logic.display("", "You wait until the figure moves away, and then you continue walking, hoping to find a way out of the darkness.", delay= 0.02)
        break
dpg.logic.display("", "Time past, you feel like enternity. You start to lose hope, but you keep walking, hoping to find a way out of the darkness. Suddenly, you see a faint light in the distance.", delay= 0.02)
dpg.logic.display("", "You run towards the light, and as you get closer, you realize that it's a door. You open the door, and you see a bright light on the other side.", delay= 0.02)
dpg.logic.display("", "You step through the door, and you find yourself in a beautiful garden. You can see flowers, trees, and a clear blue sky. You feel a sense of relief, as if you have finally escaped the darkness.", delay= 0.02)
dpg.logic.display("", "You walk through the garden, then you notice a tea table. You sit down at the table, and you see a cup of tea in front of you. You take a sip, and you feel a sense of calm wash over you.", delay= 0.02)
dpg.logic.display("", "Suddenly, you see a person walk out of some path in the garden. It's a girl, she looks at you and smiles. You feel a sense of familiarity, as if you have met her before.", delay= 0.02)
dpg.logic.display("", "She walks towards you, and you can see that she has a kind face and gentle eyes. She sits down at the table with you.", delay= 0.02)
dpg.logic.display("???", "2000 years ago, the great war of Dusk happened. Darkness surround the planet, The world was on the brink of destruction, and humanity was desperate for salvation.", delay= 0.1)
dpg.logic.display("???", "People prayed to the gods for help, but their prayers went unanswered. In their desperation, they turned to a powerful sorcerer named Gadner, who promised to save them from the darkness.", delay= 0.1)
dpg.logic.display("???", "Gadner is the son of the god of light, he has the power to control light, thing that can push back the destruction, but his power was not enough.", delay= 0.1)
dpg.logic.display("???", "When god abandon us, lord Gadner decided to turn himself into a vessel for Valuga - The angel that fallen into hell.", delay= 0.1)
dpg.logic.display("???", "Valuga was a powerful being, with the ability to control darkness and shadows. Gadner believed that by merging with Valuga, he could gain the power to save humanity from the darkness.", delay= 0.1)
dpg.logic.display("???", "However, Valuga is known as the demon among the angels. Days and year in hell have turn him into a threatened creature. Gadner has no option but to turn his soul into the god box, where it trap the soul of Valuga, at the cost of Gadner himself.", delay = 0.1)
dpg.logic.display("???","The god box was powerful enough that it clear out all of the darkness and bring back the Dawn to Paradia.", delay = 0.1)
dpg.logic.display("???","However, the god box is also a prison for Valuga, and it is said that if the box is ever opened, Valuga will be released and bring darkness back to the world.", delay = 0.1)
dpg.logic.display("???", "After 2000 years, the box that capture Valuga had losen and start to lost it power.", delay = 0.1)
dpg.logic.display("???", "You however, are not from this world.", delay = 0.2)
dpg.logic.display("???", "The room you were just in, is the summonning gate to the after life from another world.", delay = 0.1)
dpg.logic.display("???", "The creature that you encounter in that hallway, was a test to see if you can handle against the darkness, against Valuga power.", delay= 0.1)
dpg.logic.display("???", "You was summon here with a mission, to save Paradia from the awakening of Valuga.", delay = 0.1)
