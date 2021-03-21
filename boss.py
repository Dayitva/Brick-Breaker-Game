from gameitems import *

boss = [ 
        list("         ___          "),
        list("     ___/   \___      "),
        list("    /   '---'   \     "),
        list("   /_____________\    ")
        ]

shape = """     
      ___          
  ___/   \___     
 /   '---'   \     
/_____________\     
"""
 
class Boss(GameItems):
    def __init__(self, x, y):
        self.health = 100
        GameItems.__init__(self, x, y, "b", Back.BLACK, Fore.WHITE)