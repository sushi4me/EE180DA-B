import time
import mraa
import pyupm_i2clcd as oledObj

class OLED:
	oled = oledObj.EBOLED()
	
	BUTTON_UP = 	mraa.Gpio(47, owner=False, raw=True)
	BUTTON_DOWN = 	mraa.Gpio(44, owner=False, raw=True)
	BUTTON_LEFT = 	mraa.Gpio(165, owner=False, raw=True)
	BUTTON_RIGHT = 	mraa.Gpio(45, owner=False, raw=True)
	BUTTON_SELECT = mraa.Gpio(48, owner=False, raw=True)
	BUTTON_A = 	mraa.Gpio(49, owner=False, raw=True)
	BUTTON_B = 	mraa.Gpio(46, owner=False, raw=True)

	BUTTON_UP.dir(mraa.DIR_IN)
	BUTTON_DOWN.dir(mraa.DIR_IN)
	BUTTON_LEFT.dir(mraa.DIR_IN)
	BUTTON_RIGHT.dir(mraa.DIR_IN)
	BUTTON_SELECT.dir(mraa.DIR_IN)
	BUTTON_A.dir(mraa.DIR_IN)
	BUTTON_B.dir(mraa.DIR_IN)

	def __init__(self):
	    self.oled.setTextWrap(1)
	    self.oled.clear()

	def write(self, string):
            self.oled.write(string)
            self.oled.refresh()

        def clear(self):
            self.oled.clear()
            self.oled.clearScreenBuffer()

        def resetCursor(self):
            self.oled.setCursor(0,0)

        def run(self):
            while(1):
                self.clear()
                if int(self.BUTTON_UP.read()) != 0:
                    self.write("UP > 0")
                if int(self.BUTTON_DOWN.read()) != 0:
                    self.write("DOWN > 0")
                self.resetCursor()
                time.sleep(0.5)

