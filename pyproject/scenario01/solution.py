# Your solution goes in this file!

'''
    GOAL: Fill in the code for 'moveTowardPizza' to ensure that the cat finds the pizza!

    Use the following functions to understand the cat's situation:

        cat.isBlocked() -> Bool
            returns True if the cat is facing a wall or the edge of the maze, False if the coast is clear
        cat.isFacingN() -> Bool
            True iff cat is facing north
        cat.isFacingS() -> Bool
            True iff cat is facing south
        cat.isFacingE() -> Bool
            True iff cat is facing east
        cat.isFacingW() -> Bool
            True iff cat is facing west

        Just a refresher...:

                   /|\
                    |
                  North
                    |
        <-- West --- --- East --->
                    |
                    |
                  South
                    |
                   \|/

    Use the following functions to instruct the cat:

        cat.turnLeft() -> None
            Instructs the cat to turn left / counter-clockwise
        cat.turnRight() -> None
            Instructs the cat to turn right / clockwise
        cat.walk() -> None
            Instructs the cat to walk in the direction it is facing
'''

class Solution:
    def __init__(self):
        # If you want to keep track of any variables, you can initialize them here using self.var = value
        # e.g.
        #   self.moveCount = 0
        pass

    # Choose your level here: 'easy', 'medium', or 'hard'!
    def getLevel(self):
        return 'easy'

    # Smaller pause time = faster simulation
    def getPauseTime(self):
        return 0.5

    # Your solution!
    def moveTowardPizza(self, cat):
        # Wheeeee!
        cat.turnLeft()