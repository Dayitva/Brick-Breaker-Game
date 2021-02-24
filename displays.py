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

def bottom_display():
    print(Fore.WHITE + Back.RED + "                       ".center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "Lives : {} | Score : {} | Time : {:.2f}".format(config.LIVES, config.SCORE, time.time() - config.START_TIME).center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "                       ".center(config.WIDTH))
    
def lives_over_display():
    print(Fore.WHITE + Back.RED + "          ".center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "LIVES OVER!!!".center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "Score : {}".format(config.SCORE).center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "          ".center(config.WIDTH))
    
def quit_display():
    print(Fore.WHITE + Back.RED + "          ".center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "You quit the game".center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "Score : {}".format(config.SCORE).center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "          ".center(config.WIDTH))
    
def win_display():
    print(Fore.WHITE + Back.RED + "          ".center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "YOU WON!!!".center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "Score : {}".format(config.SCORE).center(config.WIDTH))
    print(Fore.WHITE + Back.RED + "          ".center(config.WIDTH))