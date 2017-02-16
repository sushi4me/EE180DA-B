#----------------------------
# Imported Modules
#----------------------------
import gesture as ges
from OLED import OLED
from Buzzer import Buzzer
import time

#----------------------------
# Globals
#----------------------------
ledHeader = "getFlag();\n"
display = OLED()
audio = Buzzer()
display.clear()
display.resetCursor()
display.write(ledHeader)
audio.connected()
time.sleep(1)
#----------------------------
# Print Initialization to LED
#----------------------------
buzz = [ 0 ]
buzzfinal = [ 4 ]
microsec = [ 16 ]
for i in range (0, 3):
    message = ledHeader + "Starting\n\t\t\t" + str(3 - i)
    display.clear()
    display.resetCursor()
    display.write(message)
    audio.play(buzz, microsec)
    time.sleep(0.7)
display.clear()
display.resetCursor()
display.write(ledHeader)
audio.play(buzzfinal, microsec)
#----------------------------
# Gesture Detection
#----------------------------
while True:
    x = ges.run()
    if x == 1:
        message = ledHeader + "Freeze!!!"
        display.clear()
        display.resetCursor()
        display.write(message)
        audio.shoot()
    elif x == 2:
        message = ledHeader + "Cloak!!!"
        display.clear()
        display.resetCursor()
        display.write(message)
        audio.disconnected()
    else:
        display.clear()

