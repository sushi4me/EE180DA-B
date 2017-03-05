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
    def __init__(self, numPlayers):
    	# Instantiate all the players
        players = []
        for i in range(1, numPlayers + 1):
        	players.append(Player(i))

	def displayGame(self):

#    def move(self):

#    def cleanUp(self):
