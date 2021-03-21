from gameitems import *

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