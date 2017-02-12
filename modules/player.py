#!/usr/bin/python

class Player:
<<<<<<< HEAD
	m_client = None;
	m_location = None;
	m_player_num = None;
	m_status = 0;

	def setClient(self, client):
		m_client = client

	def setLocation(self, location):
		m_location = location

	def setPlayerNum(self, player_num):
		m_player_num = player_num

	def setStatus(self, status):
		m_status = status

	def getClient(self):
		return self.m_client

	def getLocation(self):
		return self.m_location

	def getPlayerNum(self):
		return self.m_player_num

	def getStatus(self):        
		return self.status
=======
    team = 0
    position = 0


    def __init__(self, team):
        self.team = team
    
    def setTeam(self):
        return team

    def getTeam(self):
        return team

    def setPosition(self, pos):
        self.position = pos

    def getPosition(self)
        return pos
>>>>>>> 080680c866ad75b2ac7164e4d4098e05a55ccddc
