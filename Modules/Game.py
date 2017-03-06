B#!/usr/bin/python
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
from Map import Map
import sys
#----------------------------
# Globals
#----------------------------


#----------------------------
# Game Class
#----------------------------
class Game:
    MAX_PLAYERS = 4

    def __init__(self, numPlayers):
        self.players    = []
        self.numPlayers = 0

    def addPlayer(self):
        playerID = self.numPlayers
        self.players.append(Player(playerID))

        self.numPlayers += 1

    def removePlayer(self, playerID):
        del self.players[playerID]

        self.numPlayers -= 1

#    def move(self):

#    def cleanUp(self):
