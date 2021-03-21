import config
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

class GameItems:
    def __init__(self, x, y, shape, bgcolor=Back.WHITE, fgcolor=Fore.WHITE):
        self.x = x
        self.y = y
        self.shape = shape
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor

    def update_coords(self, x, y):
        self.x = x
        self.y = y
