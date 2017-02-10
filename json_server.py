#!/usr/bin/python

import json
from modules.jsonsocket import Server
from multiprocessing import Process, Pipe
from optparse import OptionParser
import os
import socket
from subprocess import call
import sys

def client_connect(server, num):
	# Connect to a player and give them a player ID
	print 'Connecting to player %d!' % num
	server.send({'player_num': num})
	while True:	
		print server.recv()

def main():
	# Define option parse messages/options
	version_msg = "server_12.22.16"
	usage_msg = """%prog [OPTIONS] ...
	Hosts server on HOST & waits for clients to connect."""
	
	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-s", "--specific", action="store",
		dest="specific_host", help="Hosts onto specific HOST.")

	options, args = parser.parse_args(sys.argv[1:])

	if options.specific_host is not None:
		host = options.specific_host
	else:
		host = 'localhost'

	# Set up server variables
	port = 8888
	server = Server(host, port)
	client_process_list = []
	num = 1

	# Accept incoming connections and make a thread for it
	print "Set-up complete!"
	while True:
		print "Awaiting for a player to connect..."
		server.accept()
		print "Player connected! Creating new process!"
		process = Process(target=client_connect, args=(server, num ))
		num += 1
		client_process_list.append(process)
		process.start()

	# Join & close server
	server.close()

if __name__ == "__main__":
	main()

