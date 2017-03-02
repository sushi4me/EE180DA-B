#!/usr/bin/python

"""
NOTES:
	Requires pyupm to run, intended for the Intel Edison.

"""
#from Modules.Buzzer		import Buzzer
#from Modules.DOF 		import DOFsensor
#from Modules.OLED		import OLED
from optparse			import OptionParser
from random			import randint
from twisted.internet		import reactor, protocol, defer
from twisted.internet.task	import LoopingCall		#IMPORTANT!
from twisted.python		import log
from position_estimation.position import position

import json
import mraa
import os
import sys
import time

# GLOBALS
PLAYER_NUM = 0
STATUS = 0
#BUZZER = Buzzer()

# TWISTED NETWORKING
class ClientProtocol(protocol.Protocol):	
	def periodic(self):
		global PLAYER_NUM	
		# Get player data and dump in this function
		if PLAYER_NUM != 0:
			location = position()
			self.transport.write(json.dumps({"request": "UPDATE", 
				"player_num": PLAYER_NUM, 
				"location": location}))
			if options.verbose:
				print "Location sent: %d" % location	
		else:
			pass

	def connectionMade(self):
		#global BUZZER
		if options.verbose:
			print "Connected to server."
		lp = LoopingCall(self.periodic)
		lp.start(1)
		#BUZZER.connected()
		#self.transport.loseConnection()

	def dataReceived(self, data):
		try:
			if options.verbose:
				print "Data recieved from server: %s" % data
			processResponse(data)
		except:
			pass

	def connectionLost(self, reason):
		#global PLAYER_NUM, BUZZER
		self.transport.write(json.dumps({"request": "QUIT", "player_num": PLAYER_NUM}))		
		#BUZZER.disconnected()
		if options.verbose:
			print "Protocol::Connection lost."

class ClientFactory(protocol.ClientFactory):
	protocol = ClientProtocol	

	def clientConnectionLost(self, connector, reason):
		if options.verbose:
			print "Factory::Connection lost."

# HELPER FUNCTIONS
def handleSetPlayerNumber(decoded_data):
	global PLAYER_NUM
	PLAYER_NUM = decoded_data['player_num']
	if options.verbose:
		print "You are player %d" % PLAYER_NUM

def handleSetStatus(decoded_data):	
	global STATUS
	STATUS = decoded_data['status']
	print STATUS
	# Do something here to OLED when afflicted with status

def handleQuit(decoded_data):	
	if options.verbose:
		print "Quitting!"
	reactor.stop()

def processResponse(data):
	decoded_data = json.loads(data)			
	request = decoded_data["request"]
	if options.verbose:
		print "Request: %s" % request
	response = {"NEWPLAYER" : handleSetPlayerNumber,
		    "STATUS" : handleSetStatus,
		    "FULL" : handleQuit
		   }[request](decoded_data)
# MAIN
def main():
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
	parser.add_option("-l", "--laptop",
		action="store_true",
		dest="ie_lib",
		default=False,
		help="Does not import Intel Edison only files.")

	options, args = parser.parse_args(sys.argv[1:])

	if options.specific_host is not None:
		HOST = options.specific_host

	# Start
	if options.verbose:
		print "Starting client."

	# Start logging
	log.startLogging(sys.stdout)

	# Run the client
	reactor.connectTCP(HOST, PORT, ClientFactory())
	reactor.run()

if __name__ == "__main__":
	main()
