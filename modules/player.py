#!/usr/bin/python

class Player:
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
