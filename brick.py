from gameitems import *

class Brick(GameItems):
    BGCOLORS = {1: Back.GREEN, 2: Back.BLUE,
        3: Back.RED, 4: Back.WHITE, 5: Back.YELLOW}
    FGCOLORS = {1: Fore.GREEN, 2: Fore.BLUE,
        3: Fore.RED, 4: Fore.WHITE, 5: Fore.YELLOW}

    def __init__(self, x, y, level, type=False):
        self.level = level
        self.rainbowType = type
        GameItems.__init__(self, x, y, "b", Brick.BGCOLORS[level], Brick.FGCOLORS[level])

    def hit(self):
        if self.level > 1 and self.level < 4:
            self.level -= 1
            self.bgcolor = Brick.BGCOLORS[self.level]
            self.fgcolor = Brick.FGCOLORS[self.level]
        
            config.SCORE += 10
            
    def rainbow(self):
        if self.level == 1:
            self.level = 3
            
        else:
            self.level -= 1
        
        self.bgcolor = Brick.BGCOLORS[self.level]
        self.fgcolor = Brick.FGCOLORS[self.level]