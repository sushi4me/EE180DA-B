#!/usr/bin/python

from Modules.Game		import Game
from Modules.Player		import Player
from optparse 			import OptionParser
from threading			import Thread
from twisted.internet 		import reactor, protocol
from twisted.internet.task	import LoopingCall
from twisted.python		import log

import json
import os			
import sys			
import time

"""
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

TO DO: 
	* Allow the Game class to receive information from the reactor thread.
		1. Start Game's "checking" function in LoopingCall.
		2. If we detect something in LoopingCall, send back to reactor.

	* Upon data receive send decoded JSON to Game class.
"""

# GLOBALS
GAME_START = False

class Game():
	global VERBOSE

	def __init__(self, host="localhost", port=8080):
		self.m_factory = ServerFactory()
		self.m_factory.clients = []
		self.m_host = host
		self.m_port = port

	def run(self):
		twisted_thread = Thread(target=self.runTwisted)
		twisted_thread.start()
		
		twisted_thread.join()
		if VERBOSE:
			log.msg("End of game.")

	def runTwisted(self):
		reactor.listenTCP(self.m_port, self.m_factory, interface=self.m_host)
		if VERBOSE:
			log.msg("Running reactor.")
		reactor.run()

# TWISTED NETWORKING
class ServerProtocol(protocol.Protocol):
        def __init__(self):
            MAX_PLAYERS = 1
            self.game = Game(MAX_PLAYERS)

	def connectionMade(self):
	    if self.game.numPlayers < self.game.MAX_PLAYERS:
		log.msg("Player has connected!")
		self.factory.clients.append(self)
		response = json.dumps({"request": "NEWPLAYER", "player_num": self.game.numPlayers})

		self.game.addPlayer()
		
                # Start game if we have max num players connected.
                if self.game.numPlayers == self.game.MAX_PLAYERS:
                    GAME_START = True
                    response = json.dumps({"request": "GAMESTART", "player_num": self.game.numPlayers})
                        
		self.transport.write(response)

            else: # Decline connections when at max capacity
		log.msg("Declined a player because full!")
	        self.transport.write(json.dumps({"request": "FULL"}))

	def dataReceived(self, data):
		log.msg("Data recieved from client: %s" % data)
		self.processResponse(data)

	def connectionLost(self, reason):
		log.msg("{}".format(reason))
                self.game.removePlayer(self.game.numPlayers-1)

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
		player_num = decoded_data["player_num"]
		
                for player in self.game.players:
			if player_num == player.m_id:	
				player.m_location = decoded_data["location"]
				log.msg("PLAYER: %d LOCATION: %d" % (player_num, player.m_location))

	def handleAction(decoded_data):
            count = 0

	def handleNextPlayer(self, decoded_data):
		next_player = decoded_data["player_num"]
		if next_player == self.game.MAX_PLAYERS:
		    next_player = 1
		else:
		    next_player = next_player + 1
		log.msg("NEXT PLAYER: %d" % next_player)
		# Get the specific next player and send them TURNSTART
		send_to = self.factory.clients[next_player-1]
		send_to.transport.write(json.dumps({"request": "TURNSTART"}))

	def handleQuit(decoded_data):	
		delete_player = decoded_data["player_num"]
		for player in self.game.players:
			if delete_player == player.m_id:
				log.msg("QUIT %d" % delete_player)
				self.game.removePlayer(delete_player)

class ServerFactory(protocol.Factory):
	protocol = ServerProtocol

# MAIN
def main():
	global VERBOSE

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

	if options.verbose is not None:
		VERBOSE = options.verbose

	if VERBOSE:
		log.startLogging(sys.stdout)

	# Start reactor
	m_factory = ServerFactory()
	m_factory.clients = []

	reactor.listenTCP(PORT, m_factory, interface=HOST)
	if VERBOSE:
		log.msg("Running reactor.")
	reactor.run()

if __name__ == "__main__":
	main()
