#!/usr/bin/python

"""
Notes:
	0 is PRESSED, 1 is NOT PRESSED
	BUTTON_UP	47
	BUTTON_DOWN	44
	BUTTON_LEFT	165
	BUTTON_RIGHT	45
	BUTTON_SELECT	48
	BUTTON_A	49
	BUTTON_B	46
"""

from modules.jsonsocket import Client
from modules.dof import DOFsensor
from modules.oled import OLED
import mraa
from optparse import OptionParser
import socket
from subprocess import call
import sys
import time

BUTTON_UP = 	mraa.Gpio(47, owner=False, raw=True)
BUTTON_DOWN = 	mraa.Gpio(44, owner=False, raw=True)
BUTTON_LEFT = 	mraa.Gpio(165, owner=False, raw=True)
BUTTON_RIGHT = 	mraa.Gpio(45, owner=False, raw=True)
BUTTON_SELECT = mraa.Gpio(48, owner=False, raw=True)
BUTTON_A = 	mraa.Gpio(49, owner=False, raw=True)
BUTTON_B = 	mraa.Gpio(46, owner=False, raw=True)

BUTTON_UP.dir(mraa.DIR_IN)
BUTTON_DOWN.dir(mraa.DIR_IN)
BUTTON_LEFT.dir(mraa.DIR_IN)
BUTTON_RIGHT.dir(mraa.DIR_IN)
BUTTON_SELECT.dir(mraa.DIR_IN)
BUTTON_A.dir(mraa.DIR_IN)
BUTTON_B.dir(mraa.DIR_IN)

def dof_function():
	m_OLED = OLED()
	while True:
		if BUTTON_A.read() == 0:
			m_OLED.write("Hello")

def network_connect(host_name, post):
	while True:
		name = raw_input('Enter any string to be sent: ')
		test_dict = dict([('wifi1', 1), ('wifi2', 2)]);

		data = {
			'player':	1,
			'name':		name,
			'use':		0,
			'wifi_list': 	test_dict
		}		

		client = Client()
		client.connect(host_name, port)
		client.send(data)
		client.close()

def main():
	# Constants
	DEFAULT = "localhost"
	
	# Define option parse messages/options
	version_msg = "client_12.22.16"
	usage_msg = """%prog [OPTIONS] ...
	Connects client to HOST found on same network."""

	parser = OptionParser(version=version_msg, usage=usage_msg)	

	parser.add_option("-s", "--specific", action="store", 
		dest="specific_host", help="Use spcific HOST.")
	parser.add_option("-t", "--test", action="store_true", default=False,
		dest="dof_test", help="Enables DOF testing.")

	options, args = parser.parse_args(sys.argv[1:])

	if options.specific_host is not None:
		host_name = options.specific_host
	else:
		host_name = DEFAULT
	port = 8888

	# Option select
	if options.dof_test == True:
		dof_function()
	elif options.dof_test == False:
		network_connect(host_name, post)

if __name__ == "__main__":
	main()
