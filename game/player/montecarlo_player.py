import player.player
from tree.mct import MCT
from random import random,randint
import copy

class MonteCarloPlayer(player.Player):
    def __init__(self): 
        super().__init__()
        
    def getLegalActions(self): 
        allActions = [i for i in range(1, 6)]

        if self.bet == -1: 
            # you can only go all-in or fold
            allActions = [4, 5]
        elif self.debt:
            # cannot check 
            allActions = allActions[1:]
        
        return allActions

    # TODO: include raising in state space
    # for now, random
    def raising(self, raising = None):
        """
        Function for getting random input
        :returns: TODO

        """
        #return randint(1, self.money - self.debt) if self.money > self.debt else 0.0 
        return randint(1, 1 + int((self.money - self.debt)/3)) if self.money > self.debt else 0.0 
    
    def runAction(self, action):
        options = {1: self.checkBet ,
                    2: self.callBet , 
                    3: self.raiseBet , 
                    4: self.foldBet , 
                    5: self.allin,
                    }
        
        return options[action]()

    def options(self, game):
        monteTree = MCT(game, self.name, numIters=1000)
        action = monteTree.solve()

        # run an action on the real game
        return self.runAction(action)
