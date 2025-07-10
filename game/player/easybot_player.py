import player.player 
from random import random,randint

class EasyBot(player.Player):

    """
    Easy to compete player
    Selects randomly between his options
    """

    def __init__(self):
       """TODO: to be defined1. """
       super().__init__()

    def raising(self, raising = None):
        """
        Function for getting random input
        :returns: TODO

        """
        #return randint(1, self.money - self.debt) if self.money > self.debt else 0.0 
        return randint(1, 1 + int((self.money - self.debt)/3)) if self.money > self.debt else 0.0 

    def checkBet(self):
        """
        Checks only if difference between deposit and bet is zero
        
        :returns: True/False based on if you can check or not
        """
        if self.debt:
            return False
        else:
            print("{} check".format(self.name))
            return (self.bet,0)


    def options(self):
        """
        Gives all options to the player
        :action: input of the player
        :returns: used function

        """
        # Select randomly
        return super().options()
        

