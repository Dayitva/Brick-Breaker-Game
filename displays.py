import config
import time
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

"""
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
"""

def bottom_display(level):
    print(Fore.WHITE + Back.BLACK + "                       ".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "Lives : {} | Score : {} | Time : {:.2f} | Level : {}".format(config.LIVES, config.SCORE, time.time() - config.START_TIME, level).center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "                       ".center(config.WIDTH))
    
def boss_display(health):
    print(Fore.WHITE + Back.BLACK + "                       ".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "Lives : {} | Score : {} | Time : {:.2f} | Boss Health : {}".format(config.LIVES, config.SCORE, time.time() - config.START_TIME, health).center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "                       ".center(config.WIDTH))
        
def lives_over_display():
    for _ in range(int(config.HEIGHT/2)):
        print(Fore.WHITE + Back.BLACK + "          ".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "LIVES OVER!!!".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "Score : {}".format(config.SCORE).center(config.WIDTH))
    for _ in range(int(config.HEIGHT/2)):
        print(Fore.WHITE + Back.BLACK + "          ".center(config.WIDTH))
    
def quit_display():
    for _ in range(int(config.HEIGHT/2)):
        print(Fore.WHITE + Back.BLACK + "          ".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "YOU QUIT THE GAME".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "Score : {}".format(config.SCORE).center(config.WIDTH))
    for _ in range(int(config.HEIGHT/2)):
        print(Fore.WHITE + Back.BLACK + "          ".center(config.WIDTH))
    
def win_display():
    for _ in range(int(config.HEIGHT/2)):
        print(Fore.WHITE + Back.BLACK + "          ".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "YOU WON!!!".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "Score : {}".format(config.SCORE).center(config.WIDTH))
    for _ in range(int(config.HEIGHT/2)):
        print(Fore.WHITE + Back.BLACK + "          ".center(config.WIDTH))
    
def lose_display():
    for _ in range(int(config.HEIGHT/2)):
        print(Fore.WHITE + Back.BLACK + "          ".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "YOU LOSE!!!".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "Score : {}".format(config.SCORE).center(config.WIDTH))
    for _ in range(int(config.HEIGHT/2)):
        print(Fore.WHITE + Back.BLACK + "          ".center(config.WIDTH))
    
def level_cleared_display(level):
    for _ in range(int(config.HEIGHT/2)):
        print(Fore.WHITE + Back.BLACK + "          ".center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "YOU CLEARED LEVEL {}!!!".format(level).center(config.WIDTH))
    print(Fore.WHITE + Back.BLACK + "Score : {}".format(config.SCORE).center(config.WIDTH))
    for _ in range(int(config.HEIGHT/2)):
        print(Fore.WHITE + Back.BLACK + "          ".center(config.WIDTH))
    time.sleep(2)