# Brick Breaker Game
An arcade, terminal-based game written in Python. Only dependency needed is `colorama`.

## Instructions to run the game
* `python3 main.py`

## Controls
* `A` to move left
* `D` to move right
* `Q` to quit
* `S` to skip level
* `Space` to release ball

## Game Details
* The game has 3 levels with the last level being the boss level.
### Brick info
* `GREEN` Bricks are Level 1 (Lowest Strength)
* `BLUE` Bricks are Level 2(Medium Strength)
* `RED` Bricks are Level 3 (Highest Strength)
* `WHITE` Bricks are Level 4 (Unbreakable)
* `YELLOW` Bricks are Exploding Bricks

### Player Info
* The Player has 3 lives.
* Score is incremented by 10 points each time the ball hits a brick of level 3 or below.