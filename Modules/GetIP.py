#!/usr/bin/python

import socket
import fcntl
import struct
import time
from time import gmtime, strftime
import datetime

def getIP('wlan0'):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', wlan0[:15])
        )[20:24])


