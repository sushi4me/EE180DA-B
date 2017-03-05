#!/usr/bin/python
#******************************************************************************
# Module: Globals.py
#
# Description: 
#
# Version: 
# 
# Revisions:
#******************************************************************************
#----------------------------
# Globals
#----------------------------
ENUM_SIZE = 0
#----------------------------
# Helper Functions
#----------------------------
def start():
	global ENUM_SIZE
	ENUM_SIZE = 0
	return ENUM_SIZE

def inc():
	global ENUM_SIZE
	ENUM_SIZE += 1
	return ENUM_SIZE
#----------------------------
# Object Types
#----------------------------
global 	HEALTH, POISON, SHIELD, WEAPON, END_OBJECTS
HEALTH = start()
POISON = inc()
SHIELD = inc()
WEAPON = inc()
END_OBJECTS = ENUM_SIZE

#----------------------------
# Player States
#----------------------------
global isDEAD, isALIVE, END_STATES
isDEAD = start()
isALIVE = inc()
END_STATES = ENUM_SIZE

#----------------------------
# Player Actions
#----------------------------
global ATTACK, DEFEND, PICKUP_ITEM, USE_ITEM, END_ACTIONS
ATTACK = start()
DEFEND = inc()
PICKUP_ITEM = inc()
USE_ITEM = inc()
END_ACTIONS = ENUM_SIZE

