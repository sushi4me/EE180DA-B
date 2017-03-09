#!/usr/bin/python
#**************************************
# Module: Globals.py
#
# Description: 
#
# Version: 
# 
# Revisions:
#**************************************
#----------------------------
# Module Imports
#----------------------------
from enum import IntEnum

#----------------------------
# Globals
#----------------------------
global INDEX

#----------------------------
# Helper Functions
#----------------------------
def start():
	global INDEX
	INDEX = 1
	return INDEX

def inc():
	global INDEX
	INDEX += 1
	return INDEX
#----------------------------
# Object Types
#----------------------------
class items(IntEnum):
    HEALTH = start()
    POISON = inc() 
    SHIELD = inc()
    WEAPON = inc()
    
#----------------------------
# Player Actions
#----------------------------
class actions(IntEnum):
    ATTACK      = start()
    DEFEND      = inc()
    PICKUP_ITEM = inc()
    USE_ITEM    = inc()

#----------------------------
# OLED Buttons
#----------------------------
class buttons(IntEnum):
    A	= start()
    B	= inc()
    S	= inc()
    U	= inc()
    D	= inc()
    L	= inc()
    R	= inc()

#----------------------------
# OLED Orientation
#----------------------------
class orientation(IntEnum):
    NORTH   = start()
    SOUTH   = inc()
    EAST    = inc()
    WEST    = inc()
