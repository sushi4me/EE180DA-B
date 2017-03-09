#!/usr/bin/python

from collections	import deque
#from Modules.Game	import Game
from Modules.Player	import Player
from optparse		import OptionParser
from random		import randint
from threading		import Thread
from twisted.internet	import reactor, protocol, task
from twisted.python	import log

import json
import os			
import sys			
import time

"""
NOTES:
	SEND:
	{"request": "GAMESTART"}
	{"request": "EVENT", "event": "event_num"}
	{"request": "NEWPLAYER", "player_num": player_num}
	{"request": "TURNSTART"}

	RECEIVE:
	{"request": "ACTION", "player_num": player_num, "powerup": powerup}
	{"request": "DISCONNECTED", "player_num": player_num}
	("request": "NEWPLAYER")
	{"request": "TURNEND", "player_num:" player_num}
	{"request": "UPDATE", "player_num": player_num, "location": location}

"""

# GLOBALS

# FUNCTION
class Game():
	global NUMBER_OF_PLAYERS
	global PLAYERS

	PLAYERS = []

	# CALLED BY SERVER CODE TO PROCESS JSON
	def processJSON(self, decoded):
		global m_factory

		log.msg("%s" % decoded)
		request = decoded["request"]

		# Use the request field to execute corresponding function.
		# If the player can perform a new action, add it here:
		response = {	"ACTION":	self.handleAction,
				"DISCONNECTED": self.handleDisconnect,
				"NEWPLAYER": 	self.handleNewPlayer,
				"TURNEND": 	self.handleTurnEnd,
				"UPDATE":	self.handleUpdate
			   }[request](decoded)

	# HANDLER FUNCTIONS
	def handleAction(self, decoded):
		# TO DO
		pass

	def handleDisconnect(self, decoded):
		# TO DO
		pass

	def handleNewPlayer(self, decoded):
		log.msg("A new player has connected!")
		

		return

	def handleTurnEnd(self, decoded):
		# TO DO
		pass

	def handleUpdate(self, decoded):
		# TO DO
		pass

	# HELPER FUNCTIONS
	def rollDice(self, max=6):
		random.seed(time.time())
		return random.randint(0, max)

# TWISTED NETWORKING
class ServerProtocol(protocol.Protocol):
        def __init__(self):
        	self.gameObj = Game()
            	log.msg("ServerProtocol constructor called.")

	def connectionMade(self):
	    	log.msg("Connection made.")
	    	self.factory.clients.append(self)

	def dataReceived(self, data):
		global LOOPING

		log.msg("You got data!")

		decoded = json.loads(data)
		detect_thread = Thread(target=self.gameObj.processJSON, 
			args=(decoded, ))
		detect_thread.start()

	def connectionLost(self, reason):
		log.msg("Connection lost.")

class ServerFactory(protocol.Factory):
	protocol = ServerProtocol

def writeToClient(client, msg):
	global m_factory

	m_factory.clients[client].transport.write(json.dumps(msg))
	log.msg("Wrote to a client.")

# MAIN
def main():
	global LOOPING, m_factory

	# Defaults
	HOST = 'localhost'
	PORT = 8080

	# Option parser
	version_msg = "server.py--3.8.17"
	usage_msg = """%prog [OPTIONS] ...
	Hosts server on HOST & waits for clients to connect."""

	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-l", "--looping", 
		action="store_true",
		dest="looping", 
		default=False, 
		help="Uses LoopingCall.")
	parser.add_option("-s", "--specificHost",
		dest="specific_host",
		default=None,
		help="Connect to a specific hostname other than localhost.")

	options, args = parser.parse_args(sys.argv[1:])

	if options.looping is not None:
		LOOPING = options.looping

	if options.specific_host is not None:
		HOST = options.specific_host

	# Logging
	log.startLogging(sys.stdout)

	# Start
	m_factory = ServerFactory()
	m_factory.clients = []

	# LoopingCall version
	if LOOPING:
		check = task.LoopingCall(gameObj.detect)
		check.start(0)

	reactor.listenTCP(PORT, m_factory, interface=HOST)
	reactor.run()
	# End

if __name__ == "__main__":
	main()
