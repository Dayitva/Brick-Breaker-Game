import tty
import sys
import termios
import atexit
import os
from select import select

class KeyInput:
    def __init__(self):
        self.fedvar = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fedvar)
        self.new_settings = termios.tcgetattr(self.fedvar)
        
        self.new_settings[3] = (self.new_settings[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fedvar, termios.TCSADRAIN, self.old_settings)
        
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        termios.tcsetattr(self.fedvar, termios.TCSAFLUSH, self.old_settings)
            
    def getch(self):
        return sys.stdin.read(1)
    
    def kbhit(self):
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []
    
    def flush(self):
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)