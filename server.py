#!/usr/bin/python

import socket
import sys
from optparse import OptionParser


def main():
	#Define option parse messages/options
	version_msg = "server_12.22.16"
	usage_msg = """%prog [OPTIONS] ...
	Hosts server on HOST & waits for clients to connect."""
	
	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-s", "--specific", action="store",
		dest="specific_host", help="Hosts onto specific HOST.")

	options, args = parser.parse_args(sys.argv[1:])
	
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
		try:	
			print 'Got connection from: ', client_address
			c.send('You have connected!')
		finally:
			c.close()

if __name__ == "__main__":
	main()
