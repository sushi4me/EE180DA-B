#!/usr/bin/python
#------------------------------------------------
# Module: Demo.py
# Description:
#	This program will be saved under /etc/init.d/ and configured to
#	run on startup when the wearable device is turned on.  The player
#	will then be taken to a Main Menu where prompted with the options
#	to start the game or use development options (collect data/check IP)
#
#------------------------------------------------
import position_estimation.position
from time				import sleep
from Modules.OLED		import OLED
from Modules.Globals	import buttons
from Modules.GetIP		import getIP
from Miscellaneous.detect import sample_location_number
#----------------------------
# Initialization
# Description:
#	Initializes the OLED Block Display and displays 
#	the initialization Screen. Waits 1 second for 
#	smooth transition between screens
#----------------------------
oled = OLED()
oled.clear()
oled.drawInitScreen()
sleep(1)

#----------------------------
# Function: runScan
# Description:
#	This is used when in developer mode.  Developer
#	options allows for access point data collection.
#	This function will save a file with the location
#	data and additionally display the results on the
#	OLED display.
#----------------------------
def runScan(position):
	oled.clear()
	oled.drawBorder()
	oled.write("Position " + str(position))
	oled.write("SCANNING..")
	locationdata = sample_location_number(position)
	oled.clear()
	oled.write(str(locationdata))
	while True:
		input = oled.waitForUserInput()
		if input == buttons.U:
			oled.scrollUp()
		elif input == buttons.D:
			oled.scrollDown()
		else:
			break;

#----------------------------
# Function: runGame
# Description:
#	This function is run when the user is ready to 
#	begin playing the game.  This function imports
#	the client function and begins running the client
#	code for the game.
#----------------------------
def runGame():
	oled.clear()
	oled.drawBorder()
	oled.write("STARTING  GAME...")
	sleep(3)
	import Miscellaneous.client_test as client
	client.main()

#----------------------------
# Function: runDeveloper
# Description:
#	This is the UI for collecting wireless access
#	point data.  
# 
#----------------------------
def runDeveloper(position):
	oled.clear()
	oled.drawBorder()
	oled.write("POS:" + str(position))
	oled.setTextCursor(1,0)
	oled.oled.write("S: SCAN   A: NEXT   B: PREV   L: BACK")
	oled.oled.refresh()
	input = oled.waitForUserInput()
	if input == buttons.S:
		runScan(position)
	elif input == buttons.A:
		if position == 60:
			position = 0
		else:
			position += 1
		runDeveloper(position)
	elif input == buttons.B:
		if position == 0:
			position = 60
		else:
			position -= 1
		runDeveloper(position)
	elif input != buttons.L:
		runDeveloper(position)
		

#----------------------------
# Function: showIP()
# Description:
#	This a developer option to obtain IP for
#	ssh access.
#----------------------------
def showIP():
	oled.clear()
	oled.drawBorder()
	IP = getIP('wlan0')
	oled.write("IP: " + IP)
	oled.setTextCursor(4, 0)
	oled.oled.write("B: BACK")
	oled.oled.refresh()
	while True:
		input = oled.waitForUserInput()
		if input == buttons.B:
			break;


#----------------------------
# Function: mainMenu
# Description:
#	Run at startup.  Presents the user with a 
#	series of options including, START game,
#	DEVELOP options, ShowIP, and EXIT
#----------------------------
def mainMenu():
	options = [" START", " DEVELOP", " ShowIP", " EXIT"]
	refreshScreen = True
	while True:
		if refreshScreen == True:
			oled.drawMenu("Main Menu", options)
		input = oled.waitForUserInput()
		if input == buttons.A:
			runGame()
		elif input == buttons.B:
			runDeveloper(0)
		elif input == buttons.S:
			showIP()
		elif input == buttons.U:
			break;
		else:
			refreshScreen = False

#----------------------------
# main
#----------------------------
mainMenu()
