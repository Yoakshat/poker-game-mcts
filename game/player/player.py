"""
File:player.py
Author:dave
Github:https://github.com/davidus27
Description:Player and variations of bots.
"""
from random import random, randint
from os import path as p
from sys import path,exit
ui_package = p.abspath("..") + "/ui"
path.append(ui_package)
from ui.cli import optionsInput, raising,allInOrFold

class Player(object):
    def __init__(self, name = "Player", money = 500.0):
        self.name = name
        self.money = money
        self.handValue = 0.0
        self.hand = []
        self.deposit = 0.0 #how much money player spent in one game
        self.bet = 0.0 #how much money is needed for one player to stay in game
        #bet - deposit is debt
        self.virtual = False

    def getLegalActions(self): 
        allActions = [i for i in range(1, 6)]

        if self.bet == -1: 
            # you can only go all-in or fold
            allActions = [4, 5]
        elif self.debt:
            # cannot check 
            allActions = allActions[1:]
        
        return allActions
    
    def virtualMode(self): 
        self.virtual = True

    @property
    def debt(self):
        """
        Creates value of debt needed in calculations 
        :returns: TODO

        """
        return self.bet - self.deposit
    
    def __eq__(self, other): 
        return self.name == other.name
    

    def clearDebt(self):
        """
        Clears deposit and bet on each game
        :returns: TODO

        """
        self.bet = 0.0
        self.deposit = 0.0
        return self

    def callBet(self):
        """
        Action for player to call a bet on table

        :returns: (bet, debt)

        """
        if not self.debt:
            return self.checkBet()
     
        elif self.debt >= self.money:
            return self.allin()
    
        elif self.debt < self.money:
           self.money -= self.bet - self.deposit
           previousDebt = self.debt
           self.deposit = self.bet
           print("{} call".format(self.name))
           return (self.bet,previousDebt)

    def raising(self):
        """
        Function for getting input
        :returns: TODO

        """
        return raising(1, self.money-self.debt)


    def raiseBet(self, raised = None):
       """
       Method for raising bets
       :returns: (bet, how much player sent to pot now)
       """
       while True:
            if raised == None:
                raised = self.raising()
            if raised == 0.0:
                return self.callBet()
            
            elif raised >= self.money-self.debt:
                return self.allin()
            
            else:
                self.money -= raised + self.debt
                bet = self.bet
                debt = self.debt
                self.bet += raised
                self.deposit = self.bet
                print("{} raised bet:{} ".format(self.name,raised))
                return (self.bet,debt + raised)
                #  problem with reraising. Fix it somehow!:  <05-09-19, dave> # 

    def checkBet(self):
        """
        Checks only if difference between deposit and bet is zero
        
        :returns: True/False based on if you can check or not
        """
        if self.debt:
            print("Cannot perform check.", self.name)
            return False
        else:
            print("{} check".format(self.name))
            return (self.bet,0)

    def foldBet(self):
       """
       :returns: self

       """
       print("{} fold.".format(self.name))
       return (self.bet,-1)

    def allin(self):
       """
       Gives all money to the pot

       :currentBet: Money on pot
       :returns: currentBet with all player's money

       """
       #currentBet += self.money
       print("{} all in!".format(self.name))
       self.deposit += self.money
       self.bet = -1
       #self.deposit = -1
       money = self.money
       self.money = 0
       return (-1,money)

    def quit(self):
        print("Exiting program. Hope you will come back again.")
        exit()

    def runAction(self, action):
        options = {1: self.checkBet ,
                    2: self.callBet , 
                    3: self.raiseBet , 
                    4: self.foldBet , 
                    5: self.allin,
                    }
        
        return options[action]()
    
    def options(self):
        if self.virtual: 
            legal = self.getLegalActions()
            action = legal[randint(0, len(legal)-1)]
            return self.runAction(action)

        '''
        options = { 0: self.quit,
                    1: self.checkBet ,
                    2: self.callBet , 
                    3: self.raiseBet , 
                    4: self.foldBet , 
                    5: self.allin,
                    }
        
        while True:
            if self.bet == -1:
                action = allInOrFold()
            else:
                action = optionsInput()
            choosed = options[action]()
            if choosed:
                return choosed
            else:
                continue
        '''
