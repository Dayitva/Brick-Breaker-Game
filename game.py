import signal
import random
from objects import *
from displays import lives_over_display, quit_display
from alarmexception import AlarmException
from getch import _getChUnix as getChar

GameBoard = Board(config.HEIGHT, config.WIDTH)

GamePaddle = Paddle(int(config.WIDTH/2),
                    int(config.WIDTH/2) + config.PADDLE_LENGTH)

where_on_paddle = random.randint(0, config.PADDLE_LENGTH - 1)
GameBall = Ball(int(config.WIDTH/2) + where_on_paddle, int(config.HEIGHT) - 3, where_on_paddle)

GamePowerups = []

def place_items_on_board():
    #Placing Wall
    for i in range(config.HEIGHT):
        for j in range(config.WIDTH):
            if i == 0 or j == 0 or i == config.HEIGHT - 1 or j == config.WIDTH - 1:
                GameWall = Wall(i, j)
                GameBoard.grid[i][j] = GameWall
                    
    # Placing Normal Bricks
    for i in range(int(config.HEIGHT/10), int(config.HEIGHT/2), 4):
        for j in range(int(config.WIDTH/10), int(config.WIDTH/1.1), config.BRICK_LENGTH + 2):
            level = random.randint(1, 4)
            my_brick = Brick(i, j, level)
            for k in range(j, j + config.BRICK_LENGTH):
                GameBoard.grid[i][k] = my_brick
    
    #Placing Exploding Bricks
    for j in range(int(config.WIDTH/3), int(config.WIDTH/1.5), config.BRICK_LENGTH):
        for k in range(j, j + config.BRICK_LENGTH):
            GameBoard.grid[i+1][k] = Brick(i, j, 5)

    # Placing Paddle
    for i in range(int(config.WIDTH/2), int(config.WIDTH/2) + config.PADDLE_LENGTH):
        GameBoard.grid[int(config.HEIGHT) - 2][i] = GamePaddle

    # Placing Ball
    GameBoard.grid[int(config.HEIGHT) - 3][int(config.WIDTH/2) + where_on_paddle] = GameBall

def take_input():
    def alarmhandler(signum, frame):
        raise AlarmException

    def user_input(timeout=0.1):
        signal.signal(signal.SIGALRM, alarmhandler)
        signal.setitimer(signal.ITIMER_REAL, timeout)
        try:
            text = getChar()()
            signal.alarm(0)
            return text
        except AlarmException:
            pass
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return ""

    INPUT_CHAR = user_input()
    char = INPUT_CHAR

    curr_start_x = GamePaddle.start
    curr_end_x = GamePaddle.end

    if char == 'q':
        print("\033[0;0H")
        print("\033[?25h")
        quit_display()
        quit()
        
    elif char == " ":
        GameBall.on_paddle = False

    elif char == 'd':
        if curr_end_x + 3 < config.WIDTH - 2:
            for i in range(1, 4):
                GameBoard.grid[int(config.HEIGHT) - 2][curr_start_x + i - 1] = " "
                GameBoard.grid[int(config.HEIGHT) - 2][curr_end_x + i] = GamePaddle
            
            GamePaddle.update_coords(curr_start_x + 3, curr_end_x + 3)
            
            if GameBall.on_paddle:
                GameBoard.grid[GameBall.y][GameBall.x] = " "
                GameBoard.grid[int(config.HEIGHT) - 3][GameBall.x + 3] = GameBall
                GameBall.update_coords(GameBall.x + 3, int(config.HEIGHT) - 3)
        else:
            GamePaddle.update_coords(curr_start_x, curr_end_x)

    elif char == 'a':
        if curr_start_x - 3 > 0:
            for i in range(1, 4):
                GameBoard.grid[int(config.HEIGHT) - 2][curr_start_x - i + 1] = " "
                GameBoard.grid[int(config.HEIGHT) - 2][curr_end_x - i] = GamePaddle
        
            GamePaddle.update_coords(curr_start_x - 3, curr_end_x - 3)
            
            if GameBall.on_paddle:
                GameBoard.grid[GameBall.y][GameBall.x] = " "
                GameBoard.grid[int(config.HEIGHT) - 3][GameBall.x - 3] = GameBall
                GameBall.update_coords(GameBall.x - 3, int(config.HEIGHT) - 3)
        else:
            GamePaddle.update_coords(curr_start_x, curr_end_x)

