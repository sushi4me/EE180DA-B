#!/usr/bin/python

from collections	import deque
from Modules.Game       import Game
from Modules.Player	import Player
from optparse 		import OptionParser
from threading		import Thread
from twisted.internet 	import reactor, protocol, task
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
JSON_REQUESTS = deque()

# FUNCTION
class Game():
	def detect(self):
		global JSON_REQUESTS, m_factory
		if len(JSON_REQUESTS) > 0:
			decoded = JSON_REQUESTS.popleft()
			print "%s" % decoded
			writeToClient(0, decoded)

# TWISTED NETWORKING
class ServerProtocol(protocol.Protocol):
        def __init__(self):
        	self.gameObj = Game()
            	log.msg("ServerProtocol constructor called.")

	def connectionMade(self):
	    	log.msg("Connection made.")
	    	self.factory.clients.append(self)

	def dataReceived(self, data):
		global JSON_REQUESTS, LOOPING
		log.msg("You got data!")
		decoded = json.loads(data)
		JSON_REQUESTS.append(decoded)
		detect_thread = Thread(target=self.gameObj.detect)
		detect_thread.start()

	def connectionLost(self, reason):
		log.msg("Connection lost.")

def writeToClient(client, msg):
	global m_factory
	m_factory.clients[client].transport.write(json.dumps(msg))
	log.msg("Wrote to a client.")

class ServerFactory(protocol.Factory):
	protocol = ServerProtocol

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

	options, args = parser.parse_args(sys.argv[1:])

	if options.looping is not None:
		LOOPING = options.looping

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
