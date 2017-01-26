#!/usr/bin/python

import json
from modules.jsonsocket import Server
from optparse import OptionParser
import socket
from subprocess import call
import sys

def new_socket_connection(server):
	while True:	
		print server.recv()
	'''
		try:	
			print 'Got connection from: ', client_address
			c.send('You have connected!')
		finally:
			c.close()
	'''
def main():
	#Define option parse messages/options
	version_msg = "server_12.22.16"
	usage_msg = """%prog [OPTIONS] ...
	Hosts server on HOST & waits for clients to connect."""
	
	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-s", "--specific", action="store",
		dest="specific_host", help="Hosts onto specific HOST.")

	options, args = parser.parse_args(sys.argv[1:])
	
	"""	
	#Create a TCP/IP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	if options.specific_host is not None:
		server_name = options.specific_host
	else:
		server_name = "Nathan-Laptop.hawaii.rr.com" #default host

	#Connect
	server_address = (server_name, 8000)
	s.bind(server_address)

	s.listen(5)

	while True:
		c, client_address = s.accept()
		newpid = os.fork()
		if newpid == 0:
			new_socket_connection(c);
		else
			print 'Dropped someone?!'
		if input() == 'q': break
	"""

	#host = 'wifi-131-179-2-179.host.ucla.edu'
	host = 'localhost'	
	port = 8888
	server = Server(host, port)

	while True:
		server.accept()
		newpid = os.fork()
		if newpid == 0:
			while True:
				data = server.recv()
				print data

	server.close()
if __name__ == "__main__":
	main()
