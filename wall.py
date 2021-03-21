from gameitems import *

class Wall(GameItems):
    def __init__(self, x, y):
        GameItems.__init__(self, x, y, "#", Back.CYAN, Fore.CYAN)