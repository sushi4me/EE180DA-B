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

	def write(self, string):
		self.oled.write(string)

	def clear(self):
		self.oled.clear()

	
