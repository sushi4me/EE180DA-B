#------------------------------------------------
# Module: OLED.py
# Description:
#
#------------------------------------------------
import time
import mraa
import pyupm_i2clcd as oledObj
from Globals import buttons

#--------------------------------------
# OLED Class (Sparkfun OLED Block)
#--------------------------------------
class OLED:
	# Instantiate new OLED object
	oled = oledObj.EBOLED()
	#----------------------------------
	# SparkFun OLED Screen Variables
	#----------------------------------
	MAX_PIXELS_COL = 64
	MAX_PIXELS_ROW = 48
	NUM_ROWS = 6			# 6 rows per column of the OLED display
	NUM_COLS = 10			# 10 character per row of the OLED dispaly
	CURSOR_ROW = [ 2, 11, 20, 29, 38, 47 ]  # values correspond to pixels
	CURSOR_COL = [ 2, 8, 14, 20, 26, 32, 38, 44, 50, 56 ] # 
	CURSOR_POS = 0 # Takes values from [ 0, 59 ] where e.g. 13 -> (9, 12)
	MAX_CURS_POS = 59		# Text Cursor Used for writing characters
	CURRENT_PAGE = 0		# Used for scrolling
	TEXT_BUFFER = ""		# Used for remembering the text in the screen buffer
	PIXEL_BUFFER = [ " " for i in range(MAX_PIXELS_ROW)] # Used to remember pixel screen state
	TYPE_DELAY = 0.005		# Delay for writeScroll()

	#----------------------------------
	# GPIO OLED Block Buttons
	#----------------------------------
	BUTTON_UP = 	mraa.Gpio(46)
	BUTTON_DOWN = 	mraa.Gpio(31)
	BUTTON_LEFT = 	mraa.Gpio(15)
	BUTTON_RIGHT = 	mraa.Gpio(45)
	BUTTON_SELECT = mraa.Gpio(33)
	BUTTON_A = 	mraa.Gpio(47)
	BUTTON_B = 	mraa.Gpio(32)

	BUTTON_UP.dir(mraa.DIR_IN)
	BUTTON_DOWN.dir(mraa.DIR_IN)
	BUTTON_LEFT.dir(mraa.DIR_IN)
	BUTTON_RIGHT.dir(mraa.DIR_IN)
	BUTTON_SELECT.dir(mraa.DIR_IN)
	BUTTON_A.dir(mraa.DIR_IN)
	BUTTON_B.dir(mraa.DIR_IN)

	#----------------------------------
	# Class Initialization
	#----------------------------------
	def __init__(self):
		self.oled.setTextWrap(1)
		self.oled.clear()

	#----------------------------------
	# Method: int row(self)
	# Description:
	#	The setCursor() method in the pyupm_i2dlcd module 
	#	indexes the rows each by pixel location in the range [0, 48]
	#	The row method returns the pixel value of the Current
	#	position of the cursor.  Each character row begins in the following
	#	y range pixels respectively (0, 9, 18, 27, 36, 45)
	#----------------------------------
	def row(self):
		r = min(self.CURSOR_POS//self.NUM_COLS, self.NUM_ROWS - 1)
		return self.CURSOR_ROW[r]

	#----------------------------------
	# Method: int col(self)
	# Description:
	#	The setCursor() method in the pyupm_i2dlcd module 
	#	indexes the columns each by pixel location in the range [0, 64]
	#	The col method returns the pixel value of the Current
	#	position of the cursor.  Each character column begins in the following
	#	x range pixels respectively (0, 6, 12, 18, 24, 30, 36, 42, 48, 54)
	#----------------------------------
	def col(self):
		c = min(self.CURSOR_POS%self.NUM_COLS, self.NUM_COLS - 1)
		return self.CURSOR_COL[c]

	#----------------------------------
	# Method: write(self, string)
	# Description:
	#	Differs from the pyupm write function as it refreshes the OLED
	#	display each time it is called and it keeps track of the position
	#	of the cursor.  The write function also keeps track of the screen 
	#	buffer allowing for each character to be written at a time or a 
	#	full message all at once. The screen buffer is essential for allowing 
	#	the user to scroll using the OLED Block Joystick when the messages 
	#	are too long to fit in the (5 x 10) rows/columns. 
	#	The screen buffer continues to grow with each call to write()
	#	or writeScroll() and only gets cleared when clear() is called.
	#	write() uses a member variable called CURSOR_POS to keep track
	#	of the current position of the cursor for future calls to write()
	#	CURSOR_POS takes values [0, 59] inclusively, corresponding to the
	#	number of characters that can fit on the display.
	#----------------------------------	
	def write(self, string):
		self.TEXT_BUFFER += string
		if self.CURSOR_POS >= self.MAX_CURS_POS:
			return
		if len(self.TEXT_BUFFER) > self.MAX_CURS_POS:
			self.oled.setCursor(self.row(), self.col())
			self.oled.write(string[self.CURSOR_POS : self.MAX_CURS_POS])
			self.oled.refresh()	
		else:
			self.oled.setCursor(self.row(), self.col())
			self.oled.write(string)
			self.oled.refresh()
		self.CURSOR_POS += len(string)

	#----------------------------------
	# Method: writeScroll(self,string)
	# Description:
	#	Exactly the same as write() with the exception that it writes
	#	each character at a time with a delay, so to appear as if the 
	#	message is being typed out each character at a time.
	#----------------------------------
	def writeScroll(self, string):
		self.TEXT_BUFFER += string
		for i in string:
			if self.CURSOR_POS > self.MAX_CURS_POS:
				return
			self.oled.setCursor(self.row(), self.col())
			self.oled.write(i)
			self.oled.refresh()
			time.sleep(self.TYPE_DELAY)
			self.CURSOR_POS += 1

	#----------------------------------
	# Module: clear(self)
	# Description:
	#	Clears the screen, resets the position of the cursor, and 
	#	clears the OLED screen buffer (which is different from the 
	#	TEXT_BUFFER).  Additionally resets the TEXT_BUFFER
	#	and the CURRENT_PAGE (Used to determine what page of the 
	#	TEXT_BUFFER the user is looking at)
	#----------------------------------
	def clear(self):
		self.CURSOR_POS = 0
		self.oled.clear()
		self.oled.clearScreenBuffer()
		self.oled.setCursor(0,0)
		self.TEXT_BUFFER = ""
		self.CURRENT_PAGE = 0

	#----------------------------------
	# Module: setTextCursor
	# Description:
	#	The OLED display fits 6 rows of characters by 10 columns of 
	#	characters.  The pyupm setCursor() enables to set the cursor 
	#	at any given pixel in contrast with this module that enables
	#	the user to set the cursor at a specific (row,col) that are
	#	index based on the set size of all characters.
	#----------------------------------
	def setTextCursor(self, row, col):
		r = min(row, self.NUM_ROWS - 1)
		c = min(col, self.NUM_COLS - 1)
		self.oled.setCursor(self.CURSOR_ROW[r], self.CURSOR_COL[c])

	#----------------------------------
	# Module: scrollDown(self)
	# Description:
	#	This module scrolls the display down according to the 
	#	characters stored in TEXT_BUFFER.  This module can
	#	be used in conjuction with the BUTTON_DOWN to allow the user
	#	to scroll through large messages.  This module uses
	#	CURRENT_PAGE to keep track of how much the user has 
	#	scrolled down.  
	#----------------------------------
	def scrollDown(self):
		buffer_size = len(self.TEXT_BUFFER)
		num_pages = -(-buffer_size//self.NUM_COLS) - 5
		if buffer_size < self.MAX_CURS_POS:
			return
		elif num_pages <= self.CURRENT_PAGE:
			return
		else:
			self.CURRENT_PAGE += 1
			self.oled.clear()
			self.oled.clearScreenBuffer()
			self.oled.home()
			self.oled.write(self.TEXT_BUFFER[self.CURRENT_PAGE*self.NUM_COLS:])
			self.oled.refresh()

	#----------------------------------
	# Module: scrollUp(self)
	# Description:
	#	This module scrolls the display up according to the 
	#	characters stored in TEXT_BUFFER.  This module can
	#	be used in conjuction with the BUTTON_UP to allow the user
	#	to scroll through large messages.  This module uses
	#	CURRENT_PAGE to keep track of how much the user has 
	#	scrolled up.
	#----------------------------------
	def scrollUp(self):
		if self.CURRENT_PAGE == 0:
			return
		self.CURRENT_PAGE -= 1
		self.oled.clear()
		self.oled.clearScreenBuffer()
		self.oled.home()
		self.oled.write(self.TEXT_BUFFER[self.CURRENT_PAGE*self.NUM_COLS:])
		self.oled.refresh()

	#----------------------------------
	# Module: getUserInput(self)
	# Description:
	#	waits and listens for user input.  Immediately returns
	#	when the user has pressed any of the buttons. Returns a
	#	char that corresponds with the button that was pressed.
	#---------------------------------- 
	def waitForUserInput(self):
		while(self.BUTTON_A.read() != 0 and self.BUTTON_B.read() != 0 and 
			self.BUTTON_SELECT.read() != 0 and self.BUTTON_DOWN.read() != 0 and
			self.BUTTON_LEFT.read() != 0 and self.BUTTON_RIGHT.read() != 0 and 
			self.BUTTON_UP.read() != 0):
			pass
		if (self.BUTTON_A.read() == 0):
			return "A"
		if (self.BUTTON_B.read() == 0):
			return "B"
		if (self.BUTTON_SELECT.read() == 0):
			return "S"
		if (self.BUTTON_UP.read() == 0):
			return "U"
		if (self.BUTTON_DOWN.read() == 0):
			return "D"
		if (self.BUTTON_LEFT.read() == 0):
			return "L"
		if (self.BUTTON_RIGHT.read() == 0):
			return "R"

	#----------------------------------
	# Module: drawBorder(self)
	# Description:
	#	Draws a rounded rectangular border
	#	onto the edges of the screen
	#----------------------------------
	def drawBorder(self):
		self.oled.drawRoundedRectangle(0, 0, self.MAX_PIXELS_COL, self.MAX_PIXELS_ROW, 4, 1)
		self.oled.refresh()

	#----------------------------------
	# Module: drawScreen(self, ArrayofStrings, delay)
	# Description:
	# 	Each pixel that is drawn corresponds to a character
	# 	other than the SPACE character.  The ArrayofStrings
	#	can have maximum index of MAX_PIXELS_ROW and each
	#	string in the array can have maximum length of
	#	MAX_PIXELS_COL. Delay parameter is used to inidiate
	#	the screen to be refreshed after drawing each pixel.
	#	This option can be used as a delay while game
	#	initialization takes place
	#----------------------------------
	def drawScreen(self, ArrayOfStrings, delay=0):
		self.PIXEL_BUFFER = ArrayOfStrings
		x = 0
		y = 0
		# For each string in the array
		for i in ArrayOfStrings:
			x = 0
			# For each character in the string
			for j in i:
				# Any character other than space 
				# corresponds to a pixel drawn on the map
				if j != " ":
					self.oled.drawPixel(x, y, 1)
					if delay == 1:
						self.oled.refresh()
				x += 1
			y += 1
		self.oled.refresh()

	#----------------------------------
	# Module: drawInitScreen(self)
	# Description:
	# 	Draws game initialization screen
	#----------------------------------
	def drawInitScreen(self):
		self.drawBorder()
		grid = [" " for y in range(self.MAX_PIXELS_ROW)]
		grid[self.MAX_PIXELS_ROW//2 - 9] = "                    ****          ******                        "
		grid[self.MAX_PIXELS_ROW//2 - 8] = "                    * * **      **      **                      "
		grid[self.MAX_PIXELS_ROW//2 - 7] = "                    * *   ******          **                    "
		grid[self.MAX_PIXELS_ROW//2 - 6] = "                    * *                    *                    "
		grid[self.MAX_PIXELS_ROW//2 - 5] = "                    * *                    *                    "
		grid[self.MAX_PIXELS_ROW//2 - 4] = "                    * *                    *                    "
		grid[self.MAX_PIXELS_ROW//2 - 3] = "                    * *                    *                    "
		grid[self.MAX_PIXELS_ROW//2 - 2] = "                    * *                    *                    "
		grid[self.MAX_PIXELS_ROW//2 - 1] = "                    * *                    *                    "
		grid[self.MAX_PIXELS_ROW//2 - 0] = "                    * *                    *                    "
		grid[self.MAX_PIXELS_ROW//2 + 1] = "                    * *                    *                    "
		grid[self.MAX_PIXELS_ROW//2 + 2] = "                    * *                    *                    "
		grid[self.MAX_PIXELS_ROW//2 + 3] = "                    * **          ******   *                    "
		grid[self.MAX_PIXELS_ROW//2 + 4] = "                    * * **      **      ** *                    "
		grid[self.MAX_PIXELS_ROW//2 + 5] = "                    * *   ******          **                    "
		grid[self.MAX_PIXELS_ROW//2 + 6] = "                    * *                                         "
		grid[self.MAX_PIXELS_ROW//2 + 7] = "                    * *                                         "
		grid[self.MAX_PIXELS_ROW//2 + 8] = "                    * *                                         "
		grid[self.MAX_PIXELS_ROW//2 + 9] = "                    ***                                         "
		self.drawScreen(grid, 1)

	#----------------------------------
	# Module: drawStartScreen(self)
	# Description:
	#	Draws the game main menu, allowing the
	#	user to indicate they are ready to start
	#	or navigate the options.  This module
	#	returns the value the user select
	#----------------------------------
	def drawStartScreen(self):
		self.drawBorder()
		self.setTextCursor(0, 0)
		self.oled.write("Main Menu")
		self.oled.drawLineHorizontal(0, 10, 64, 1)
		self.setTextCursor(2, 0)
		self.oled.write("(A) Start")
		self.setTextCursor(3, 0)
		self.oled.write("(B) Option")
		self.oled.refresh()
		input = self.waitForUserInput()
		while (input != "A"):
			if input == "B":
				# Initialize options menu
				pass
			input = self.waitForUserInput()

	#----------------------------------
	# Module: drawEIVMap(self)
	# Description:
	#	Clears the screen before drawing the map
	#	Draws a map of UCLA EIV 4th Floor
	# 	with map position indices
	#----------------------------------
	def drawEIVMap(self):
		# Clear Screen
		self.oled.clearScreenBuffer()
		self.oled.clear()
		# Draw outline
		self.drawBorder()
		self.oled.setCursor(3,3)
		self.oled.write("EIV")
		
		# Initialize MAP array of strings
		grid = [" " for y in range(self.MAX_PIXELS_ROW)]
		grid[0] = "                      |                                         "
		for i in range(1,9):
			grid[i] = grid[0]
		grid[9] = "                      |                                         "
		grid[10]= "                      |          _____________________          "
		grid[11]= "                      |          |                   |          "
		grid[12]= "                      |          |                   |          "
		grid[13]= "                      |          |                   |          "
		grid[14]= "-----------------------          |                   |          "
		grid[15]= "                                 |                   |          "
		for i in range(16, 25):
			grid[i] = grid[15]
		grid[25] ="          _______________________|                   |          "
		grid[26] ="          |                                          |          "
		for i in range(27, 37):
			grid[i] = grid[26]
		grid[37] ="          |                                          |          "
		grid[38] ="          --------------------------------------------          "

		# Draw EIV Map
		self.drawScreen(grid)
		
		# Draw Map Position References
		self.oled.setCursor(39, 56)
		self.oled.write("0")
		self.oled.setCursor(39, 2)
		self.oled.write("17")
		self.oled.setCursor(16, 2)
		self.oled.write("25")
		self.oled.setCursor(16, 22)
		self.oled.write("35")
		self.oled.setCursor(2, 24)
		self.oled.write("42")
		self.oled.setCursor(2, 48)
		self.oled.write("47")
		self.oled.refresh()

	#----------------------------------
	# Position to pixel (row and column) mapping
	#----------------------------------
	POS = [{'ROW': 43, 'COL': 58}, {'ROW': 43, 'COL': 53}, {'ROW': 43, 'COL': 50}, {'ROW': 43, 'COL': 47}, {'ROW': 43, 'COL': 44},
	{'ROW': 43, 'COL': 41}, {'ROW': 43, 'COL': 38}, {'ROW': 43, 'COL': 35}, {'ROW': 43, 'COL': 32}, {'ROW': 43, 'COL': 29},
	{'ROW': 43, 'COL': 26}, {'ROW': 43, 'COL': 22}, {'ROW': 43, 'COL': 19}, {'ROW': 43, 'COL': 16}, {'ROW': 43, 'COL': 13},
	{'ROW': 43, 'COL': 10}, {'ROW': 43, 'COL': 7}, {'ROW': 43, 'COL': 5}, {'ROW': 41, 'COL': 5}, {'ROW': 38, 'COL': 5},
	{'ROW': 35, 'COL': 5}, {'ROW': 32, 'COL': 5}, {'ROW': 29, 'COL': 5}, {'ROW': 26, 'COL': 5}, {'ROW': 23, 'COL': 5},
	{'ROW': 20, 'COL': 5}, {'ROW': 20, 'COL': 7}, {'ROW': 20, 'COL': 10}, {'ROW': 20, 'COL': 12}, {'ROW': 20, 'COL': 15},
	{'ROW': 20, 'COL': 17}, {'ROW': 20, 'COL': 20}, {'ROW': 20, 'COL': 22}, {'ROW': 20, 'COL': 24}, {'ROW': 20, 'COL': 26},
	{'ROW': 20, 'COL': 28}, {'ROW': 18, 'COL': 28}, {'ROW': 16, 'COL': 28}, {'ROW': 14, 'COL': 28}, {'ROW': 12, 'COL': 28},
	{'ROW': 10, 'COL': 28}, {'ROW': 8, 'COL': 28}, {'ROW': 5, 'COL': 28}, {'ROW': 5, 'COL': 34}, {'ROW': 5, 'COL': 40},
	{'ROW': 5, 'COL': 46}, {'ROW': 5, 'COL': 52}, {'ROW': 5, 'COL': 58}, {'ROW': 7, 'COL': 58}, {'ROW': 10, 'COL': 58},
	{'ROW': 12, 'COL': 58}, {'ROW': 15, 'COL': 58}, {'ROW': 17, 'COL': 58}, {'ROW': 19, 'COL': 58}, {'ROW': 21, 'COL': 58},
	{'ROW': 23, 'COL': 58}, {'ROW': 26, 'COL': 58}, {'ROW': 29, 'COL': 58}, {'ROW': 31, 'COL': 58}, {'ROW': 34, 'COL': 58},
	{'ROW': 37, 'COL': 58}, {'ROW': 40, 'COL': 58}]
	# Current Player Position in the map
	PLAYER_POS = 0

	#----------------------------------
	# Module: updateMap(self, position)
	# Description:
	# 	drawEIVMap(self) should be called before this module.
	# 	This module updates the location of the player without
	#	having to redraw the map.  The module takes a parameter
	# 	named position that takes values in the range [0, 60]
	#----------------------------------
	def updateMap(self, position):
		# Erase Old Location
		self.oled.drawCircleFilled(self.POS[self.PLAYER_POS]['COL'], self.POS[self.PLAYER_POS]['ROW'], 2, 0)
		# Draw New Location
		self.PLAYER_POS = position
		self.oled.drawCircleFilled(self.POS[self.PLAYER_POS]['COL'], self.POS[self.PLAYER_POS]['ROW'], 2, 1)
		# ReDraw Map Position References
		self.oled.setCursor(39, 56)
		self.oled.write("0")
		self.oled.setCursor(39, 2)
		self.oled.write("17")
		self.oled.setCursor(16, 2)
		self.oled.write("25")
		self.oled.setCursor(16, 22)
		self.oled.write("35")
		self.oled.setCursor(2, 24)
		self.oled.write("42")
		self.oled.setCursor(2, 48)
		self.oled.write("47")
		self.oled.refresh()

	def rotateScreenRight(self):
		self.oled.clear()
		self.oled.clearScreenBuffer()
		self.drawBorder()
		x = 0
		y = 0
		# For each string in the array
		for i in reversed(self.PIXEL_BUFFER):
			y = 0
			index = 0
			# For each character in the string
			for j in i:
				# Any character other than space 
				# corresponds to a pixel drawn on the map
				if j != " ":
					self.oled.drawPixel(x, y, 1)
					if x%4 == 1:
						self.oled.drawPixel(x+1, y, 1)
				if index%3 != 1:
					y += 1
				index += 1
			if x%4 == 1:
				x += 1
			x += 1
		self.oled.refresh()

	def rotateScreenLeft(self):
		self.oled.clear()
		self.oled.clearScreenBuffer()
		self.drawBorder()
		x = 0
		y = 0
		# For each string in the array
		for i in self.PIXEL_BUFFER:
			y = 0
			index = 0
			# For each character in the string
			for j in reversed(i):
				# Any character other than space 
				# corresponds to a pixel drawn on the map
				if j != " ":
					self.oled.drawPixel(x, y, 1)
					if x%4 == 1:
						self.oled.drawPixel(x+1, y, 1)
				if index%3 != 1:
					y += 1
				index += 1
			if x%4 == 1:
				x += 1
			x += 1
		self.oled.refresh()

	def rotateScreenTwice(self):
		self.oled.clear()
		self.oled.clearScreenBuffer()
		self.drawBorder()
		x = 0
		y = 0
		# For each string in the array
		for i in reversed(self.PIXEL_BUFFER):
			x = 0
			# For each character in the string
			for j in reversed(i):
				# Any character other than space 
				# corresponds to a pixel drawn on the map
				if j != " ":
					self.oled.drawPixel(x, y, 1)
				x += 1
			y += 1
		self.oled.refresh()


	def drawMainMenu(self, optionsList):
		self.clear()
		self.drawBorder()
		self.oled.drawLineHorizontal(0, 10, 64, 1)
		self.oled.setCursor(2, 2)
		self.oled.write("Main Menu")
		rowIndex = 1
		for option in optionsList:
			if rowIndex < self.NUM_ROWS:
				self.oled.setCursor(self.CURSOR_ROW[rowIndex], 2)
				self.oled.write(button[rowIndex - 1].name + option)
			rowIndex += 1
		self.oled.refresh()

