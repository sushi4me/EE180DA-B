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
	{"request": "GAMESTART"}
	{"request": "EVENT", "event": "event_num"}
	{"request": "NEWPLAYER", "player_num": player_num}
	{"request": "TURNSTART"}
"""

from datetime				import datetime
#from Modules.Buzzer			import Buzzer
#from Modules.DOF 			import DOFsensor
#from Modules.OLED			import OLED
from optparse				import OptionParser
from random				import randint
from twisted.internet			import reactor, protocol, defer
#from twisted.internet.task		import LoopingCall
from twisted.python			import log
#from position_estimation.position 	import position

import json
#import mraa
import os
import random
import sys
import time

# GLOBALS

# TWISTED NETWORKING
class ClientProtocol(protocol.Protocol):	
	def connectionMade(self):
		self.transport.write(json.dumps({"request": "GREETINGS"}))

	def dataReceived(self, data):
		decoded = json.loads(data)
		log.msg("%s" % data)

class ClientFactory(protocol.ClientFactory):
	protocol = ClientProtocol	

# MAIN
def main():
	# Defaults
	HOST = 'localhost'
	PORT = 8080

	# Start
	log.startLogging(sys.stdout)

	reactor.connectTCP(HOST, PORT, ClientFactory())
	reactor.run()
	# End

if __name__ == "__main__":
	main()
