from gameitems import *

class PowerUp(GameItems):
    def __init__(self, x, y, shape, x_vel, y_vel):
        self.hiddenGrid = ""
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.go_up = 4
        GameItems.__init__(self, x, y, shape, Back.MAGENTA, Fore.WHITE)

    def update_hiddenGrid(self, hiddenGrid):
        self.hiddenGrid = hiddenGrid