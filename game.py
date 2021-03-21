import os
import config
import random
import signal

from alarmexception import AlarmException
from getch import _getChUnix as getChar

from displays import *
from ball import *
from board import *
from bomb import *
from boss import *
from brick import *
from paddle import *
from powerup import *
from wall import *

class Game:
    def __init__(self, level):
        self.level = level
        
        self.GameBoard = Board(config.HEIGHT, config.WIDTH)

        self.GamePaddle = Paddle(int(config.WIDTH/2),
                            int(config.WIDTH/2) + config.PADDLE_LENGTH)

        self.where_on_paddle = random.randint(0, config.PADDLE_LENGTH - 1)
        self.GameBall = Ball(int(config.WIDTH/2) + self.where_on_paddle, int(config.HEIGHT) - 3, self.where_on_paddle)

        self.GamePowerups = []
        self.GameBombs = []
        
        if config.BOSS_LEVEL:
            self.GameBoss = Boss(int(config.WIDTH/2), 2)
        
    def place_items_on_board(self):
        #Placing Wall
        for i in range(config.HEIGHT):
            for j in range(config.WIDTH):
                if i == 0 or j == 0 or i == config.HEIGHT - 1 or j == config.WIDTH - 1:
                    GameWall = Wall(i, j)
                    self.GameBoard.grid[i][j] = GameWall

        # Placing Paddle
        for i in range(int(config.WIDTH/2), int(config.WIDTH/2) + config.PADDLE_LENGTH):
            self.GameBoard.grid[int(config.HEIGHT) - 2][i] = self.GamePaddle

        # Placing Ball
        self.GameBoard.grid[int(config.HEIGHT) - 3][int(config.WIDTH/2) + self.where_on_paddle] = self.GameBall

    def show_level_1(self):
        # Placing Normal Bricks
        for i in range(int(config.HEIGHT/10), int(config.HEIGHT/2), 4):
            for j in range(int(config.WIDTH/10), int(config.WIDTH/1.1), config.BRICK_LENGTH + 2):
                level = random.randint(1, 4)
                my_brick = Brick(i, j, level)
                my_brick.rainbowType = True
                for k in range(j, j + config.BRICK_LENGTH):
                    self.GameBoard.grid[i][k] = my_brick
        
        #Placing Exploding Bricks
        # for j in range(int(config.WIDTH/3), int(config.WIDTH/1.5), config.BRICK_LENGTH):
        #     for k in range(j, j + config.BRICK_LENGTH):
        #         self.GameBoard.grid[i+1][k] = Brick(i, j, 5)
        
        for i in range(int(config.HEIGHT/10), int(config.HEIGHT/2)):
            for j in range(int(config.WIDTH/10) - config.BRICK_LENGTH, int(config.WIDTH/10)):
                self.GameBoard.grid[i][j] = Brick(i, j, 5)

    def show_level_2(self):
        # Placing Normal Bricks
        for i in range(int(config.HEIGHT/10), int(config.HEIGHT/2), 4):
            for j in range(int(config.WIDTH/10), int(config.WIDTH/2), 2*(config.BRICK_LENGTH + 2)):
                level = random.randint(1, 4)
                my_brick = Brick(i, j, level)
                my_brick.rainbowType = True
                for k in range(j, j + config.BRICK_LENGTH):
                    self.GameBoard.grid[i][k] = my_brick
        
        #Placing Exploding Bricks
        # for j in range(int(config.WIDTH/3), int(config.WIDTH/1.5), config.BRICK_LENGTH):
        #     for k in range(j, j + config.BRICK_LENGTH):
        #         self.GameBoard.grid[i+1][k] = Brick(i, j, 5)
        
        for i in range(int(config.HEIGHT/10), int(config.HEIGHT/2)):
            for j in range(int(config.WIDTH/10)-config.BRICK_LENGTH, int(config.WIDTH/10)):
                self.GameBoard.grid[i][j] = Brick(i, j, 5)
        
    def show_boss_level(self):
        for i in range(self.GameBoss.y, self.GameBoss.y + 3):
            for j in range(self.GameBoss.x, self.GameBoss.x + 10):
                self.GameBoard.grid[i][j] = self.GameBoss
        
    
    def take_input(self):
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
            return ''
        INPUT_CHAR = user_input()
        char = INPUT_CHAR
        
        paddle_start_x = self.GamePaddle.start
        paddle_end_x = self.GamePaddle.end
        
        if config.BOSS_LEVEL:
            boss_start_x = self.GameBoss.x
            boss_end_x = self.GameBoss.x + 9

        if char == 'q' or char == "Q":
            print("\033[0;0H")
            print("\033[?25h")
            quit_display()
            quit()
            
        elif char == " ":
            self.GameBall.on_paddle = False
            
        elif char == 's' or char == "S":
            config.CHANGE_LEVEL = True

        elif char == 'd' or char == "D":
            if paddle_end_x + 3 < config.WIDTH - 1:
                for i in range(1, 4):
                    self.GameBoard.grid[int(config.HEIGHT) - 2][paddle_start_x + i - 1] = " "
                    self.GameBoard.grid[int(config.HEIGHT) - 2][paddle_end_x + i] = self.GamePaddle
                    
                    if config.BOSS_LEVEL:
                        for j in range(2, 5):
                            self.GameBoard.grid[j][boss_start_x + i - 1] = " "
                            self.GameBoard.grid[j][boss_end_x + i] = self.GameBoss
                
                self.GamePaddle.update_coords(paddle_start_x + 3, paddle_end_x + 3)
                
                if config.BOSS_LEVEL:
                    self.GameBoss.update_coords(boss_start_x + 3, boss_end_x + 3)
                
                if self.GameBall.on_paddle:
                    self.GameBoard.grid[self.GameBall.y][self.GameBall.x] = " "
                    self.GameBoard.grid[int(config.HEIGHT) - 3][self.GameBall.x + 3] = self.GameBall
                    self.GameBall.update_coords(self.GameBall.x + 3, int(config.HEIGHT) - 3)
            else:
                self.GamePaddle.update_coords(paddle_start_x, paddle_end_x)

        elif char == 'a' or char == "A":
            if paddle_start_x - 3 > 0:
                for i in range(1, 4):
                    self.GameBoard.grid[int(config.HEIGHT) - 2][paddle_end_x - i + 1] = " "
                    self.GameBoard.grid[int(config.HEIGHT) - 2][paddle_start_x - i] = self.GamePaddle
                    
                    if config.BOSS_LEVEL:
                        for j in range(2, 5):
                            self.GameBoard.grid[j][boss_end_x - i + 1] = " "
                            self.GameBoard.grid[j][boss_start_x - i] = self.GameBoss
                
                self.GamePaddle.update_coords(paddle_start_x - 3, paddle_end_x - 3)
                
                if config.BOSS_LEVEL:
                    self.GameBoss.update_coords(boss_start_x - 3, boss_end_x - 3)
                
                if self.GameBall.on_paddle:
                    self.GameBoard.grid[self.GameBall.y][self.GameBall.x] = " "
                    self.GameBoard.grid[int(config.HEIGHT) - 3][self.GameBall.x - 3] = self.GameBall
                    self.GameBall.update_coords(self.GameBall.x - 3, int(config.HEIGHT) - 3)
            else:
                self.GamePaddle.update_coords(paddle_start_x, paddle_end_x)
    
    def ball_dynamics(self):
        if not self.GameBall.on_paddle:
            
            self.GameBoard.grid[self.GameBall.y][self.GameBall.x] = " "
                
            if type(self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity]) is Paddle:
                os.system('afplay sounds/paddle.mp3&')
                #Ball hits left-side of the Paddle
                if (self.GameBall.x + self.GameBall.x_velocity - self.GamePaddle.start) < int(config.PADDLE_LENGTH/2):
                    #Ball coming from left-side
                    if self.GameBall.x_velocity > 0:
                        self.GameBall.update_velocity(-1 * self.GameBall.x_velocity, -1 * self.GameBall.y_velocity)
                    
                    #Ball coming straight-down
                    elif self.GameBall.x_velocity == 0:
                        self.GameBall.update_velocity(-1, -1 * self.GameBall.y_velocity)
                    
                    #Ball coming from right-side
                    else:
                        self.GameBall.update_velocity(self.GameBall.x_velocity, -1 * self.GameBall.y_velocity)
                
                #Ball hits the right-side of the Paddle
                elif (self.GameBall.x + self.GameBall.x_velocity - self.GamePaddle.start) > int(config.PADDLE_LENGTH/2):
                    #Ball coming from left-side
                    if self.GameBall.x_velocity > 0:
                        self.GameBall.update_velocity(self.GameBall.x_velocity, -1 * self.GameBall.y_velocity)
                    
                    #Ball coming straight-down
                    elif self.GameBall.x_velocity == 0:
                        self.GameBall.update_velocity(1, -1 * self.GameBall.y_velocity)
                    
                    #Ball coming from right-side
                    else:
                        self.GameBall.update_velocity(-1 * self.GameBall.x_velocity, -1 * self.GameBall.y_velocity)
                
                #Ball hits the center of the Paddle
                else:
                    self.GameBall.update_velocity(0, -1 * self.GameBall.y_velocity)
            
            elif type(self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity]) is Wall:
                os.system('afplay sounds/wall.mp3&')
                #Ball hits the Top Wall
                if self.GameBall.y - self.GameBall.y_velocity == 0:
                    self.GameBall.update_velocity(self.GameBall.x_velocity, -1 * self.GameBall.y_velocity)
                
                #Ball hits the Side Walls
                elif self.GameBall.x + self.GameBall.x_velocity == 0 or self.GameBall.x + self.GameBall.x_velocity == config.WIDTH - 1:
                    self.GameBall.update_velocity(-1 * self.GameBall.x_velocity, self.GameBall.y_velocity)
                    
                #Ball hits the Bottom Wall
                else:
                    if config.LIVES == 0:
                        print("\033[0;0H")
                        print("\033[?25h")
                        lives_over_display()
                        quit()
                        
                    else:
                        config.LIVES -= 1
                    
                    self.where_on_paddle = random.randint(1, config.PADDLE_LENGTH - 2)
                    self.GameBall.update_coords(self.GamePaddle.start + self.where_on_paddle, int(config.HEIGHT) - 4)
                    self.GameBall.on_paddle = True
                    
            elif type(self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity]) is Brick:
                self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity].rainbowType = False        
                
                #Remove brick completely if it is Level 1
                if self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity].level == 1:
                    os.system('afplay sounds/level1brick.mp3&')
                    prevGrid = self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity]
                    
                    for i in range(config.BRICK_LENGTH):
                        if self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity - i] == prevGrid:
                            self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity - i] = " "
                        if self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity + i] == prevGrid:
                            self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity + i] = " "

                    config.SCORE += 10
                    
                #Explode brick if it is Level 5
                elif self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity].level == 5:
                    os.system('afplay sounds/explodingbrick.mp3&')
                    # for j in range(int(config.WIDTH/3), int(config.WIDTH/1.5)+1):
                    #     self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][j] = " "
                    #     self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity - 1][j] = " "
                    for i in range(int(config.HEIGHT/10), config.HEIGHT - 3):
                        for j in range(int(config.WIDTH/10)-config.BRICK_LENGTH, int(config.WIDTH/10)+config.BRICK_LENGTH):
                            self.GameBoard.grid[i][j] = " "
                    
                    config.SCORE += 60
            
                #Decrease Level of Brick otherwise
                else:
                    self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity].hit()
                    os.system('afplay sounds/hardbrick.mp3&')
                    if self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity].level < 4:
                        got_powerup = random.randint(0, 1)
                        
                        if got_powerup:
                            choose_powerup = random.choice(["E", "S"])
                            powerup = PowerUp(self.GameBall.x + self.GameBall.x_velocity, self.GameBall.y - self.GameBall.y_velocity, choose_powerup, self.GameBall.x_velocity, self.GameBall.y_velocity)
                            powerup.update_hiddenGrid(self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity])
                            self.GamePowerups.append(powerup)
                        
                self.GameBall.update_velocity(self.GameBall.x_velocity, -1 * self.GameBall.y_velocity)
            
            elif type(self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity]) is Boss:
                os.system('afplay sounds/boss.mp3&')
                self.GameBall.update_velocity(self.GameBall.x_velocity, -1 * self.GameBall.y_velocity)
                self.GameBoss.health -= 2
                
            #Update Board with the new position of the ball
            self.GameBoard.grid[self.GameBall.y - self.GameBall.y_velocity][self.GameBall.x + self.GameBall.x_velocity] = self.GameBall
            self.GameBall.update_coords(self.GameBall.x + self.GameBall.x_velocity, self.GameBall.y - self.GameBall.y_velocity)

    def activate_powerup(self, powerup):
        # if powerup.shape == "G":
        #     self.GameBall.on_paddle = True
        
        if powerup.shape == "E":
            self.GameBoard.grid[int(config.HEIGHT) - 2][self.GamePaddle.start - 1] = self.GamePaddle
            self.GameBoard.grid[int(config.HEIGHT) - 2][self.GamePaddle.end + 1] = self.GamePaddle
            self.GamePaddle.update_coords(self.GamePaddle.start - 1, self.GamePaddle.end + 1)
            
        elif powerup.shape == "S":
            if config.PADDLE_LENGTH > 3:
                config.PADDLE_LENGTH -= 2
                self.GameBoard.grid[int(config.HEIGHT) - 2][self.GamePaddle.start] = " "
                self.GameBoard.grid[int(config.HEIGHT) - 2][self.GamePaddle.end] = " "
                self.GamePaddle.update_coords(self.GamePaddle.start + 1, self.GamePaddle.end - 1)

    def powerup_dynamics(self):
        for powerup in self.GamePowerups:
            #Move Powerup in the direction of the ball
            if powerup.y_vel > 0:
                while powerup.go_up > 0:
                    self.GameBoard.grid[powerup.y][powerup.x] = powerup.hiddenGrid
                    nextGrid = self.GameBoard.grid[powerup.y-1][powerup.x + powerup.x_vel]
                    self.GameBoard.grid[powerup.y-1][powerup.x+powerup.x_vel] = powerup
                    powerup.update_hiddenGrid(nextGrid)
                    powerup.update_coords(powerup.x+powerup.x_vel, powerup.y-1)
                    powerup.go_up -= 1
                
            #Move PowerUp down
            if powerup.y < config.HEIGHT - 1:
                self.GameBoard.grid[powerup.y][powerup.x] = powerup.hiddenGrid
                nextGrid = self.GameBoard.grid[powerup.y+1][powerup.x]
                if self.GameBoard.grid[powerup.y+1][powerup.x] == self.GameBall:
                    nextGrid = ' '
                self.GameBoard.grid[powerup.y+1][powerup.x] = powerup
                powerup.update_hiddenGrid(nextGrid)
                powerup.update_coords(powerup.x, powerup.y+1)
            
            #Activate PowerUp if it hits the Paddle
            if powerup.y == config.HEIGHT - 2 and powerup.x >= self.GamePaddle.start and powerup.x <= self.GamePaddle.end:
                self.activate_powerup(powerup)
                self.GamePowerups.remove(powerup)
                
    def move_bricks_down(self):
        time_over = time.time() - config.START_TIME
        config.BRICK_DOWN += 1

        if int(time_over) > 20 and config.BRICK_DOWN%40 == 0:
            for i in range(config.HEIGHT-1, -1, -1):
                for j in range(config.WIDTH-1, -1, -1):
                    if type(self.GameBoard.grid[i][j]) is Brick:
                        if i+1 == config.HEIGHT - 2:
                            # variables.GAME_OVER = True
                            break
                        else:
                            self.GameBoard.grid[i+1][j] = self.GameBoard.grid[i][j]
                            self.GameBoard.grid[i][j] = " "
                            
        for k in range(1, config.WIDTH-1):
            if type(self.GameBoard.grid[config.HEIGHT - 3][k]) is Brick:
                lose_display()
                print("\033[?25h")
                quit()
                
    def bomb_drop(self):
        time_over = time.time() - config.START_TIME
        config.BRICK_DOWN += 1
        
        if int(time_over) != 0 and config.BRICK_DOWN%30 == 0:
            bomb = Bomb(self.GameBoss.y, self.GameBoss.x)
            bomb.update_hiddenGrid(self.GameBoard.grid[self.GameBoss.x][self.GameBoss.y])
            self.GameBombs.append(bomb)
            
            for bomb in self.GameBombs:
                if bomb.y < config.HEIGHT - 1:
                    self.GameBoard.grid[bomb.y][bomb.x] = bomb.hiddenGrid
                    nextGrid = self.GameBoard.grid[bomb.y+1][bomb.x]
                    if self.GameBoard.grid[bomb.y+1][bomb.x] == self.GameBall:
                        nextGrid = ' '
                    self.GameBoard.grid[bomb.y+1][bomb.x] = bomb
                    bomb.update_hiddenGrid(nextGrid)
                    bomb.update_coords(bomb.x, bomb.y+1)
        
                if bomb.y == config.HEIGHT - 2 and bomb.x >= self.GamePaddle.start and bomb.x <= self.GamePaddle.end:                   
                    if config.LIVES == 0:
                        print("\033[0;0H")
                        print("\033[?25h")
                        lives_over_display()
                        quit()
                        
                    else:
                        config.LIVES -= 1
                    
                    self.where_on_paddle = random.randint(1, config.PADDLE_LENGTH - 2)
                    self.GameBall.update_coords(self.GamePaddle.start + self.where_on_paddle, int(config.HEIGHT) - 4)
                    self.GameBall.on_paddle = True
                
    def spawn_defense_1(self):
        for i in range(1, int(config.WIDTH)-1):
            my_brick = Brick(7, i, 1)
            my_brick.rainbowType = False
            self.GameBoard.grid[7][i] = my_brick
        
        config.SPAWN1 = False
            
    def spawn_defense_2(self):
        for i in range(1, int(config.WIDTH)-1):
            my_brick = Brick(8, i, 2)
            my_brick.rainbowType = False
            self.GameBoard.grid[8][i] = my_brick
            
        config.SPAWN2 = False
        
    def play(self):
        self.place_items_on_board()
        
        if self.level == 1:
            self.show_level_1()
            
        elif self.level == 2:
            self.show_level_2()
            
        elif self.level == 3:
            self.show_boss_level()
            config.BOSS_LEVEL = True
            
        while True:
            if config.CHANGE_LEVEL == True:
                config.CHANGE_LEVEL = False
                level_cleared_display(self.level)
                break
            
            self.take_input()
            self.GameBoard.print_board()
            self.ball_dynamics()
            
            if config.BOSS_LEVEL == False:
                self.powerup_dynamics()
                self.move_bricks_down()
            
            # if self.GameBoard.check_game_over():
            #     break
            
            for i in range(int(config.HEIGHT/10), config.HEIGHT - 1):
                if type(self.GameBoard.grid[i][int(config.WIDTH/10)]) is Brick and self.GameBoard.grid[i][int(config.WIDTH/10)].rainbowType == True:
                    self.GameBoard.grid[i][int(config.WIDTH/10)].rainbow()
            
            if config.BOSS_LEVEL:
                # self.bomb_drop()
                
                if self.GameBoss.health < 25 and config.SPAWN1 == True:
                    self.spawn_defense_1()
                elif self.GameBoss.health < 10 and config.SPAWN2 == True:
                    self.spawn_defense_2()
                    
                boss_display(self.GameBoss.health)
            else:
                bottom_display(self.level)
                
            print("\033[0;0H")