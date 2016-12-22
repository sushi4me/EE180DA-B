#!/usr/bin/python

"""
Takes in one argument which is the host name.
Check using host command.
Example:
	python server.py nathan.hawaii.rr.com
"""

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_name = sys.argv[1]
server_address = (server_name, 8000)
s.bind(server_address)

s.listen(5)

while True:
	TO-DO: forking new processes for each Intel Edison
	c, client_address = s.accept()
	try:	
		print 'Got connection from: ', client_address
		c.send('You have connected!')
	finally:
		c.close()
