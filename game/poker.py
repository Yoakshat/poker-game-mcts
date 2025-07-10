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
        self.phase = ""
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
    
    def findPlayer(self, player): 
        for p in self.players: 
            if(p == player): 
                return p
            
    def getLegalActions(self, playerName): 
        myPlayer = self.findPlayer(playerName)
        return myPlayer.getLegalActions()
    
    # friendly for different players
    def options(self, player): 
        if isinstance(player, MonteCarloPlayer): 
            # pass game instance in
            return player.options(game=self)
        else: 
            return player.options()

    def resumeRound(self, montePlayer): 
        alreadyPlayed = True

        players = self.players[:]
        # play out rest of player's turns
        for index, p in enumerate(players[:]):
            # check if equals by name
            if(p == montePlayer): 
                alreadyPlayed = False
            elif not alreadyPlayed: 
                # play turn
                self.playTurn(index, p, players)

        self.players = players[:]

        # this round is finished
        # next decision we need to make is the player's next turn
        if (self.isAllIn() or self.controlDeposit()): 
            pass 
        else: 
            self.round()

    # record the number of virtual turns the player has taken
    def playTurn(self, index, player, players): 
        record = self.options(player)
                
        index = (index+1) % len(self.players) 
        self.players[index].bet = record[0]
        if record[1] == -1:
            players.remove(player)
        else:
            self.dealer.playerControl.pot += record[1]

        
    def round(self):
        """
        Goes through all players until every player gave same ammount to the pot
        :returns: TODO
        """
        # multiple turns in a round
        # return player, game after first turn

        while True:
            players = self.players[:]
            for index,player in enumerate(players[:]):
                self.playTurn(index, player, players)
            
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
        self.phase = phase
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
    
    def playOut(self, player):
        # resume round from after the player's turn
        self.resumeRound(player)

        # rest of game should continue like before
        if self.phase == "Preflop": 
            # do both 2 cases
            self.flop()
            self.turn()
        elif self.phase == "Flop": 
            self.turn()
    
    def makeSimPlayers(self):
        # make them all random players
        for p in self.players: 
            p.virtualMode()

    def flop(self): 
        if self.isAllIn():
            #allin on flop
            return self.dealer.cardOnTable("All-flop")
        else:
            #Flop
            self.startPhase("Flop")

    def turn(self): 
        if self.isAllIn():
            #allin on turn
            return self.dealer.cardOnTable("All-turn")
        else:
            #Turn
            self.startPhase("Turn")

    def eachRound(self):
        """TODO: Docstring for function.

        :returns: TODO

        """

        self.dealer.playerControl.ante(self.rounds)
        #Preflop
        self.startPhase("Preflop")
        self.flop()
        self.turn()

