import config
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[" " for j in range(self.cols)] for i in range(self.rows)]

    def print_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] != " ":
                    print(self.grid[i][j].fgcolor + self.grid[i][j].bgcolor + self.grid[i][j].shape, end="")
                else:
                    print(self.grid[i][j], end="")
            print()
            
    def check_game_over(self):
        game_over = True
        
        for i in range(self.rows):
            for j in range(self.cols):
                if type(self.grid[i][j]) == Brick:
                    if self.grid[i][j].level < 4:
                        game_over = False
                        
        return game_over


class GameItems:
    def __init__(self, x, y, shape, bgcolor, fgcolor):
        self.x = x
        self.y = y
        self.shape = shape
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor

    def update_coords(self, x, y):
        self.x = x
        self.y = y


class Wall(GameItems):
    def __init__(self, x, y):
        GameItems.__init__(self, x, y, "#", Back.YELLOW, Fore.YELLOW)


class Ball(GameItems):
    def __init__(self, x, y, position):
        if int((position - int(config.PADDLE_LENGTH/2))) > 0:
            self.x_velocity = 1
        elif int((position - int(config.PADDLE_LENGTH/2))) < 0:
            self.x_velocity = -1
        else:
            self.x_velocity = 0

        # self.x_velocity = position - int(config.PADDLE_LENGTH/2)
        self.y_velocity = 1
        self.on_paddle = True

        GameItems.__init__(self, x, y, "O", Back.BLACK, Fore.WHITE)

    def update_velocity(self, x, y):
        self.x_velocity = x
        self.y_velocity = y


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


class Brick(GameItems):
    BGCOLORS = {1: Back.GREEN, 2: Back.BLUE,
        3: Back.RED, 4: Back.WHITE, 5: Back.YELLOW}
    FGCOLORS = {1: Fore.GREEN, 2: Fore.BLUE,
        3: Fore.RED, 4: Fore.WHITE, 5: Fore.YELLOW}

    def __init__(self, x, y, level):
        self.level = level
        GameItems.__init__(self, x, y, "b", Brick.BGCOLORS[level], Brick.FGCOLORS[level])

    def hit(self):
        if self.level > 1 and self.level < 4:
            self.level -= 1
            self.bgcolor = Brick.BGCOLORS[self.level]
            self.fgcolor = Brick.FGCOLORS[self.level]
        
            config.SCORE += 10


class PowerUp(GameItems):
    def __init__(self, x, y, shape):
        self.hiddenGrid = ""
        GameItems.__init__(self, x, y, shape, Back.MAGENTA, Fore.WHITE)

    def update_hiddenGrid(self, hiddenGrid):
        self.hiddenGrid = hiddenGrid