#------------------------------------------------
# Module: Demo.py
# Description:
#
#------------------------------------------------
from time				import sleep
from pythonwifi.iwlibs 	import Wireless
from Modules.OLED		import OLED
from Modules.DOF		import DOF
from Modules.Globals	import buttons
from Modules.GetIP		import getIP
from position_estimation import sample_current_location
#----------------------------
# Globals
#----------------------------
oled = OLED()
dof = DOF()
wifi = Wireless('wlan0')

#----------------------------
# Initialization
#----------------------------
oled.clear()
oled.drawInitScreen()
time.sleep(3)

#----------------------------
# runScan
#----------------------------
def runScan(position):
	oled.clear()
	oled.write("Position " + position)
	oled.write("SCANNING..")
	sample_current_location(1)

#----------------------------
# runDemo
#----------------------------
def runDemo():
	oled.clear()
	oled.write("STARTING  DEMO...")
	sleep(3)
	mainMenu()	

#----------------------------
# runCalib()
#----------------------------
def runCalib(position):
	oled.clear()
	oled.drawBorder()
	oled.write("POS:" + position)
	oled.write("S: SCAN    A: NEXT   B: PREV   R: EXIT")
	input = oled.waitForUserInput()
	if input == buttons.S:
		runScan(position)
	elif input == buttons.A:
		position += 1
	elif input == buttons.B:
		if position > 0:
			position -= 1
		else:
			position = 0
	elif input == buttons.R:
		quit()
	runCalib(position)
#----------------------------
# showIP()
#----------------------------
def showIP():
	oled.clear()
	oled.drawBorder()
	IP = getIP()
	oled.write(IP + "       ")
	oled.write("A: BACK   B: EXIT   ")
	input = oled.waitForUserInput()
	if input == buttons.A:
		mainMenu()
	if input == buttons.B:
		quit()

#----------------------------
# Main Menu
#----------------------------
def mainMenu():
	options = [" Demo", " Calib", "ShowIP", "EXIT"]
	oled.drawMainMenu(options)
	input = oled.waitForUserInput()
	incorrectInput = True
	while (incorrectInput):
		incorrectInput = False
		if input == buttons.A:
			runDemo()
		elif input == buttons.B:
			runCalib(0)
		elif input == buttons.SELECT:
			showIP()
		elif input == buttons.DOWN:
			quit()
		else:
			incorrectInput = True

#----------------------------
# main
#----------------------------
mainMenu()
