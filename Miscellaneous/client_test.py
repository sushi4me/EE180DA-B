#!/usr/bin/python

"""
NOTES:
	Requires pyupm to run, intended for the Intel Edison.

"""

from datetime				import datetime
#from Modules.Buzzer			import Buzzer
#from Modules.DOF 			import DOFsensor
#from Modules.OLED			import OLED
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

# TWISTED NETWORKING
class ClientProtocol(protocol.Protocol):	
	def connectionMade(self):
		self.transport.write(json.dumps({"request": "GREETINGS"}))

	def dataReceived(self, data):
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
