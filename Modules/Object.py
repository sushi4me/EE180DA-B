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
    
    m_type = 0
    m_value = 0
    m_life = 0

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
            self.m_life = 1
        elif item == items.POISON:
            self.m_value = self.m_strength * MAX_POISON
            self.m_life = 1
        elif item == items.SWORD:
            self.m_value = self.m_strength * MAX_SWORD
        elif item == items.SHIELD:
            self.m_value = self.m_strength * MAX_SHIELD


    def getItemType (self):
        return self.m_type



