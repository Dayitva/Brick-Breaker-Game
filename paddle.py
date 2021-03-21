from gameitems import *

class Paddle(GameItems):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.shape = "p"
        self.lives = 3
        self.score = 0
        self.bgcolor = Back.MAGENTA
        self.fgcolor = Fore.MAGENTA
        # GameItems.__init__(self, x, y)

    def update_coords(self, start, end):
        self.start = start
        self.end = end

    def reduceLife(self):
        self.lives -= 1
