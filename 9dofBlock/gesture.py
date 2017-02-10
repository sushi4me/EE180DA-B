#!/usr/bin/python
#---------------------------------
# Modules
#---------------------------------
from SF_9DOF import IMU
from subprocess import call
import time

#---------------------------------
# Globals
#---------------------------------
# Occurence Threshold for gesture occured
SLEEP_TIME = 0.05

# Gesture 1 Constants
#--------------------
gesturedetected = 0
gestureoccured = 9
# Position Threshold to start recording gesture
posthreshold = 0.8
negthreshold = -0.8
count = 0
occurence = 0

# Gesture 2 Constants
#--------------------


#---------------------------------
# Initialize IMU
#---------------------------------

# Create IMU object
imu = IMU() # To select a specific I2C port, use IMU(n). Default is 1. 

# Initialize IMU
imu.initialize()

# Enable accel, mag, gyro, and temperature
imu.enable_accel()
imu.enable_mag()
imu.enable_gyro()
imu.enable_temp()

# Set range on accel, mag, and gyro

# Specify Options: "2G", "4G", "6G", "8G", "16G"
imu.accel_range("2G")       # leave blank for default of "2G" 

# Specify Options: "2GAUSS", "4GAUSS", "8GAUSS", "12GAUSS"
imu.mag_range("2GAUSS")     # leave blank for default of "2GAUSS"

# Specify Options: "245DPS", "500DPS", "2000DPS" 
imu.gyro_range("245DPS")    # leave blank for default of "245DPS"

#----------------------------------
# run Module
#----------------------------------
def run():
	# Loop and read accel, mag, and gyro
	while(1):
    		imu.read_accel()
    		imu.read_gyro()

    		if imu.az > posthreshold:
        		occurence += 1
    		elif imu.az < negthreshold:
        		occurence -= 1
    		else:
        		count += 1
    
    		if abs(occurence) >= gestureoccured:
        		print "gesture received"
        		occurence = 0
        		count = 0
    
    		if count > 5:
        		occurence = 0
        		count = 0

    		# Sleep for SLEEP_TIME seconds
    		time.sleep(SLEEP_TIME)


def reset():
	# Reset gesturedetected value
	gesturedetected = 0
