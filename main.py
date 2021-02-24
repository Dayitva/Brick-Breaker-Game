import os
from game import place_items_on_board, take_input, ball_dynamics, powerup_dynamics, GameBoard
from displays import bottom_display, win_display

os.system('clear')
print("\033[0;0H")
place_items_on_board()
print("\033[?25l")

while True:
    print("\033[0;0H")
    take_input()
    ball_dynamics()
    powerup_dynamics()
    
    if GameBoard.check_game_over() == True:
        print("\033[0;0H")
        print("\033[?25h")
        win_display()
        quit()
        
    GameBoard.print_board()
    bottom_display()