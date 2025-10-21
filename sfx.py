from pygame import mixer
mixer.init() 


def confirm():
    sfx = mixer.Sound("confirm_sfx.wav")
    sfx.play()

