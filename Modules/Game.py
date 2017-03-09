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
from Player import Player
from Object import Object

import sys
import random

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

    def addPlayer(self):
        playerID = self.numPlayers
        self.players.append(Player(playerID))

        self.numPlayers += 1

    def removePlayer(self, playerID):
        del self.players[playerID]

        self.numPlayers -= 1

    def move(self, playerID, numSpaces):
        currentLocation = self.players[playerID].m_location

        newLocation = (currentLocation + numSpaces) % self.numLocations
        self.players[playerID].setLocation(newLocation)

        return newLocation

    def randomEvent(self, location):
        return random.choice(['Lose health', 'Gain health', 'Fight!'])
    
#    def cleanUp(self):
