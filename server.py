#!/usr/bin/python

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
	{"request": "GAMESTART"}
	{"request": "TURNSTART"}
	{"request": "EVENT", "event": "event_num"}
	RECEIVE:	
	{"request": "UPDATE", "player_num": player_num, "location": location}
	{"request": "ACTION", "player_num": player_num, "powerup": powerup}
	{"request": "TURNEND", "player_num:" player_num}
	{"request": "QUIT", "player_num": player_num}
"""

# GLOBALS
PLAYER_LIST = []
PLAYER_COUNT = 0
PLAYER_IDS = 1
GAME_START = False
MAX_PLAYERS_TO_START = 1

# TWISTED NETWORKING
class ServerProtocol(protocol.Protocol):
	def connectionMade(self):
		global PLAYER_LIST, PLAYER_COUNT, PLAYER_IDS, GAME_START, MAX_PLAYERS_TO_START
		# Decline connections if we are over the maximum
		if PLAYER_COUNT == MAX_PLAYERS_TO_START:
			log.msg("Declined a player because full!")
			self.transport.write(json.dumps({"request": "FULL"}))
		else:
			log.msg("Player has connected!")
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
				# Start game if player cap met
				if PLAYER_COUNT == MAX_PLAYERS_TO_START:
					GAME_START = True
					response = json.dumps({"request": "GAMESTART",
						"player_num": PLAYER_IDS})
				PLAYER_IDS   += 1
				self.transport.write(response)

	def dataReceived(self, data):
		log.msg("Data recieved from client: %s" % data)
		self.processResponse(data)

	def connectionLost(self, reason):
		global PLAYER_COUNT, PLAYER_IDS
		log.msg("{}".format(reason))
		PLAYER_IDS -= 1
		PLAYER_COUNT -= 1

	# HELPER FUNCTIONS
	def processResponse(self, data):
		decoded_data = json.loads(data)			
		request = decoded_data["request"]
		log.msg("REQUEST: %s" % request)

		response = {	"ACTION": 	self.handleAction,
		    		"TURNEND": 	self.handleNextPlayer,
		    		"UPDATE": 	self.handleUpdate,
		    		"QUIT": 	self.handleQuit
		   }[request](decoded_data)

		return response

	def handleUpdate(self, decoded_data):
		global PLAYER_LIST
		player_num = decoded_data["player_num"]
		for players in PLAYER_LIST:
			if player_num == players.m_id:	
				players.m_location = decoded_data["location"]
				log.msg("PLAYER: %d LOCATION: %d" % (player_num, players.m_location))

	def handleAction(decoded_data):
		global PLAYER_LIST

	def handleNextPlayer(self, decoded_data):
		next_player = decoded_data["player_num"]
		if next_player == MAX_PLAYERS_TO_START:
			next_player = 1
		else:
			next_player = next_player + 1
		log.msg("NEXT PLAYER: %d" % next_player)
		# Get the specific next player and send them TURNSTART
		send_to = self.factory.clients[next_player-1]
		send_to.transport.write(json.dumps({"request": "TURNSTART"}))

	def handleQuit(decoded_data):	
		global PLAYER_LIST
		delete_player = decoded_data["player_num"]
		for players in PLAYER_LIST:
			if delete_player == players.m_id:
				log.msg("QUIT %d" % delete_player)
				PLAYER_LIST.remove(players)


class ServerFactory(protocol.Factory):
	protocol = ServerProtocol

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
	log.startLogging(sys.stdout)
	m_factory = ServerFactory()
	m_factory.clients = []

	reactor.listenTCP(PORT, m_factory, interface=HOST)
	log.msg("Starting server.")	
	reactor.run()
	log.msg("Closing server.")

if __name__ == "__main__":
	main()
