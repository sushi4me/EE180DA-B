#!/usr/bin/python
#******************************************************************************
# Module: Game.py
#
# Description: Contains modules that will be used for keeping track of a game
#              of Capture the Flag.  These modules include the status of
#              the players, the Flag, and keeping score.
#
# Version: 1.01 created December 15, 2016 by Edison Vallejo
# 
# Revisions:
#******************************************************************************

#----------------------------
# Modules
#----------------------------
from Globals import *
from Player  import Player
from Object  import Object
from enum    import IntEnum

import sys
import random

class GameEvent(IntEnum):
    LOSEHEALTH = 1
    GAINHEALTH = 2
    MONSTRFGHT = 3
    ITEMPICKUP = 4

#----------------------------
# Game Class
#----------------------------
class Game:
    def __init__(self, maxPlayers):
        # Players metadata
        self.players     = []
        self.numPlayers  = 0

        self.MAX_PLAYERS = maxPlayers
   
        # Number of possible player locations
        self.numLocations = 61

        # Dictionary for battle results
        self.actDict = {
        	(1, 1): ("\n\nDRAW!", 5),
        	(1, 2): ("\n\nYou lost!", 10),
        	(1, 3): ("\n\nYou won!", 0),
        	(2, 1): ("\n\nYou won!", 0),
        	(2, 2): ("\n\nDRAW!", 5),
        	(2, 3): ("\n\nYou lost!", 10),
        	(3, 1): ("\n\nYou lost!", 10),
        	(3, 2): ("\n\nYou won!", 0),
        	(3, 3): ("\n\nDRAW!", 5)
        }

    def randomFlagLocation(self):
        while True:
            count = 0 # count how many players are at flag location 

            self.flagLocation = random.randint(0, self.numLocations-1)
            
            for player in self.players:
                if player.m_location == self.flagLocation:
                    count += 1

            # No players at flagLocation, ok to break
            if count == 0:
                break

    def addPlayer(self, playerLocation):
        playerID = self.numPlayers
        self.players.append(Player(playerID, playerLocation))

        self.numPlayers += 1

    def removePlayer(self, playerID):
        del self.players[playerID]

        self.numPlayers -= 1

    def move(self, player, numSpaces):
        currentLocation = player.m_location

        newLocation = (currentLocation + numSpaces) % self.numLocations
        player.setLocation(newLocation)

        return newLocation

    def monstrBattle(self, player, player_act, monster_act):
        (msg, hpAmt) = self.actDict[(player_act, monster_act)]
        player.changeHP(-hpAmt)
        return msg

            
    def randomEvent(self):
        return random.choice([event for event in GameEvent])

    def anyWinner(self):
        for player in self.players:
            if player.m_location == self.flagLocation:
                return player.m_id

        return None

    def runTurn(self, playerID, numSpaces):
        player = self.players[playerID]

        newLocation = self.move(player, numSpaces)
        
        event = self.randomEvent()

        hpAmt = 10

        if event == GameEvent.LOSEHEALTH:
            player.changeHP(-hpAmt)

            playerMsg = "\nYou lost  {0} HP!".format(hpAmt)

        elif event == GameEvent.GAINHEALTH:
            player.changeHP(hpAmt)

            playerMsg = "\nYou gained {0} HP!".format(hpAmt)

        elif event == GameEvent.MONSTRFGHT:
            playerMsg = "You run into a monster! Prepare for battle!"


        elif event == GameEvent.ITEMPICKUP:
            playerMsg = "\n   Item\n   acquired!"

        else:
            playerMsg = "Your turn was a little boring..."

        return (newLocation, playerMsg, int(event))
