from gameitems import *
from brick import *

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