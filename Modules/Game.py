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

        self.flagLocation = self.randomFlagLocation()

    def randomFlagLocation(self):
        while True:
            count = 0 # count how many players are at flag location 

            flagLocation = random.randint(0, self.numLocations-1)
            
            for player in self.players:
                if player.m_location == flagLocation:
                    count += 1

            # No players at flagLocation, ok to break
            if count == 0:
                break

        return flagLocation

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

    def monstrBattle(self, player):
        monsterHP = 25

        hpAmt = 5

        while player.isAlive() and monsterHP > 0:
            playerDmg = random.randint(0, 1) * hpAmt
            player.changeHP(playerDmg)

            monsterHP -= random.randint(0, 1) * hpAmt

        if player.isAlive():
            return "You battled... and won!"
        else:
            return "You battled... and lost!"
            
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

            playerMsg = "You lost {0} HP!".format(hpAmt)

        elif event == GameEvent.GAINHEALTH:
            player.changeHP(hpAmt)

            playerMsg = "You gained {0} HP!".format(hpAmt)

        elif event == GameEvent.MONSTRFGHT:
            playerMsg = self.monstrBattle(player)

        elif event == GameEvent.ITEMPICKUP:
            playerMsg = "Item acquired!"

        else:
            playerMsg = "Your turn was a little boring..."

        return (newLocation, playerMsg)
