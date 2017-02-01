#!/usr/bin/python

"""
Takes in one argument which is the hostname of the server.
"""

from modules.jsonsocket import Client
from modules.dof import DOFsensor
import mraa
from optparse import OptionParser
import socket
from subprocess import call
import sys
import time

def dof_function():
		dof  = DOFsensor()
		dof.update_values()
		print "Here: ", dof.getAX()

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
