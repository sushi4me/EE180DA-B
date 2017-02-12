#!/usr/bin/python

from modules.jsonsocket import Server
from multiprocessing 	import Process, Pipe
from optparse 		import OptionParser
from subprocess 	import call

import json
import os
import socket
import sys

def client_connect(server, player_count):
	# Connect to a player and give them a player ID
	print 'Connecting to player %d!' % player_count
	server.send({'player_num': player_count})

	# Keep polling for client data
	while True:	
		print server.recv()

def main():
	# Define option parse messages/options
	version_msg = "server_12.22.16"
	usage_msg = """%prog [OPTIONS] ...
	Hosts server on HOST & waits for clients to connect."""
	
	# Option parser
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
	player_count = 1
	setup = True

	# Accept incoming connections and make a thread for it
	print "Set-up complete!"
	while setup:
		print "Awaiting for a player to connect..."
		server.accept()
		print "Player connected! Creating new process!"
		parent_conn, child_conn = Pipe()		
		process = Process(target=client_connect, args=(server, player_count ))
		player_count += 1
		client_process_list.append(process)
		process.start()
		if player_count == 5
			server.send({'status': 1})
			break

	# Game logic section
	while True:
		print "OK"
	# Join & close server
	server.close()

if __name__ == "__main__":
	main()

