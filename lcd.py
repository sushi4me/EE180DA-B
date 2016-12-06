#!/usr/bin/python
#
# copyright (c) 2016 Edison Vallejo
#
# References:
# http://www.instructables.com/id/Show-the-Intel-Edison-WiFi-IP-Address-on-a-Grove-L/step2/Run-the-Code/
#
# Permission is hereby granted, free of charge, to any person obtaining
#
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
import fcntl
import struct
import pyupm_i2clcd as lcd

#----------------------------
# Globals
#----------------------------
R="red"
G="green"
B="blue"

#----------------------------
# LCD Class
#----------------------------
class lcd:

	# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
	myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

	# Clear
	myLcd.clear()

	def display(self, string, posX, posY, color=None):
                myLcd.clear()
                # Green
		if color == 'green':
			self.myLcd.setColor(255, 255, 0)
		# Red
		elif color == 'red':
			self.myLcd.setColor(255, 0, 0)
		# Blue
		elif color == 'blue':
			self.myLcd.setColor(0, 0, 255)
		# Default: White
		else:
			self.myLcd.setColor(255, 255, 255)
		
                # Set the cursor
		self.myLcd.setCursor(posX,posY)
		# Print it.
		self.myLcd.write(string)


