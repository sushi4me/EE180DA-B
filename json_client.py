#!/usr/bin/python

"""
Takes in one argument which is the hostname of the server.
"""

from modules.jsonsocket import Client
from optparse import OptionParser
import socket
import sys
import time

def main():
	#Define option parse messages/options
	version_msg = "client_12.22.16"
	usage_msg = """%prog [OPTIONS] ...
	Connects client to HOST found on same network."""

	parser = OptionParser(version=version_msg, usage=usage_msg)	
	parser.add_option("-s", "--specific", action="store", 
		dest="specific_host", help="Use spcific HOST.")

	options, args = parser.parse_args(sys.argv[1:])
	
	"""
	#Create a TCP/IP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	if options.specific_host is not None:
		host_name = options.specific_host
	else:
		host_name = "Nathan-Laptop.hawaii.rr.com" #default host
	
	#Connect
	server_name = (host_name, 8000)
	s.connect(server_name)

	
	#Print what is sent from the server
	try:
		#TO-DO: [WHILE 1]Get info from Intel Edison & send it
		print s.recv(1024)
	finally:
		s.close
	"""

	host = 'wifi-131-179-3-10.host.ucla.edu'
	port = 8888

	while True:
		pos = input('What is your position (1-10): ')
		data = {
			'player': 1,
			'position': pos,
			'use':	0
		}		
		client = Client()
		client.connect(host, port)
		client.send(data)
		client.close()
		time.sleep(1)

if __name__ == "__main__":
	main()
