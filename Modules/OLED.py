import time
import mraa
import pyupm_i2clcd as oledObj

class OLED:
	# Instantiate new OLED object
	oled = oledObj.EBOLED()
	#----------------------------------
	# SparkFun OLED Screen Variables
	#----------------------------------
	NUM_ROWS = 6			# 6 rows per column of the OLED display
	NUM_COLS = 10			# 10 character per row of the OLED dispaly
	CURSOR_ROW = [ 0, 9, 18, 27, 36, 45 ]  # values correspond to pixels
	CURSOR_COL = [ 0, 6, 12, 18, 24, 30, 36, 42, 48, 54 ] # 
	CURSOR_POS = 0 # Takes values from [ 0, 59 ] where e.g. 13 -> (9, 12)
	MAX_CURS_POS = 59		# Text Cursor Used for writing characters
	CURRENT_PAGE = 0		# Used for scrolling
	SCREEN_BUFFER = ""		# Used for remembering the sate of the buffer
	TYPE_DELAY = 0.005		# Delay for writeScroll()
	MAX_PIXELS_COL = 64
	MAX_PIXELS_ROW = 48

	#----------------------------------
	# GPIO OLED Buttons
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
		self.SCREEN_BUFFER += string
		if self.CURSOR_POS >= self.MAX_CURS_POS:
			return
		if len(self.SCREEN_BUFFER) > self.MAX_CURS_POS:
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
		self.SCREEN_BUFFER += string
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
	#	SCREEN_BUFFER).  Additionally resets the SCREEN_BUFFER
	#	and the CURRENT_PAGE (Used to determine what page of the 
	#	SCREEN_BUFFER the user is looking at)
	#----------------------------------
	def clear(self):
		self.CURSOR_POS = 0
		self.oled.clear()
		self.oled.clearScreenBuffer()
		self.oled.setCursor(0,0)
		self.SCREEN_BUFFER = ""
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
	#	characters stored in SCREEN_BUFFER.  This module can
	#	be used in conjuction with the BUTTON_DOWN to allow the user
	#	to scroll through large messages.  This module uses
	#	CURRENT_PAGE to keep track of how much the user has 
	#	scrolled down.  
	#----------------------------------
	def scrollDown(self):
		buffer_size = len(self.SCREEN_BUFFER)
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
			self.oled.write(self.SCREEN_BUFFER[self.CURRENT_PAGE*self.NUM_COLS:])
			self.oled.refresh()

	#----------------------------------
	# Module: scrollUp(self)
	# Description:
	#	This module scrolls the display up according to the 
	#	characters stored in SCREEN_BUFFER.  This module can
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
		self.oled.write(self.SCREEN_BUFFER[self.CURRENT_PAGE*self.NUM_COLS:])
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
	# Module: drawMap(self)
	# Description:
	#
	#----------------------------------
	def drawMap(self):
		self.clear()
		# Draw outline
		self.oled.drawRoundedRectangle(0, 0, self.MAX_PIXELS_COL, self.MAX_PIXELS_ROW, 4, 1)
                self.oled.setCursor(3,3)
                self.oled.write("EIV")
		# Draw map
		grid = [" " for y in range(self.MAX_PIXELS_ROW)]
		grid[0] = "                           |                                    "
		grid[1] = "                           |                                    "
		grid[2] = "                           |                                    "
		grid[3] = "                           |                                    "
		grid[4] = "                           |                                    "
		grid[5] = "                           |     __________________________     "
		grid[6] = "                           |     |                        |     "
		grid[7] = "                           |     |                        |     "
		grid[8] = "                           |     |                        |     "
		grid[9] = "                           |     |                        |     "
		grid[10]= "                           |     |                        |     "
		grid[11]= "                           |     |                        |     "
		grid[12]= "                           |     |                        |     "
		grid[13] ="----------------------------     |                        |     "
		grid[14] ="                                 |                        |     "
		grid[15] ="                                 |                        |     "
		grid[16] ="                                 |                        |     "
		grid[17] ="                                 |                        |     "
		grid[18] ="                                 |                        |     "
		grid[19] ="     ____________________________|                        |     "
		grid[20] ="     |                                                    |     "
		for i in range(21, 42):
			grid[i] = grid[20]
		grid[42] ="     |                                                    |     "
		grid[43] ="     ------------------------------------------------------     "
		x = 0
		y = 0
		for i in grid:
			x = 0
			for j in i:
				if j != " ":
					self.oled.drawPixel(x, y, 1)
					self.oled.refresh()
				x += 1
			y += 1
        
	def updateMap(self, position):
    	# need to implement
        self.oled.drawCircle(46, 61, 2, 1)
        self.oled.refresh()
