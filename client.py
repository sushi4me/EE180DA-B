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
#from Modules.OLED		import OLED
from optparse			import OptionParser
from random			import randint
from twisted.internet		import reactor, protocol, defer
#from twisted.internet.task	import LoopingCall
from twisted.python		import log
from location.location 		import location

import json
#import mraa
import os
import random
import sys
import time

# GLOBALS
global PLAYER

# TWISTED NETWORKING
class ClientProtocol(protocol.Protocol):	
	def connectionMade(self):
		global PLAYER

                log.msg("Connected to server.")
                
                log.msg("Determining start location...")
                startLocation = location()
                log.msg("Done!")

                self.transport.write(json.dumps({"request": "NEWPLAYER", "location": startLocation}))

	def dataReceived(self, data):
		decoded = json.loads(data)
		log.msg("%s" % data)

class ClientFactory(protocol.ClientFactory):
	protocol = ClientProtocol	

def processJSON(decoded):
		log.msg("%s" % decoded)
		request = decoded["request"]

		# Use the request field to execute corresponding function.
		# If the player can perform a new action, add it here:
		response = {	"NEWPLAYER": 	self.handleNewPlayer,
				"TURNSTART": 	self.handleTurnEnd,
			   }[request](decoded)

		return

def handleNewPlayer(decoded):
	global PLAYER



	return

def handleTurnStart(decoded):
	log.msg("Turn started!")

	return

# MAIN
def main():
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

	reactor.connectTCP(HOST, PORT, ClientFactory())
	reactor.run()
	# End

if __name__ == "__main__":
	main()