def ball_dynamics():
    if not GameBall.on_paddle:
        
        GameBoard.grid[GameBall.y][GameBall.x] = " "
            
        if type(GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity]) is Paddle:
            #Ball hits left-side of the Paddle
            if (GameBall.x + GameBall.x_velocity - GamePaddle.start) < int(config.PADDLE_LENGTH/2):
                #Ball coming from left-side
                if GameBall.x_velocity > 0:
                    GameBall.update_velocity(-1 * GameBall.x_velocity, -1 * GameBall.y_velocity)
                
                #Ball coming straight-down
                elif GameBall.x_velocity == 0:
                    GameBall.update_velocity(-1, -1 * GameBall.y_velocity)
                
                #Ball coming from right-side
                else:
                    GameBall.update_velocity(GameBall.x_velocity, -1 * GameBall.y_velocity)
            
            #Ball hits the right-side of the Paddle
            elif (GameBall.x + GameBall.x_velocity - GamePaddle.start) > int(config.PADDLE_LENGTH/2):
                #Ball coming from left-side
                if GameBall.x_velocity > 0:
                    GameBall.update_velocity(GameBall.x_velocity, -1 * GameBall.y_velocity)
                
                #Ball coming straight-down
                elif GameBall.x_velocity == 0:
                    GameBall.update_velocity(1, -1 * GameBall.y_velocity)
                
                #Ball coming from right-side
                else:
                    GameBall.update_velocity(-1 * GameBall.x_velocity, -1 * GameBall.y_velocity)
            
            #Ball hits the center of the Paddle
            else:
                GameBall.update_velocity(0, -1 * GameBall.y_velocity)
        
        elif type(GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity]) is Wall:
            #Ball hits the Top Wall
            if GameBall.y - GameBall.y_velocity == 0:
                GameBall.update_velocity(GameBall.x_velocity, -1 * GameBall.y_velocity)
            
            #Ball hits the Side Walls
            elif GameBall.x + GameBall.x_velocity == 0 or GameBall.x + GameBall.x_velocity == config.WIDTH - 1:
                GameBall.update_velocity(-1 * GameBall.x_velocity, GameBall.y_velocity)
                
            #Ball hits the Bottom Wall
            else:
                if config.LIVES == 0:
                    print("\033[0;0H")
                    print("\033[?25h")
                    lives_over_display()
                    quit()
                    
                else:
                    config.LIVES -= 1
                
                where_on_paddle = random.randint(1, config.PADDLE_LENGTH - 2)
                GameBall.update_coords(GamePaddle.start + where_on_paddle, int(config.HEIGHT) - 4)
                GameBall.on_paddle = True
                
        elif type(GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity]) is Brick:
            #Remove brick completely if it is Level 1
            if GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity].level == 1:
                prevGrid = GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity]
                
                for i in range(config.BRICK_LENGTH):
                    if GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity - i] == prevGrid:
                        GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity - i] = " "
                    if GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity + i] == prevGrid:
                        GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity + i] = " "

                config.SCORE += 10
                
            #Explode brick if it is Level 5
            elif GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity].level == 5:
                for j in range(int(config.WIDTH/3), int(config.WIDTH/1.5)+1):
                    GameBoard.grid[GameBall.y - GameBall.y_velocity][j] = " "
                    GameBoard.grid[GameBall.y - GameBall.y_velocity - 1][j] = " "
                    
                config.SCORE += 60
            
            #Decrease Level of Brick otherwise
            else:
                GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity].hit()
                
                if GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity].level < 4:
                    got_powerup = random.randint(0, 1)
                    
                    if got_powerup:
                        choose_powerup = random.choice(["E", "S"])
                        powerup = PowerUp(GameBall.x + GameBall.x_velocity, GameBall.y - GameBall.y_velocity, choose_powerup)
                        powerup.update_hiddenGrid(GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity])
                        GamePowerups.append(powerup)
                    
            GameBall.update_velocity(GameBall.x_velocity, -1 * GameBall.y_velocity)
        
        #Update Board with the new position of the ball
        GameBoard.grid[GameBall.y - GameBall.y_velocity][GameBall.x + GameBall.x_velocity] = GameBall
        GameBall.update_coords(GameBall.x + GameBall.x_velocity, GameBall.y - GameBall.y_velocity)

def activate_powerup(powerup):
    # if powerup.shape == "G":
    #     GameBall.on_paddle = True
    
    if powerup.shape == "E":
        GameBoard.grid[int(config.HEIGHT) - 2][GamePaddle.start - 1] = GamePaddle
        GameBoard.grid[int(config.HEIGHT) - 2][GamePaddle.end + 1] = GamePaddle
        GamePaddle.update_coords(GamePaddle.start - 1, GamePaddle.end + 1)
        
    elif powerup.shape == "S":
        if config.PADDLE_LENGTH > 3:
            config.PADDLE_LENGTH -= 2
            GameBoard.grid[int(config.HEIGHT) - 2][GamePaddle.start] = " "
            GameBoard.grid[int(config.HEIGHT) - 2][GamePaddle.end] = " "
            GamePaddle.update_coords(GamePaddle.start + 1, GamePaddle.end - 1)

def powerup_dynamics():
    for powerup in GamePowerups:
        #Move PowerUp down
        if powerup.y < config.HEIGHT - 1:
            GameBoard.grid[powerup.y][powerup.x] = powerup.hiddenGrid
            nextGrid = GameBoard.grid[powerup.y+1][powerup.x]
            if GameBoard.grid[powerup.y+1][powerup.x] == GameBall:
                nextGrid = ' '
            GameBoard.grid[powerup.y+1][powerup.x] = powerup
            powerup.update_hiddenGrid(nextGrid)
            powerup.update_coords(powerup.x, powerup.y+1)
        
        #Activate PowerUp if it hits the Paddle
        if powerup.y == config.HEIGHT - 2 and powerup.x >= GamePaddle.start and powerup.x <= GamePaddle.end:
            activate_powerup(powerup)
            GamePowerups.remove(powerup)