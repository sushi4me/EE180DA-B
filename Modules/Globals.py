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
# Modules
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
    A		= start()
    B		= inc()
    SELECT	= inc()
    UP		= inc()
    DOWN	= inc()
    LEFT	= inc()
    RIGHT	= inc()

