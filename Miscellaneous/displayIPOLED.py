#!/usr/bin/python

import socket
import fcntl
import struct
import time
from time import gmtime, strftime
import datetime
import mraa
import pyupm_i2clcd as oledObj

def get_ip_address(ifname):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])


time.sleep(20)

led = oledObj.EBOLED()
led.setTextWrap(1)

# Obtain IP Address
ip_address = get_ip_address('wlan0')

# Print the date and IP address every 10 seconds 
while [ 0 ]:
    # Clear the screen and screen buffer
    led.clear()
    led.clearScreenBuffer()
    # Reset the Cursor to the top left
    led.setCursor(0,0)
    # Retrieve current time
    tstamp = datetime.datetime.now()
    # Hour and minute should always consist of two digits
    if tstamp.minute < 10:
        timeminute = "0" + str(tstamp.minute)
    else:
        timeminute = str(tstamp.minute)
    if tstamp.hour < 10:
        timehour = "0" + str(tstamp.hour)
    else:
        timehour = str(tstamp.hour)
    # catenate the time string
    currentTime = timehour + ":" + timeminute
    # Print the time onto the LED
    led.write(currentTime)
    # Move the cursor down one row
    led.setCursor(10, 0)
    # Print the IP Address
    led.write(ip_address)
    # Refresh updates the display
    led.refresh()
    # Update the time every 10 seconds
    time.sleep(10)
