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

#----------------------------
# Game Class
#----------------------------
class Game:
    def __init__(self, maxPlayers):
        # Players
        self.players     = []
        self.numPlayers  = 0

        self.MAX_PLAYERS = maxPlayers
   
        # Number of possible player locations
        self.numLocations = 61

    def addPlayer(self, playerLocation):
        playerID = self.numPlayers
        self.players.append(Player(playerID, playerLocation))

        self.numPlayers += 1

    def removePlayer(self, playerID):
        del self.players[playerID]

        self.numPlayers -= 1

    def move(self, playerID, numSpaces):
        currentLocation = self.players[playerID].m_location

        newLocation = (currentLocation + numSpaces) % self.numLocations
        self.players[playerID].setLocation(newLocation)

        return newLocation

    def battle(self, playerID):
        playerDmg = random.randint(0, 1) * -5

        self.players[playerID].changeHP(playerDmg)
            
    def randomEvent(self):
        return random.choice([GameEvent.LOSEHEALTH, GameEvent.GAINHEALTH, GameEvent.MONSTRFGHT])

    def runTurn(self, playerID, numSpaces):
        newLocation = self.move(playerID, numSpaces)

        event = self.randomEvent()

        if event == GameEvent.LOSEHEALTH:
            self.players[playerID].changeHP(-10)

            playerMsg = "You lost 10 HP!"
        elif event == GameEvent.GAINHEALTH:
            self.players[playerID].changeHP(10)

            playerMsg = "You gained 10 HP!"
        elif event == GameEvent.MONSTRFGHT:
            self.battle(playerID)

            playerMsg = "You slayed! ;)"
        else:
            playerMsg = "Your turn was a little boring..."

        return (newLocation, playerMsg)
