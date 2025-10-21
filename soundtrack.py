from pygame.mixer import music, init
from pygame.time import Clock 
from pygame.event import poll
init()



    
def play_music(song : str , wait : bool = False, loop : bool = False):
    music.load(song)
    if loop == True:
        music.play(-1)
    else:
        music.play()
    if wait == True:
        while music.get_busy():
            Clock().tick(10)


