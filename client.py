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
from location.location 		import location
from Modules.Buzzer		import Buzzer
#from Modules.DOF 		import DOFsensor
from Modules.IMU.gesture 	import run as detectGesture
from Modules.OLED		import OLED
from Modules.Globals 		import buttons
from optparse			import OptionParser
from random			import randint
from time			import sleep, time
from twisted.internet		import reactor, protocol
#from twisted.internet.task	import LoopingCall
from twisted.python		import log

import json
import mraa
import os
import random
import subprocess
import sys

# GLOBALS
global DISPLAY
DISPLAY = OLED()
global PLAYER_ID
global Buzzer
AUDIO = Buzzer()

# TWISTED NETWORKING
class ClientProtocol(protocol.Protocol):	
	def connectionMade(self):
		global DISPLAY, TESTING
		DISPLAY.connecting()
		log.msg("CONNECTED")
		self.factory.server = self

		log.msg("LOCATING START LOCATION")
		if not TESTING:
			startLocation = location()
		else:
			startLocation = 1
		DISPLAY.drawEIVMap(startLocation)

		# Request for player_num identification
		self.transport.write(json.dumps({"request": "NEWPLAYER", "location": startLocation}))
		DISPLAY.connected()
		sleep(1)

	def dataReceived(self, data):
		log.msg("%s" % data)
		decoded = json.loads(data)		
		processJSON(decoded)


class ClientFactory(protocol.ClientFactory):
	protocol = ClientProtocol	

def writeToServer(msg):
	global m_factory

	# Use this over the original because it is not "buffered"
	m_factory.server.transport.getHandle().sendall(json.dumps(msg))
	#m_factory.server.transport.write(json.dumps(msg))
	log.msg("WRITING TO SERVER: %s" % msg)


def processJSON(decoded):
	#log.msg("%s" % decoded)
	request = decoded["request"]

	# Use the request field to execute corresponding function.
	# If the player can perform a new action, add it here:
	response = {	"DISPLAY":	handleDisplay,
			"NEWPLAYER": 	handleNewPlayer,
			"TURNSTART": 	handleTurnStart,
			"WINNER":	handleWinner,
		   }[request](decoded)

	return

def handleDisplay(decoded):
	DISPLAY.write(str(decoded["msg"]))
	sleep(5)
	DISPLAY.clear()
	DISPLAY.updateMap(decoded["location"])


def handleNewPlayer(decoded):
	global PLAYER_ID, DISPLAY
	
	PLAYER_ID = decoded["player_num"]
	log.msg("PLAYER ID IS %d" % PLAYER_ID)
	DISPLAY.drawWelcomeScreen(str(decoded["player_num"]))
	#AUDIO.connected()
	sleep(2)

	return

def handleTurnStart(decoded):
	global PLAYER_ID, DISPLAY, AUDIO
	
	log.msg("START TURN")
	DISPLAY.promptDiceRoll()
	gesture = detectGesture()
	roll = rollDice()
	DISPLAY.displayDiceRoll()

	# Wait for player to arrive at destination and press A
	DISPLAY.clear()
	DISPLAY.write("ROLL: " + str(roll) + "\n\nMove & \npress A to\ncontinue")
	while True:
		button_select = DISPLAY.waitForUserInput()
		if button_select != buttons.A:
			continue
		else:
			# Depending what you place in here you will have different game logic
			# after the button press.  Right now we simply send the roll back to
			# the server and generate a random event.
			DISPLAY.clear()
			#DISPLAY.write("")
			#newLocation = location()
			#writeToServer({"request": "ROLL", "player_num": PLAYER_ID, "roll": roll})
			#sleep(1)
			break
			"""
			if abs(newLocation - decoded["location"]) <= roll:
				DISPLAY.clear()
				DISPLAY.write("You are now at %d" % newLocation)
				sleep(3)
				DISPLAY.drawEIVMap(newLocation)
				break
			else:
				continue
			"""
	#writeToServer({"request": "UPDATE", "player_num": PLAYER_ID, "location": newLocation})
	writeToServer({"request": "TURNEND", "player_num": PLAYER_ID, "roll": roll})
	return

def handleWinnder(decoded):
	global PLAYER_ID

	winner = decoded["player_num"]

	DISPLAY.clear()
	if winner == PLAYER_ID:
		DISPLAY.write("WINNER!")
	else:
		DISPLAY.write("LOSER!")

# HELPER FUNCTIONS
def rollDice(max=6):
	random.seed(time())
	return random.randint(0, max)

# MAIN
def main():
	global TESTING, m_factory

	# Defaults
	HOST = 'localhost'
	PORT = 8080

	# Default IP grab
	exe = "/home/root/EE180DA-B/Modules/getServerIP.sh"
	subprocess.call([exe])
	fd = open('ipaddress.txt', 'r')
	hostname = fd.readline().strip("\n")
	HOST = hostname

	# Option parser
	version_msg = "sclient.py--3.8.17"
	usage_msg = """%prog [OPTIONS] ...
	getFlag?!"""

	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-s", "--specificHost",
		dest="specific_host",
		default=None,
		help="Connect to a specific hostname other than localhost.")
	parser.add_option("-t", "--testing",
		action="store_true",
		dest="testing",
		default=False,
		help="Connect to a specific hostname other than localhost.")

	options, args = parser.parse_args(sys.argv[1:])

	if options.specific_host is not None:
		HOST = options.specific_host

	if options.testing is not None:
		TESTING = options.testing

	# Start
	print "Server's IP Address: %s" % HOST
	
	log.startLogging(sys.stdout)

	m_factory = ClientFactory()
	m_factory.server = None	

	reactor.connectTCP(HOST, PORT, m_factory)
	reactor.run()
	# End

if __name__ == "__main__":
	main()
