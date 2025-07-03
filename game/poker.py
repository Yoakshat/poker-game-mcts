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
    
    def findPlayer(self, playerName): 
        for player in self.players: 
            if(player.name == playerName): 
                return player
            
    def getLegalActions(self, playerName): 
        myPlayer = self.findPlayer(playerName)
        return myPlayer.getLegalActions()
    
    def options(self, player): 
        if isinstance(player, MonteCarloPlayer): 
            # pass game instance in
            return player.options(game=self)
        else: 
            return player.options()
        
    def resumeRound(self, player, action): 
        return self.round(montePlayer=player, action=action, resume=True)

    def round(self, montePlayer=None, action=None, resume=False):
        """
        Goes through all players until every player gave same ammount to the pot
        :returns: TODO
        """

        didIPlay = False

        while True:
            players = self.players[:]
            for index,player in enumerate(players[:]):
                record = None

                if resume: 
                    if(not didIPlay): 
                       # check if it's my turn
                        if(montePlayer == player): 
                            didIPlay = True
                            record = player.runAction(action)
                            # set it to random for rest of the time 
                            player.changeToRandom() 
                        else: 
                            # skip
                            continue
                    else: 
                        # if i did play, run like usual 
                        record = self.options(player)
                else: 
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
    
    # requires the player,
    # and the action as an integer
    def virtualGame(self, player, action):
        start = player.money

        # takes action, and afterwards sets policy to random, 
        # and finishes that round
        playerAfter, gameAfter = self.resumeRound(player, action)
        gameAfter = gameAfter.copy()
        playerAfter = playerAfter.copy()
        # reset to original policy
        playerAfter.reset()

        # rest of game should continue like before
        if self.phase == "Preflop": 
            # do both 2 cases
            self.flop()
            self.turn()
        elif self.phase == "Flop": 
            self.turn()

        return (player.money - start), gameAfter, playerAfter


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

