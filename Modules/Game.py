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
import player
import object_
import map_
import sys
#----------------------------
# Globals
#----------------------------


#----------------------------
# Game Class
#----------------------------
class Game:
    def init(self, numPlayers, playersTeamNums):
        players = []
        for i, c in enumerate(numPlayers):
            player[i] = Player.Player(c)

#    def displayGame(self):

#    def move(self):

#    def cleanUp(self):
