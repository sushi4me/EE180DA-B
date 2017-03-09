#!/usr/bin/python
#******************************************************************************
# Module: object_.py
#
# Description: 
#              
#              
#
# Version: 1.01 created 
# 
# Revisions:
#******************************************************************************
#----------------------------
# Modules
#----------------------------
from Globals import items, actions
import random

#----------------------------
# Globals
#----------------------------
LOW_STRENGTH = .3
MID_STRENGTH = .6
HIGH_STRENGTH = 1

STRENGTH = [LOW_STRENGTH, MID_STRENGTH, HIGH_STRENGTH]

MAX_HEALTH = 25
MAX_POISON = -20
MAX_SWORD = -20
MAX_SHIELD = 15

#----------------------------
# Object Class
#----------------------------
class Object:
    
    #------------------------
    # Member Variables
    #------------------------

    m_type = 0  # tupe of object: sword, shield, etc.
    m_value = 0 # value is the amount of life object will give/take
    m_hp = 0  # num of times the object can be used

    #------------------------
    # Class Constructor
    #------------------------

    def __init__(self, item):
        
        # initialize type of object
        self.m_type = item
        
        # initialize object strength
        length = len(STRENGTH)
        i = random.randint(0, length-1)
        self.m_strength = STRENGTH[i]

        # initialize object value and life
        if item == items.HEALTH:
            self.m_value = self.m_strength * MAX_HEALTH 
            self.m_hp = 1
        elif item == items.POISON:
            self.m_value = self.m_strength * MAX_POISON
            self.m_hp = 1
        elif item == items.SWORD:
            self.m_value = self.m_strength * MAX_SWORD
        elif item == items.SHIELD:
            self.m_value = self.m_strength * MAX_SHIELD

        if item == items.SWORD or item == items.SHIELD:
            if self.m_strength == LOW_STRENGTH:
                self.m_hp = 6
            elif self.m_strength == MID_STRENGTH:
                self.m_hp = 4
            elif self.m_strength == HIGH_STRENGTH:
                self.m_hp = 2

    #------------------------
    # Class Functions
    #------------------------

    def getObjType(self):
        return self.m_type

    def getObjValue(self):
        return self.m_value

    def getObjLife(self):
        return self.m_hp

    def getObjStrength(self):
        return self.m_strength

    def isAlive(self):
        return self.m_life > 0 



