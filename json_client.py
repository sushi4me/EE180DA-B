#!/usr/bin/python

"""
Notes:
	FROM oled.py
		0 is PRESSED, 1 is NOT PRESSED
		BUTTON_UP	47
		BUTTON_DOWN	44
		BUTTON_LEFT	165
		BUTTON_RIGHT	45
		BUTTON_SELECT	48
		BUTTON_A	49
		BUTTON_B	46
"""

from modules.jsonsocket	import Client
from modules.dof 	import DOFsensor
from modules.oled 	import OLED
from multiprocessing 	import Process, Pipe
from optparse 		import OptionParser
from subprocess 	import call

import json
import mraa
import socket
import sys
from threading 	import Thread
import time

player_num = 0
game_start = 0
frozen = 0

def dof_function():
	m_OLED = OLED()
	if m_OLED.BUTTON_A.read() == 0 and m_OLED.BUTTON_B.read() == 0:
		exit()
	elif m_OLED.BUTTON_A.read() == 0:
		m_OLED.clear()
		m_OLED.write("Hello")

def connection_init(client):
	print "You are now connected!"
	raw_player_num = client.recv()
	temp = json.loads(raw_player_num)
	player_num = temp['player_num']

	# Wait for a game_start signal
	raw_game_start = client.recv()
	temp = json.loads(raw_game_start)
	game_start = temp['signal']

def waiting_server(client, lock):
	while True:
		response = client.recv()
		temp = json.loads(response)
		status = temp['status']

		print status

		lock.acquire()
		frozen = status
		lock.release()

def main():
	# Globals
	global frozen
	global game_start
	global player_num
	lock = threading.Lock()	
	
	# Define option parse messages/options
	version_msg = "client_12.22.16"
	usage_msg = """%prog [OPTIONS] ...
	Connects client to HOST found on same network."""

	# Option parser
	parser = OptionParser(version=version_msg, usage=usage_msg)	
	parser.add_option("-s", "--specific", action="store", 
		dest="specific_host", help="Use spcific HOST.")
	options, args = parser.parse_args(sys.argv[1:])

	if options.specific_host is not None:
		host = options.specific_host
	else:
		host = 'localhost'
	
	# Set up client variables
	parent_conn, child_conn = Pipe()
	port = 8888
	client = Client()
	print 'Trying to connect to %s...' % host
	client.connect(host, port)

	# GENERATE DICTIONARIES

	connection_init(client)

	wait_thread = Thread(target=wait_server, args=(client, lock, ))
	wait_thread.start()

	# while game_start is not 0:
		

if __name__ == "__main__":
	main()
