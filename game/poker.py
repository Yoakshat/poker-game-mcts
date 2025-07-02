"""
File: poker.py
Author: dave
Github: https://github.com/davidus27
Description: Game is the main Object implementing all the necessary tools for playing. Game is created in function main()
"""
import ui.cli as ui
import dealer
from player.player import Player
from player import MonteCarloPlayer
from random import randint
import copy


class Game(object):
    """
    Creates players based on inputs on call.
    """
    def __init__(self):
        self.rounds = 1
        self.players = []
        self.dealer = dealer.Dealer()

    def createPlayers(self):
        name = ui.nameQuest()
        numPlayers = ui.numQuest()
        money = 500
        difficulty = ui.diffQuest()

        return self.dealer.playerControl.createPlayers(name,numPlayers, money, difficulty)

    def controlDeposit(self):
        """
        checks if there are any differences
        :returns: TODO

        """
        deposit = self.players[0].deposit #reference
        for player in self.players[1:]:
            if player.deposit == deposit:
                continue
            else:
                return False
        return True
    
    def findPlayer(self, playerName): 
        for player in self.players: 
            if(player.name == playerName): 
                return player
            
    def getLegalActions(self, playerName): 
        myPlayer = self.findPlayer(playerName)
        return myPlayer.getLegalActions()
    
    # returns (the total return of taking this action till the end of the game), state after taking action
    # TODO: also in a virtual round, turn off printing (done in background)

    # have game control taking action for the player we want

    def virtualRound(self, playerName, action): 
        iters = 0
        returnForAction = 0
        stateAfterAction = None

        myPlayer = self.findPlayer(playerName)

        while True:
            players = self.players[:]
            startMoney = myPlayer.money

            # runs through each player's turn
            for index,player in enumerate(players[:]):
                record = None
                if(player == myPlayer): 
                    if(iters == 0): 
                        # select the action
                        record = player.runAction(action)
                    else: 
                        # choose a random action (e.g. random policy)
                        # first get legal actions
                        legal = player.getLegalActions()
                        rand = legal[randint(0, len(legal)-1)]
                        record = player.runAction(rand)
                else: 
                    record = self.options(player)
                index = (index+1) % len(self.players) 
                self.players[index].bet = record[0]
                if record[1] == -1:
                    players.remove(player)
                else:
                    self.dealer.playerControl.pot += record[1]

            # turn-through: all living players have raised, called, folded, or checked
            # after a turn-through, get immediate state for the next node
            if(iters == 0): 
                # get this version of the game
                stateAfterAction = self.copy()
                iters += 1


            # return is how much i gained or lost in my pot
            returnForAction += (myPlayer.money - startMoney)
            self.players = players[:] 
            
            if self.isAllIn():
                break
            elif self.controlDeposit():
                break
            else:
                continue

        return returnForAction, stateAfterAction
    
    def options(self, player): 
        if isinstance(player, MonteCarloPlayer): 
            # pass game instance in
            return player.options(game=self)
        else: 
            return player.options()

    def round(self):
        """
        Goes through all players until every player gave same ammount to the pot
        :returns: TODO

        """
        while True:
            players = self.players[:]
            for index,player in enumerate(players[:]):
                record = self.options(player)
                
                index = (index+1) % len(self.players) 
                self.players[index].bet = record[0]
                if record[1] == -1:
                    players.remove(player)
                else:
                    self.dealer.playerControl.pot += record[1]
            
            self.players = players[:] 
            
            if self.isAllIn():
                break
            elif self.controlDeposit():
                break
            else:
                continue
        return self
    
    def copy(self): 
        return copy.deepcopy(self)

    def printSituation(self, table=False):
        """
        Prints out whole situation in the game.
        :returns: TODO

        """
        if type(self.players[0]) == Player:
            ui.info(self.dealer.playerControl.players[0].name, self.dealer.playerControl.players[0].money)
            print("Your cards:")
            ui.print_cards(self.dealer.playerControl.players[0].hand)
            print()
            if table:
                print("Community cards:")
                ui.print_cards(table)
                print()
        return self

    def allCards(self):
        """
        Prints hands of all players
        """
        for player in self.players:
            print(player.name, "")
            ui.print_cards(player.hand)
        return self

    def showdown(self):
        """
        Ending of the round
        :returns: TODO

        """
        print("Community cards:")
        ui.print_cards(self.dealer.cardControl.tableCards)
        self.allCards()
        
        winners = self.dealer.chooseWinner(self.players)
        x = [winner.name for winner in winners]
        ui.roundWinners(x)
        for w in winners:
            ui.print_hand_value(w.handValue)
        self.dealer.playerControl.givePot(winners)
        return self

    def startPhase(self, phase):
        """
        Goes through one phase part of easy game
        :returns: TODO

        """
        print("\n\t\t{}\n".format(phase))
        self.printSituation(self.dealer.cardControl.tableCards)
        self.round()
        self.dealer.cardOnTable(phase)
        
    def isAllIn(self):
        """
        Checking all players if someone is allin or not
        :returns: TODO

        """
        for player in self.players:
            if player.bet == -1:
                return True
        return False



    def eachRound(self):
        """TODO: Docstring for function.

        :returns: TODO

        """
        self.dealer.playerControl.ante(self.rounds)
        #Preflop
        self.startPhase("Preflop")
        if self.isAllIn():
            #allin on flop
            return self.dealer.cardOnTable("All-flop")
        else:
            #Flop
            self.startPhase("Flop")
            
        if self.isAllIn():
            #allin on turn
            return self.dealer.cardOnTable("All-turn")
        else:
            #Turn
            self.startPhase("Turn")

