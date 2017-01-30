#!/usr/bin/python
#
# copyright (c) 2016 Edison Vallejo
#
# References:
# http://www.instructables.com/id/Show-the-Intel-Edison-WiFi-IP-Address-on-a-Grove-L/step2/Run-the-Code/
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#----------------------------
# Modules
#----------------------------
import pyupm_i2clcd as lcd
import time
#----------------------------
# Globals
#----------------------------
R="red"
G="green"
B="blue"
P="pink"
Y="yellow"
T="teal"
OFF="off"
#----------------------------
# LCD Class
#----------------------------
class lcd:

	# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
	myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

	# Clear
	myLcd.clear()
       
        # Takes 4 Parameters: string, posX, posY, color=DefaultWhite
	def display(self, string, posX, posY, color=None):
		# Clear
		self.myLcd.clear()
                # Green
		if color == G:
			self.myLcd.setColor(0, 255, 0)
		# Red
		elif color == R:
			self.myLcd.setColor(100, 0, 0)
		# Blue
		elif color == B:
			self.myLcd.setColor(25, 25, 255)
                # Pink
		elif color == P:
			self.myLcd.setColor(255, 0, 255)
		# Teal
		elif color == T:
			self.myLcd.setColor(0, 255, 255)
		# Yellow
		elif color == Y:
			self.myLcd.setColor(255, 255, 0)
                # OFF
                elif color == OFF:
                        self.myLcd.setColor(0, 0, 0)
                # Default: White
		else:
			self.myLcd.setColor(255, 255, 255)
                # Set the cursor
		self.myLcd.setCursor(posX,posY)
		# Print it.
		self.myLcd.write(string)
                # OFF
                if color == OFF:
                    self.myLcd.clear()

        def gameStatus(self, string):
            self.display(string, 0, 0, Y)
        
        def capturedFlag(self):
            self.display("CAPTURED FLAG!", 0, 0, G)
        
        def droppedFlag(self):
            self.display("DROPPED FLAG!", 0, 0, R)

        def frozen(self):
            self.display("FROZEN! burr!", 0, 0, B)

        def gotPowerUp(self, string):
            message = string + " POWERUP!"
            sleeptime = 0.2
            posY=0
            for posY in range(0, 1):
                posX = 0
                for posX in range(0,7):
                    self.display(message, 0, 0, R)
                    time.sleep(sleeptime)
                    self.display(message, 0, 0, G)
                    time.sleep(sleeptime)
                    self.display(message, 0, 0, B)
                    time.sleep(sleeptime)
                    self.display(message, 0, 0, P)
                    time.sleep(sleeptime)
                    self.display(message, 0, 0, Y)
                    time.sleep(sleeptime)
                    self.display(message, 0, 0, T)
                    time.sleep(sleeptime)
                    posX += 1
            posY += 1
