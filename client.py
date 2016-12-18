#!/usr/bin/python

"""
Takes in one argument which is the hostname of the server.
"""

import socket
import sys

#Create a socket that TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_name = (sys.argv[1], 8000)
s.connect(server_name)

try:
	print s.recv(1024)
finally:
	s.close
