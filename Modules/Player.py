#!/usr/bin/python

class Player:
	m_location = None;
	m_status = 0;
	
	def __init__(self, player_num):
		self.m_player_num = player_num

	def __eq__(self, other):
		return self.m_player_num == other.m_player_num
	
	def __hash__(self):
		return hash(self.m_player_num)

	def setLocation(self, location):
		m_location = location

	def setPlayerNum(self, player_num):
		m_player_num = player_num

	def setStatus(self, status):
		m_status = status

	def getLocation(self):
		return self.m_location

	def getPlayerNum(self):
		return self.m_player_num

	def getStatus(self):        
		return self.status
