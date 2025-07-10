import player.player
from tree.mct import MCT
from random import random,randint
import copy

class MonteCarloPlayer(player.Player):
    def __init__(self): 
        super().__init__()
        self.virtual = False
        self.nextDecision = None

    # TODO: include raising in state space
    # for now, random
    def raising(self, raising = None):
        """
        Function for getting random input
        :returns: TODO

        """
        #return randint(1, self.money - self.debt) if self.money > self.debt else 0.0 
        return randint(1, 1 + int((self.money - self.debt)/3)) if self.money > self.debt else 0.0 

    def getNextDecision(self): 
        return self.nextDecision
    
    def virtualMode(self): 
        super().virtualMode()
        # reset
        self.nextDecision = None

    def options(self, game):
        if self.virtual: 
            # the next time we need to take a decision
            self.nextDecision = game.copy()
            return super().options()
        else: 
            monteTree = MCT(game, self, numIters=1000)
            action = monteTree.solve()
            return self.runAction(action)
