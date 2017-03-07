#!/usr/bin/python

"""
NOTES:
	Requires pyupm to run, intended for the Intel Edison.

"""

from datetime				import datetime
#from Modules.Buzzer			import Buzzer
#from Modules.DOF 			import DOFsensor
from Modules.OLED			import OLED
from optparse				import OptionParser
from random				import randint
from twisted.internet			import reactor, protocol, defer
#from twisted.internet.task		import LoopingCall		#IMPORTANT!
from twisted.python			import log
from position_estimation.position 	import position

import json
#import mraa
import os
import random
import sys
import time

# GLOBALS
CURRENT_LOCATION = 0
PLAYER_NUM = 0
STATUS = 0
TESTING = False
#buzzer = Buzzer()
oled = OLED()

# TWISTED NETWORKING
class ClientProtocol(protocol.Protocol):	
	def connectionMade(self):
		global buzzer, oled
		log.msg("Connected to server.")
		#BUZZER.connected()
		oled.drawInitScreen()
		time.sleep(1)
		oled.clear()
		oled.drawStartScreen()
		oled.clear()
		oled.drawEIVMap()
		i = 0
		while (i < 62):
			oled.updateMap(i)
			oled.waitForUserInput()
			i += 1
		#self.transport.loseConnection()


	def dataReceived(self, data):
		global PLAYER_NUM
		try:
			log.msg("Data recieved from server: %s" % data)
			decoded_data = json.loads(data)			
			self.transport.getHandle().sendall(self.processResponse(decoded_data))
		except:
			pass

		# If GAMESTART then send TURNEND afterwards
		request = decoded_data["request"]
		if request == "GAMESTART":
			self.transport.write(json.dumps({"request": "TURNEND",
				"player_num": PLAYER_NUM}))

	def connectionLost(self, reason):
		#global PLAYER_NUM, BUZZER
		self.transport.write(json.dumps({"request": "QUIT", "player_num": PLAYER_NUM}))		
		#BUZZER.disconnected()
		log.msg("Protocol::Connection lost.")

	# HELPER FUNCTIONS
	def processResponse(self, decoded_data):
		request = decoded_data["request"]
		log.msg("Request: %s" % request)
		response = {	"FULL": 	self.handleQuit,
			    	"GAMESTART": 	self.handleSetPlayerNumber,
				"NEWPLAYER": 	self.handleSetPlayerNumber,
		    		"STATUS": 	self.handleSetStatus,
		    		"TURNSTART":	self.handleTurnStart,
		    		"TURNEND": 	self.handleTurnEnd
			    }[request](decoded_data)
		return response

	def handleQuit(self, decoded_data):	
		log.msg("Quitting!")
		reactor.stop()

	def handleSetPlayerNumber(self, decoded_data):
		global PLAYER_NUM
		PLAYER_NUM = decoded_data['player_num']
		log.msg("You are player %d" % PLAYER_NUM)

		if TESTING:
			CURRENT_LOCATION = 1
		else:
			CURRENT_LOCATION = position()

		# time.sleep(5)
		return json.dumps({"request": "UPDATE",
			"player_num": PLAYER_NUM,
			"location": CURRENT_LOCATION})

	def handleSetStatus(self, decoded_data):	
		global STATUS
		STATUS = decoded_data['status']
		print STATUS
		# Do something here to OLED when afflicted with status

	def handleTurnStart(self, decoded_data):
		global CURRENT_LOCATION
		# Roll a die
		random.seed(time.time())
		roll = random.randint(0, 6)
		log.msg("Rolled: %d" % roll)

		# On button press locate player and find out how many steps
		if TESTING:
			log.msg("Hi")
			player_step = input('How many steps? ')
			CURRENT_LOCATION = CURRENT_LOCATION + player_step
			if player_step > roll:
				log.msg("Go back! You went too far!")
			elif player_step < roll:
				pass
			elif player_step == roll:
				pass
			self.transport.getHandle().sendall(json.dumps({"request": "UPDATE",
				"location": CURRENT_LOCATION}))
		"""
		else:
			o = OLED()
			flag = True
			while flag:
				if o.waitUserInput() == "A":
					previous_location = CURRENT_LOCATION

					if options.testing == True:
						CURRENT_LOCATION = 4
					else:
						CURRENT_LOCATION = position()

					diff = CURRENT_LOCATION - previous_location

					if diff > roll:
						log.msg("Go back!  You went too far!")
						continue
					elif diff < roll:
						flag = False
					elif diff == roll:
						flag = False
					
			self.transport.getHandle().sendall(json.dumps({"request": "UPDATE",
				"location": CURRENT_LOCATION}))
		"""

		# Record gestures and deduct from remainder


		# On button press or remainder is zero - TURNEND

	def handleTurnEnd(decoded_data):
		global PLAYER_NUM
		#TO DO:

class ClientFactory(protocol.ClientFactory):
	protocol = ClientProtocol	

	def clientConnectionLost(self, connector, reason):
		log.msg("Factory::Connection lost.")

# MAIN
def main():
	global TESTING

	# Defaults
	HOST = 'localhost'
	PORT = 8080

	# Option parser
	version_msg = "client.py--1.12.17"
	usage_msg = """%prog [OPTIONS] ...
	Connect to someone who is hosting server.py."""
	
	# Option parser
	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-s", "--specific", 
		action="store",
		dest="specific_host", 
		help="Hosts onto specific HOST.")
	parser.add_option("-v", "--verbose", 
		action="store_true",
		dest="verbose", 
		default=False, 
		help="Prints debugging statements on console.")
	parser.add_option("-t", "--testing",
		action="store_true",
		default=False,
		help="Testing mode for Nathan laptop.")

	options, args = parser.parse_args(sys.argv[1:])

	if options.testing is not None:
		TESTING = options.testing

	if options.specific_host is not None:
		HOST = options.specific_host

	# Start
	log.startLogging(sys.stdout)
	log.msg("Starting client.")

	# Run the client
	reactor.connectTCP(HOST, PORT, ClientFactory())
	reactor.run()

if __name__ == "__main__":
	main()
