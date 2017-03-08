#------------------------------------------------
# Module: Demo.py
# Description:
#
#------------------------------------------------
import position_estimation.position
from time				import sleep
from pythonwifi.iwlibs 	import Wireless
from Modules.OLED		import OLED
from Modules.DOF		import DOFsensor
from Modules.Globals	import buttons
from Modules.GetIP		import getIP
from position_estimation.position import sample_current_location
#----------------------------
# Globals
#----------------------------
oled = OLED()
dof = DOFsensor()
wifi = Wireless('wlan0')

#----------------------------
# Initialization
#----------------------------
oled.clear()
oled.drawInitScreen()
sleep(1)

#----------------------------
# runScan
#----------------------------
def runScan(position):
	oled.clear()
	oled.write("Position " + str(position))
	oled.write("SCANNING..")
	sample_current_location()

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
	oled.write("POS:" + str(position))
	oled.setTextCursor(1,0)
	oled.oled.write("S: SCAN   A: NEXT   B: PREV   R:MAIN MENU")
	oled.oled.refresh()
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
		mainMenu()
	runCalib(position)

#----------------------------
# showIP()
#----------------------------
def showIP():
	oled.clear()
	oled.drawBorder()
	IP = getIP('wlan0')
	oled.write(IP)
	oled.setTextCursor(3, 0)
	oled.oled.write("A: BACK   B: EXIT   ")
	oled.oled.refresh()
	incorrectInput = True
	while (incorrectInput):
		input = oled.waitForUserInput()
		incorrectInput = False
		if input == buttons.A:
			mainMenu()
		elif input == buttons.B:
			quit()
		else:
			incorrectInput = True


#----------------------------
# Main Menu
#----------------------------
def mainMenu():
	options = [" Demo", " Calib", " ShowIP", " EXIT"]
	oled.drawMainMenu(options)
	input = oled.waitForUserInput()
	incorrectInput = True
	while (incorrectInput):
		incorrectInput = False
		if input == buttons.A:
			runDemo()
		elif input == buttons.B:
			runCalib(0)
		elif input == buttons.S:
			showIP()
		elif input == buttons.D:
			quit()
		else:
			incorrectInput = True

#----------------------------
# main
#----------------------------
mainMenu()
