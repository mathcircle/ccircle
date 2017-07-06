
import worlds
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
        cat.smellsPizza() -> Bool
            True iff the cat is right in front of the pizza (and is facing it)

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

    NOTE: You can only call cat.walk() ONCE per call to moveTowardPizza!!
'''

class Solution:
    def __init__(self):
        # If you want to keep track of any variables, you can initialize them here using self.var = value
        self.was_wall_on_right_last_frame = False
        pass

    # Choose your level here: 'worlds.easy()', 'worlds.medium()', or 'worlds.hard()'!
    def getLevel(self):
        return worlds.hard()

    # Smaller pause time = faster simulation
    def getPauseTime(self):
        return 0.01

    def wall_on_right(self, cat):
        cat.turnRight()
        wall_on_right = cat.isBlocked()
        cat.turnLeft()

        return wall_on_right

    """ Solution assulmes two things:
            1) Cat always starts beside a wall.
            2) Pizza exists beside a wall.
    """
    def moveTowardPizza(self, cat):
        # Follow the right wall.
        is_wall_on_right = self.wall_on_right(cat)

        if not is_wall_on_right and self.was_wall_on_right_last_frame:
            cat.turnRight()
            cat.walk()

        if is_wall_on_right:
            if not cat.isBlocked():
                cat.walk()
            else:
                cat.turnLeft()

        self.was_wall_on_right_last_frame = is_wall_on_right

