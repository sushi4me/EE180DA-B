#**************************************
# Module: Player
# Description:
# 
#**************************************
from Globals import *

#------------------------
#  Player Class
#------------------------
class Player:
    #------------------------
    # Member Variables
    #------------------------
    m_id = 0
    m_location = 0
    m_hp = 100
    m_items = []

    def __init__(self, player_id):
        self.m_id = player_id

    def changeHP(self, amt):
        self.m_hp += amt

    def setHP(self, amt):
        self.m_hp = amt

    def obtainItem(self, item):
        self.m_items.append(item)

    def setLocation(self, pos):
        self.m_location = pos

    def isAlive(self):
        return self.m_hp > 0
