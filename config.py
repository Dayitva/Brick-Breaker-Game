import os
import time

# Board details
SCREEN_HEIGHT, SCREEN_WIDTH = [int(x) for x in os.popen("stty size", "r").read().split()]
WIDTH = SCREEN_WIDTH - 10
HEIGHT = SCREEN_HEIGHT - 5

# WIDTH = 127
# HEIGHT = 39

#Brick details
BRICK_LENGTH = 5

#Player details
PADDLE_LENGTH = 7 
LIVES = 3
SCORE = 0

#Time details
TOTAL_TIME = 150
START_TIME = time.time()