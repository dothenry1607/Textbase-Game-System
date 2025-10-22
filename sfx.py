from pygame import mixer
from pygame.time import Clock
mixer.init() 


def play_sfx(sfx : str, wait : bool = False):
    mixer.play(sfx)
    if wait == True:
        while mixer.get_busy():
            Clock().tick(10)

