import os
import config
from game import *

os.system('clear')
print("\033[0;0H")
print("\033[?25l")

for level in range(1, 4):
    if level == 3:
        config.BOSS_LEVEL = True
    my_game = Game(level)
    my_game.play()

# my_game = Game(3)
# my_game.play()
    
print("\033[?25h")