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

import json
from modules.jsonsocket import Client
from modules.dof import DOFsensor
from modules.oled import OLED
from multiprocessing import Process, Pipe
import mraa
from optparse import OptionParser
import socket
from subprocess import call
import sys
import time

def dof_function():
	m_OLED = OLED()
	if m_OLED.BUTTON_A.read() == 0 and m_OLED.BUTTON_B.read() == 0:
		exit()
	elif m_OLED.BUTTON_A.read() == 0:
		m_OLED.clear()
		m_OLED.write("Hello")

def network_connect(client, conn):
	print "You are now connected!"
	raw_player_num = client.recv()
	temp = json.loads(raw_player_num)
	player_num = temp['player_num']

	while True:
		print "Polling..."
		if conn.poll():
			conn.recv()
			# Interrupted main section here, set condition	
		name = raw_input('Enter any string to be sent: ')
		test_dict = dict([('fake_wifi', 100)]);

		data = {
			'player':	player_num,
			'name':		name,
			'use':		0,
			'wifi_list': 	test_dict
		}		

		client.send(data)
	
	client.close()

def waiting_function(client, conn):
	response = client.recv()
	# May have to parse in here
	conn.send([response])
	conn.close()

def main():
	# Set-up
	parent_conn, child_conn = Pipe()
	
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
		host = options.specific_host
	else:
		host = 'localhost'
	port = 8888
	client = Client()
	client.connect(host, port)

	# GENERATE DICTIONARIES

	network_connect(client, parent_conn)

	process = Process(target=waiting_function, args=(client, child_conn, ))
	process.start()
	print "3"
	# OPEN A WAITING PROCESS

if __name__ == "__main__":
	main()
