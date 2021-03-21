from gameitems import *

class Bomb(GameItems):
    def __init__(self, x, y):
        self.hiddenGrid = ""
        GameItems.__init__(self, x, y, "B", Back.RED, Fore.RED)

    def update_hiddenGrid(self, hiddenGrid):
        self.hiddenGrid = hiddenGrid