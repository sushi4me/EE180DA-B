#!/usr/bin/python

"""
NOTES:
	SEND:
	{"request": "ACTION", "player_num": PLAYER_ID, "action": action}
	{"request": "TURNEND", "player_num": PLAYER_ID}
	{"request": "ROLL", "player_num": PLAYER_ID, "roll": roll}

	RECEIVE:
	{"request": "DISPLAY", "msg": msg, "location": location, "event": event_num}
	{"request": "NEWPLAYER", "player_num": PLAYER_ID}
	{"request": "RESULT",	"result": result}
	{"request": "TURNSTART"}
	{"request": "WINNER", "player_num": PLAYER_ID}

"""

from datetime			import datetime
from location.location		import location
from Modules.Buzzer		import Buzzer
#from Modules.DOF		import DOFsensor
from Modules.IMU.gesture	import run as detectGesture
from Modules.OLED		import OLED
from Modules.Globals		import buttons
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
global PLAYER_ID
global Buzzer
DISPLAY = OLED()
AUDIO = Buzzer()

# TWISTED NETWORKING
class ClientProtocol(protocol.Protocol):	
	def connectionMade(self):
		global DISPLAY, TESTING
		DISPLAY.connecting()
		sleep(1)
		DISPLAY.connected()
		AUDIO.connected()
		sleep(1)
		DISPLAY.gettingLocation()
		log.msg("CONNECTED TO SERVER")
		self.factory.server = self

		if not TESTING:
			startLocation = location()
		else:
			startLocation = 1

		# Request for player_num identification
		self.transport.write(json.dumps({"request": "NEWPLAYER", "location": startLocation}))
		DISPLAY.drawEIVMap(startLocation)
		sleep(3)

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
			"RESULT":	handleTurnResult,
			"TURNSTART": 	handleTurnStart,
			"WINNER":	handleWinner
		   }[request](decoded)

	return

def handleDisplay(decoded):
	DISPLAY.clear()
	DISPLAY.write(str(decoded["msg"]))
	sleep(3)
	if decoded["event"] == 3:
		monster_generator = rollDice(3)
		if monster_generator == 1:
			DISPLAY.drawMonster1()
		elif monster_generator == 2:
			DISPLAY.drawMonster2()
		elif monster_generator == 3:
			DISPLAY.drawMonster3()
		sleep(3)

		DISPLAY.clear()
		DISPLAY.write("What will you do?!  > SWORD\n> SHIELD\n>MAGIC")
		# TO DO: Battle, event, nothing?
		"""
		Need display screen, detect gesture for action like dice roll!
		"""
		action = detectGesture()
		AUDIO.powerUp()
		writeToServer({"request": "ACTION", "player_num": PLAYER_ID, "action": action})

		DISPLAY.clear()
		if action == 1:
			# Sword
			DISPLAY.write("You attacked with a sword!")
			AUDIO.shoot()
		elif action == 2:
			# Shield
			DISPLAY.write("You attempt to block the attack!")
			AUDIO.cloak()
		elif action == 3:
			# Magic
			DISPLAY.write("You cast a magical spell!")
			AUDIO.powerUP()

		sleep(3)
	else:
		writeToServer({"request": "TURNEND", "player_num": PLAYER_ID})

	#DISPLAY.updateMap(decoded["location"])
	return

def handleNewPlayer(decoded):
	global PLAYER_ID, DISPLAY
	
	PLAYER_ID = decoded["player_num"]
	log.msg("PLAYER ID IS %d" % PLAYER_ID)
	DISPLAY.clear()
	DISPLAY.drawWelcomeScreen(str(decoded["player_num"]))
	#AUDIO.connected()
	sleep(2)

	return

def handleTurnResult(decoded):
	global PLAYER_ID

	msg = decoded["msg"]

	DISPLAY.clear()
	DISPLAY.write(str(msg))
	sleep(3)
	
	writeToServer({"request": "TURNEND", "player_num": PLAYER_ID})
	
	DISPLAY.clear()
	# TO DO: Waiting display
	DISPLAY.write("Waiting for other player...")
	return

def handleTurnStart(decoded):
	global PLAYER_ID, DISPLAY, AUDIO
	
	log.msg("START MY TURN")
	DISPLAY.promptDiceRoll()
	gesture = detectGesture()
	roll = rollDice()
	DISPLAY.drawDiceRoll()

	# Wait for player to arrive at destination and press A
	DISPLAY.clear()
	DISPLAY.write("ROLL: " + str(roll) + "\nMove & \npress A to continue")
	while True:
		button_select = DISPLAY.waitForUserInput()
		AUDIO.starWars()
		if button_select != buttons.A:
			continue
		else:
			# TO DO: Pass control to player, unless no event
			break
	writeToServer({"request": "ROLL", "player_num": PLAYER_ID, "roll": roll})
	return

def handleWinner(decoded):
	global PLAYER_ID

	winner = decoded["player_num"]

	DISPLAY.clear()
	if winner == PLAYER_ID:
		# TO DO: Winner display
		DISPLAY.write("\n\nWINNER!")
		AUDIO.disconnected()
		sleep(3)
	else:
		# TO DO: Loser display
		DISPLAY.write("\n\nLOSER!")
		sleep(3)
		DISPLAY.drawDead()
		sleep(3)

# HELPER FUNCTIONS
def rollDice(max=6):
	random.seed(time())
	return random.randint(1, max)

# MAIN
def main():
	global TESTING, m_factory

	# Defaults
	HOST = 'localhost'
	PORT = 8080

	# Option parser
	version_msg = "sclient.py--3.8.17"
	usage_msg = """%prog [OPTIONS] ...
	getFlag?!"""

	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-i", "--ipHost",
		action="store_true",
		dest="ip_host",
		default=False,
		help="Connect to a specific hostname other than localhost.")
	parser.add_option("-t", "--testing",
		action="store_true",
		dest="testing",
		default=False,
		help="Connect to a specific hostname other than localhost.")

	options, args = parser.parse_args(sys.argv[1:])

	if options.ip_host is True:
		# Default IP grab
		exe = "/home/root/EE180DA-B/Modules/getServerIP.sh"
		subprocess.call([exe])
		with open('ipaddress.txt', 'r') as fd:
			HOST = fd.readline().strip("\n")

	if options.testing is not None:
		TESTING = options.testing

	# Start
	print "SERVER HOSTNAME: %s" % HOST
	
	log.startLogging(sys.stdout)

	m_factory = ClientFactory()
	m_factory.server = None	

	reactor.connectTCP(HOST, PORT, m_factory)
	reactor.run()
	# End

if __name__ == "__main__":
	main()
