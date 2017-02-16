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
# Position Threshold to start recording gesture

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
	
    # Gesture  Constants
    #--------------------
    gesturedetected = 0  #1 = freeze; 2 = cloak
    gestureoccured = 9
    downcount1 = 0
    downcount1z = 0
    downcount2 = 0
    downcount2y = 0
    prereq1 = 0
    prereq2 = 0
    occurence1 = 0
    occurence2 = 0

    # Position Threshold to start recording gesture
    threshold1_az = 0.85
    threshold1low_az = 0.20
    threshold2_ax = -.85  
    threshold2_ay = -.85
    # Loop and read accel, and gyro
    while(1):
        imu.read_accel()
    	imu.read_gyro()
        
        # Gesture 1 Detection
    	if imu.az > threshold1_az:
            if imu.ax < 0 and imu.ax > -4:
                occurence1 += prereq1
                downcount1 = 0
    	else:
            downcount1 += 1
    
        if imu.az > threshold1low_az:
            downcount1z += 1
        else:
            downcount1z = 0
            prereq1 = 1

    	if occurence1 >= gestureoccured:
            return 1
            gesturedetected = 1
            occurence1 = 0
            downcount1 = 0
            prereq1 = 0
    
    	if downcount1 > 5:
            occurence1 = 0
            downcount1 = 0

        if downcount1z > 11:
            occurence1 = 0
            prereq1 = 0

        #Gesture 2 Detection
        if imu.ax <= threshold2_ax:
            if imu.az < 2 and imu.az > -2:
                occurence2 += prereq2
                downcount2 = 0
        else:
            downcount2 += 1
        
        if imu.ay > threshold2_ay:
            downcount2y += 1
        else:
            downcount2y = 0
            prereq2 = 1

        if occurence2 >= gestureoccured:
            return 2
            gesturedetected = 2
            occurence2 = 0
            downcount2 = 0
            prereq2 = 0

        if downcount2 > 5:
            occurence2 = 0
            downcount2 = 0

        if downcount2y > 11:
            occurence2 = 0
            prereq2 = 0
    	
        # Sleep for SLEEP_TIME seconds
    	time.sleep(SLEEP_TIME)


def reset():
	# Reset gesturedetected value
	gesturedetected = 0
