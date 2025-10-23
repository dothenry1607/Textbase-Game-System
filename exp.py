import level


exp = 0
exp_to_level_up = 100
level_up_scale = 20
def add_exp(amount : int):
    global exp, exp_to_level_up
    exp += amount
    
while True:
    if exp >= exp_to_level_up:     
        exp = 0 
        exp_to_level_up += level_up_scale
        level.level_up()    