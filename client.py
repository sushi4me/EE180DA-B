#!/usr/bin/python

"""
NOTES:
	SEND:
	{"request": "ACTION", "player_num": player_num, "powerup": powerup}
	{"request": "DISCONNECTED", "player_num": player_num}
	("request": "NEWPLAYER")
	{"request": "TURNEND", "player_num:" player_num}
	{"request": "UPDATE", "player_num": player_num, "location": location}

	RECEIVE:
	{"request": "NEWPLAYER", "player_num": player_num}
	{"request": "TURNSTART"}
"""

from datetime			import datetime
#from Modules.Buzzer		import Buzzer
#from Modules.DOF 		import DOFsensor
from Modules.OLED		import OLED
from optparse			import OptionParser
from random			import randint
from twisted.internet		import reactor, protocol, defer
#from twisted.internet.task	import LoopingCall
from twisted.python		import log
from location.location 		import location

import json
import mraa
import os
import random
import sys
import time

# GLOBALS
global oled 
oled = OLED()
global PLAYER_ID

# TWISTED NETWORKING
class ClientProtocol(protocol.Protocol):	
	def connectionMade(self):
                log.msg("Connected to server.")
		self.factory.server = self
                
                log.msg("Determining start location...")
                startLocation = location()
                log.msg("Done!")

                self.transport.write(json.dumps({"request": "NEWPLAYER", "location": startLocation}))

	def dataReceived(self, data):
		decoded = json.loads(data)
		log.msg("%s" % data)
		
		processJSON(decoded)


class ClientFactory(protocol.ClientFactory):
	protocol = ClientProtocol	

def writeToServer(msg):
	global m_factory

	m_factory.server.transport.write(json.dumps(msg))
	log.msg("Wrote to server!")

def handleNewPlayer(decoded):
	global oled
	oled.drawWelcomeScreen(decoded["player_num"])
	oled.drawEIVMap(decoded["location"])

def processJSON(decoded):
	log.msg("%s" % decoded)
	request = decoded["request"]

	# Use the request field to execute corresponding function.
	# If the player can perform a new action, add it here:
	response = {	"NEWPLAYER": 	handleNewPlayer,
			"TURNSTART": 	handleTurnStart,
		   }[request](decoded)

	return

def handleNewPlayer(decoded):
	global PLAYER_ID 
	
	PLAYER_ID = decoded["player_num"]
	log.msg("My player ID is %d" % PLAYER_ID)


	return

def handleTurnStart(decoded):
	global oled
	log.msg("Turn started!")
	newLocation = location()
	oled.drawEIVMap(newLocation)
	writeToServer({"request": "UPDATE", "player_num": PLAYER_ID, "location": newLocation})
	log.msg("Turn start!")

	roll = rollDice()
	writeToServer({"request": "HELLO"})

	return

# HELPER FUNCTIONS
def rollDice(max=6):
	random.seed(time.time())
	return random.randint(0, max)

# MAIN
def main():
	global m_factory

	# Defaults
	HOST = 'localhost'
	PORT = 8080

	# Option parser
	version_msg = "sclient.py--3.8.17"
	usage_msg = """%prog [OPTIONS] ...
	getFlag?!"""

	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-s", "--specificHost",
		dest="specific_host",
		default=None,
		help="Connect to a specific hostname other than localhost.")

	options, args = parser.parse_args(sys.argv[1:])

	if options.specific_host is not None:
		HOST = options.specific_host

	# Start
	log.startLogging(sys.stdout)

	m_factory = ClientFactory()
	m_factory.server = None	

	reactor.connectTCP(HOST, PORT, m_factory)
	reactor.run()
	# End

if __name__ == "__main__":
	main()
