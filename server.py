#!/usr/bin/python

from collections	import deque
from Modules.Game	import Game
from Modules.Player	import Player
#from Modules.GetIP      import getIP
from optparse		import OptionParser
from random		import randint
from threading		import Thread
from time		import sleep, gmtime, strftime
from twisted.internet	import reactor, protocol, task
from twisted.python	import log

import datetime
import fcntl
import json
import os
import socket
import struct
import subprocess			
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
	("request": "NEWPLAYER", "location": location)
	{"request": "TURNEND", "player_num:" player_num}
	{"request": "UPDATE", "player_num": player_num, "location": location}

"""

# GLOBALS

# FUNCTION
class GameProtocol():
	def __init__(self):
		maxPlayers = 1
		self.game = Game(maxPlayers)
		log.msg("FLAG LOCATION: %d" % self.game.flagLocation)
		self.game.flagLocation = 6
                

	# CALLED BY SERVER CODE TO PROCESS JSON
	def processJSON(self, decoded):
		global m_factory

		#log.msg("%s" % decoded)
		request = decoded["request"]

		# Use the request field to execute corresponding function.
		# If the player can perform a new action, add it here:
		response = {	"ACTION":	self.handleAction,
				"DISCONNECTED": self.handleDisconnect, # not used?
				"NEWPLAYER": 	self.handleNewPlayer,
				"ROLL":		self.handleRoll,
				"TURNEND": 	self.handleTurnEnd,
				"UPDATE":	self.handleUpdate
			   }[request](decoded)

	# HANDLER FUNCTIONS
	def handleAction(self, decoded):
		# TO DO
		pass

	def handleDisconnect(self, decoded):
		log.msg("PLAYER DISCONNECTED")

	def handleNewPlayer(self, decoded):
		# Reject players when the server is full
		if self.game.numPlayers != self.game.MAX_PLAYERS:
			location = decoded["location"]
			self.game.addPlayer(location)

			# Return to the player a player_num for identification
			log.msg("NEW PLAYER %d AT %d" % (self.game.numPlayers, location))
			writeToClient(self.game.numPlayers - 1, 
				{"request": "NEWPLAYER", "player_num": self.game.numPlayers})

			# If we have enough players we can start the game!
			if self.game.numPlayers == self.game.MAX_PLAYERS:
				log.msg("STARTING GAME")
				writeToClient(0, {"request": "TURNSTART"})

		return

	def handleTurnEnd(self, decoded):
		player_num = decoded["player_num"]
		roll = decoded["roll"]
		(location, msg) = self.game.runTurn(player_num - 1, roll)
		if self.game.anyWinner() is not None:
			for player in self.game.players:
				writeToClient(player.m_id, {"request": "WINNER", "player_num": player_num})
		else:
			writeToClient(player_num - 1, {"request": "DISPLAY", "msg": msg, "location": location})
			next_player = decoded["player_num"] + 1
			writeToClient(next_player % self.game.MAX_PLAYERS, {"request": "TURNSTART"})

		return

	def handleRoll(self, decoded):
		player_num = decoded["player_num"]
		roll = decoded["roll"]
		(location, msg) = self.game.runTurn(player_num - 1, roll)
		if self.game.anyWinner() is not None:
			writeToClient()
		else:
			writeToClient(player_num - 1, {"request": "DISPLAY", "msg": msg, "location": location})

	def handleUpdate(self, decoded):
		# TO DO
		pass

# TWISTED NETWORKING
class ServerProtocol(protocol.Protocol):
	def __init__(self):
		self.gameprotocol = GameProtocol()

	def connectionMade(self):
		log.msg("CLIENT CONNECTED")
		self.factory.clients.append(self)

	def dataReceived(self, data):
		# Load JSON to decode
		log.msg("%s", data)
		decoded = json.loads(data)
		# Create new thread to handle request
		detect_thread = Thread(target=self.gameprotocol.processJSON, 
			args=(decoded, ))
		detect_thread.start()

	def connectionLost(self, reason):
		log.msg("CLIENT LOST; STOPPING GAME")
		reactor.stop()

class ServerFactory(protocol.Factory):
	protocol = ServerProtocol

def writeToClient(client, msg):
	global m_factory

	m_factory.clients[client].transport.write(json.dumps(msg))
	log.msg("WRITING TO CLIENT: %s" % msg)

def getIP(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15]))[20:24])

# MAIN
def main():
	global m_factory

	# Defaults
	HOST = 'localhost'
	PORT = 8080

	# Default IP grab
	ip_address = getIP('wlp4s0')
	exe = "/home/nathan/Desktop/EE 180DA-B/Modules/uploadServerIP.sh"
	subprocess.call([exe, ip_address])
	with open('ipaddress.txt') as fd:
		HOST = fd.readline().strip("\n")

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
	parser.add_option("-p", "--players",
		dest="players",
		default=4,
		help="Initialize with specific number of players(default=4).")

	options, args = parser.parse_args(sys.argv[1:])

	if options.looping is not None:
		LOOPING = options.looping

	if options.specific_host is not None:
		HOST = options.specific_host

	if options.players is not None:
		PLAYERS = options.players

	# Logging
	print "Server IP Address: %s\n" % HOST
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
