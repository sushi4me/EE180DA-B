#!/usr/bin/python

from Modules.JSONsocket import Server			# Not applicable
from Modules.Player	import Player
from optparse 		import OptionParser
from twisted.internet 	import reactor, protocol
from twisted.python	import log

import json
import os			
import sys			
import time

"""
NOTES:
	SEND:
	{"request": "NEWPLAYER", "player_num": player_count}
	RECEIVE:	
	{"request": "UPDATE", "player_num": player_num, "location": location}
	{"request": "ACTION", "player_num": player_num, "powerup": powerup}
	{"request": "QUIT", "player_num": player_num}
"""

# GLOBALS
PLAYER_LIST = []
PLAYER_COUNT = 0
PLAYER_IDS = 1
GAME_START = False

# TWISTED NETWORKING
class ServerProtocol(protocol.Protocol):
	def connectionMade(self):
		global PLAYER_LIST, PLAYER_COUNT, PLAYER_IDS, GAME_START
		# Decline connections if we are over the maximum
		if PLAYER_COUNT == 2:
			print "DECLINED!"
			self.transport.write(json.dumps({"request": "FULL"}))
		else:
			print "Player has connected!"
			self.factory.clients.append(self)
			response = json.dumps({"request": "NEWPLAYER", 
				"player_num": PLAYER_IDS})
			p = Player(PLAYER_IDS)
			# If the player is already in the list, then pass
			if p in PLAYER_LIST:
				pass
			else:
				PLAYER_LIST.append(p)			
				PLAYER_COUNT += 1
				PLAYER_IDS   += 1
				self.transport.write(response)
			# Allow processing in dataReceived			
			if PLAYER_COUNT == 1:
				GAME_START = True

	def dataReceived(self, data):
		global GAME_START
		if GAME_START:
			processResponse(data)

	def connectionLost(self, reason):
		global PLAYER_COUNT, PLAYER_IDS
		print "Player disconnected - {}".format(reason)
		PLAYER_IDS -= 1
		PLAYER_COUNT -= 1

class ServerFactory(protocol.Factory):
	protocol = ServerProtocol

# HELPER FUNCTIONS
def handleUpdate(decoded_data):
	global PLAYER_LIST
	player_num = decoded_data["player_num"]
	for players in PLAYER_LIST:
		if player_num == players.m_player_num:	
			players.m_location = decoded_data["location"]
			print "I've updated his location to %d!" % players.m_location

def handleAction(decoded_data):
	global PLAYER_LIST

def handleQuit(decoded_data):	
	global PLAYER_LIST

def processResponse(data):
	decoded_data = json.loads(data)			
	request = decoded_data["request"]
	print request
	response = {"UPDATE" : handleUpdate,
		    "ACTION" : handleAction,
		    "QUIT" : handleQuit
		   }[request](decoded_data)

# MAIN
def main():
	# Defaults
	HOST = 'localhost'
	PORT = 8080

	# Option parser
	version_msg = "server.py--1.12.17"
	usage_msg = """%prog [OPTIONS] ...
	Hosts server on HOST & waits for clients to connect."""
	
	# Option parser
	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-s", "--specific", 
		action="store",
		dest="specific_host", 
		help="Hosts onto specific HOST.")
	parser.add_option("-v", "--verbose", 
		action="store_true",
		dest="verbose", 
		default=False, 
		help="Prints debugging statements on console.")

	options, args = parser.parse_args(sys.argv[1:])

	if options.specific_host is not None:
		HOST = options.specific_host

	# Start
	m_factory = ServerFactory()
	m_factory.clients = []

	reactor.listenTCP(PORT, m_factory, interface=HOST)
	print "Starting reactor."	
	reactor.run()
	print "Closing server."

if __name__ == "__main__":
	main()