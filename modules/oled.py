import pyupm_i2clcd as oledObj

class OLED:
	oled = oledObj.EBOLED()

	def write(self, string):
		self.oled.write(string)

	def clear(self):
		self.oled.clear()

	
