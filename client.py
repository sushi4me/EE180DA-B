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
from Modules.Buzzer		import Buzzer
#from Modules.DOF 		import DOFsensor
from Modules.OLED		import OLED
from Modules.Globals 		import buttons
from optparse			import OptionParser
from random			import randint
from twisted.internet		import reactor, protocol, defer
#from twisted.internet.task	import LoopingCall
from twisted.python		import log
from location.location 		import location
from Modules.IMU.gesture 	import run as detectGesture

import json
import mraa
import os
import random
import sys
import time

# GLOBALS
global DISPLAY
DISPLAY = OLED()
global PLAYER_ID
global Buzzer
AUDIO = Buzzer()

# TWISTED NETWORKING
class ClientProtocol(protocol.Protocol):	
	def connectionMade(self):
                global DISPLAY
                DISPLAY.connecting()
                log.msg("Connected to server.")
		self.factory.server = self
                
                log.msg("Determining start location...")
                startLocation = location()
                DISPLAY.drawEIVMap(startLocation)
                log.msg("Done!")

                self.transport.write(json.dumps({"request": "NEWPLAYER", "location": startLocation}))
                DISPLAY.connected()
                time.sleep(1)

	def dataReceived(self, data):
		decoded = json.loads(data)		
		processJSON(decoded)


class ClientFactory(protocol.ClientFactory):
	protocol = ClientProtocol	

def writeToServer(msg):
	global m_factory

	m_factory.server.transport.getHandle().sendall(json.dumps(msg))
	#m_factory.server.transport.write(json.dumps(msg))
	log.msg("Wrote to server!")


def processJSON(decoded):
	log.msg("%s" % decoded)
	request = decoded["request"]

	# Use the request field to execute corresponding function.
	# If the player can perform a new action, add it here:
	response = {	"DISPLAY":	handleDisplay,
			"NEWPLAYER": 	handleNewPlayer,
			"TURNSTART": 	handleTurnStart,
		   }[request](decoded)

	return

def handleDisplay(decoded):
	# Stuck here
	DISPLAY.write(str(decoded["msg"]))
	time.sleep(5)
	DISPLAY.updateMap(decoded["location"])

def handleNewPlayer(decoded):
	global PLAYER_ID, DISPLAY
	
	PLAYER_ID = decoded["player_num"]
	log.msg("My player ID is %d" % PLAYER_ID)
	DISPLAY.drawWelcomeScreen(str(decoded["player_num"]))
	#AUDIO.connected()
	time.sleep(2)

	return

def handleTurnStart(decoded):
	global PLAYER_ID, DISPLAY, AUDIO
	
	log.msg("Turn started!")
	DISPLAY.promptDiceRoll()
	gesture = detectGesture()
	roll = rollDice()
	DISPLAY.displayDiceRoll()

	# Wait for player to arrive at destination and press A
	DISPLAY.clear()
	DISPLAY.write("You rolled    a\n    " + str(roll) + "\nPress (A) to continue")
	while True:
		button_select = DISPLAY.waitForUserInput()
		if button_select != buttons.A:
			continue
		else:
			DISPLAY.clear()
			DISPLAY.write("Checking...")
			#newLocation = location()
			writeToServer({"request": "ROLL", "player_num": PLAYER_ID, "roll": roll})
			time.sleep(1)
			break
			"""
			if abs(newLocation - decoded["location"]) <= roll:
				DISPLAY.clear()
				DISPLAY.write("You are now at %d" % newLocation)
				time.sleep(3)
				DISPLAY.drawEIVMap(newLocation)
				break
			else:
				continue
			"""
	#writeToServer({"request": "UPDATE", "player_num": PLAYER_ID, "location": newLocation})
	writeToServer({"request": "TURNEND", "player_num": PLAYER_ID})
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
