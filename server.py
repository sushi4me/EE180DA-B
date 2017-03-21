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
import random
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
	{"request": "ACTION", 	"player_num": PLAYER_ID, 	"action": action})
	{"request": "TURNEND", 	"player_num": PLAYER_ID})
	{"request": "ROLL", 	"player_num": PLAYER_ID,	"roll": roll})


"""

# GLOBALS

# FUNCTION
class GameProtocol():
	def __init__(self):
		maxPlayers = 1
		self.game = Game(maxPlayers)
		log.msg("PLAYERS: %d" % self.game.MAX_PLAYERS)

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
		# TO DO: Handle player commands during a turn.
		monster_act = monsterAction()
		player_act = decoded["action"]
		player_num = decoded["player_num"] - 1

		msg = self.game.monstrBattle(self.game.players[player_num], player_act, monster_act)
		writeToClient(player_num, {"request": "RESULT", "msg": msg})
		return

	def handleDisconnect(self, decoded):
		log.msg("PLAYER DISCONNECTED")
		return

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

                                # Generate flag location
                                self.game.randomFlagLocation()

				writeToClient(0, {"request": "TURNSTART"})
		return

	def handleTurnEnd(self, decoded):
		player_num = decoded["player_num"]
		#roll = decoded["roll"]
		#(location, msg, event_num) = self.game.runTurn(player_num - 1, roll)
		if self.game.anyWinner() is not None:
			for player in self.game.players:
				writeToClient(player.m_id, {"request": "WINNER", "player_num": player_num})
		else:
			#writeToClient(player_num - 1, {"request": "DISPLAY", "msg": msg, "location": location, "event": event_num})
			#sleep(1)
			#if event_num == 3:
			#	return
			#else:
			next_player = player_num % self.game.MAX_PLAYERS
			writeToClient(next_player, {"request": "TURNSTART"})
		return

	def handleRoll(self, decoded):
		player_num = decoded["player_num"]
		roll = decoded["roll"]
		(location, msg, event_num) = self.game.runTurn(player_num - 1, roll)
		writeToClient(player_num - 1, {"request": "DISPLAY", "msg": msg, "location": location, "event": event_num})
		return

	def handleUpdate(self, decoded):
		# TO DO: Not yet in use.
		pass

# TWISTED NETWORKING
class ServerProtocol(protocol.Protocol):
	#def __init__(self):
	gameprotocol = GameProtocol()

	def connectionMade(self):
		log.msg("CLIENT CONNECTED")
		self.factory.clients.append(self)

	def dataReceived(self, data):
		# Load JSON to decode
		log.msg(data)
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

# HELPER FUNCTIONS
def writeToClient(client, msg):
	global m_factory

	log.msg("WRITING TO CLIENT {0}: {1}".format(client, msg))
	m_factory.clients[client].transport.getHandle().sendall(json.dumps(msg))
	#m_factory.clients[client].transport.write(json.dumps(msg))

def getIP(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15]))[20:24])

def monsterAction(max=3):
	random.seed()
	return random.randint(1, max)

# MAIN
def main():
	global m_factory

	# Defaults
	HOST = 'localhost'
	PORT = 8080

	# Option parser
	version_msg = "server.py--3.8.17"
	usage_msg = """%prog [OPTIONS] ...
	Hosts server on HOST & waits for clients to connect."""

	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-i", "--iphost",
		action="store_true",
		dest="ip_host",
		default=None,
		help="Automatically use current hostname as server.")
	parser.add_option("-p", "--players",
		dest="players",
		default=4,
		help="Initialize with specific number of players(default=4).")

	options, args = parser.parse_args(sys.argv[1:])

	if options.ip_host is not None:
		# Default IP grab
		ip_address = getIP('wlp4s0')
		exe = "/home/nathan/Desktop/EE 180DA-B/Modules/uploadServerIP.sh"
		subprocess.call([exe, ip_address])
		with open('ipaddress.txt', 'w') as fd:
			HOST = fd.readline().strip("\n")

	# Not in use
	if options.players is not None:
		PLAYERS = options.players

	# Logging
	print "SERVER HOSTNAME: %s\n" % HOST
	log.startLogging(sys.stdout)

	# Start
	m_factory = ServerFactory()
	m_factory.clients = []

	reactor.listenTCP(PORT, m_factory, interface=HOST)
	reactor.run()
	# End

if __name__ == "__main__":
	main()
