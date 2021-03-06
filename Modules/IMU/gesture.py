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
    #1 = freeze; 2 = cloak; 3 = grenade; 4 = dice

    gesturedetected = 0
    gestureoccured = 8
    
    downcount1 = 0
    downcount1z = 0
    downcount2 = 0
    downcount2y = 0
    downcount3 = 0
    downcount3z = 0
    
    prereq1 = 0
    prereq2 = 0
    prereq3 = 0
    
    occurence1 = 0
    occurence2 = 0
    occurence3 = 0

    # Position Threshold to start recording gesture
    threshold1_az = 0.85
    threshold1low_az = 0.20
    
    threshold2_ax = -.85  
    threshold2_ay = -.85

    threshold3_ax = -.6
    threshold3_az = -1.3

    # Gesture 4 variables
    start_4 = 0
    counter_4 = 0
    resetCounter_4 = 0
    peak = 0
    # previous = 1 # 1 --> positive
    # current = 0 # 0 --> negative
    # switchcount = 0
    # maxswitchcount = 11 # gesture detected
    # negcount = 0
    # poscount = 0
    # maxdircount = 4 # check if switching fast enough
    # downcount4 = 0


    # Loop and read accel, and gyro
    while(1):
        imu.read_accel()
    	imu.read_gyro()

        # Gesture 1 Detection
    	if imu.az > threshold1_az:
            if imu.ax < 0 and imu.ax > -.4:
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
            #print "GESTURE 1"
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

        # Gesture 2 Detection
        if imu.ax <= threshold2_ax:
            if imu.az < .2 and imu.az > -.2:
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
            #print "GESTURE 2"
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

        # Gesture 3 Detection
        if imu.ax < threshold3_ax:
            if imu.az < 0 and imu.az > -.5:
                occurence3 += prereq3
                downcount3 = 0
        else:
            downcount3 += 1

        if imu.az > threshold3_az:
            downcount3z += 1
        else:
            downcount3z = 0
            prereq3 = 1

        if occurence3 >= gestureoccured:
            return 3
            #print "GESTURE 3"
            gesturedetected = 3
            occurence3 = 0
            downcount3 = 0
            prereq3 = 0

        if downcount3 > 5:
            occurence3 = 0
            downcount3 = 0

        if downcount3z > 14:
            occurence3 = 0
            prereq3 = 0


        # Gesutre 4 Detection
        # Detect the begining of the gesture
        if abs(imu.ax) < 3 and abs(imu.az) < 7:
            start_4 = 1
            resetCounter_4 = 0
        else: # Detect deviasion per tick
            resetCounter_4 += 1
        
        # Detect highs and lows of gesture in y axis
        if imu.ay > 10 and peak == 0:
            counter_4 += start_4
            peak = 1
        elif imu.ay < 2 and peak == 1:
            counter_4 += start_4
            peak = 0

        # Detect the end of the gesture
        if counter_4 == 5:
            return 4 

        # Detect deviation from gesture
        if resetCounter_4 > 9:
            resetCounter_4 = 0
            counter_4 = 0

        # # stwitch from neg -> pos
        # if imu.ay < 0 and previous == 1:
        #     switchcount += 1
        #     current = 0
        #     negcount += 1
        #     poscount = 0 #reset poscount after switch
        #     downcount = 0 #reset downcount after swtich

        #     #print "switch from neg -> pos" 
        #     #print switchcount

        # if imu.ay < 0 and previous == 0:
        #     if negcount < maxdircount:
        #         negcount += 1
        #     else:
        #         downcount4 += 1

        # # switch from pos -> neg
        # if imu.ay > 0 and previous == 0:
        #     switchcount += 1
        #     current = 1
        #     poscount += 1
        #     negcount = 0 #reset negcount after switch
        #     downcount = 0 #reset downcount after switch

        #     #print "switch from pos -> neg"
        #     #print switchcount

        # if imu.ay > 0 and previous == 1:
        #     if poscount < maxdircount:
        #         poscount += 1
        #     else:
        #         downcount4 += 1

        # if switchcount >= maxswitchcount:
        #     return 4
        #     #print "GESTURE 4"
        #     gesturedetected = 4
        #     switchcount = 0
        #     negcount = 0
        #     poscount = 0
    	
        # if downcount4 >= 3:
        #     downcount4 = 0
        #     switchcount = 0
        #     negcount = 0
        #     poscount = 0
        #     #print "Reset"

        # previous = current

        # Sleep for SLEEP_TIME seconds
    	time.sleep(SLEEP_TIME)


def reset():
	# Reset gesturedetected value
	gesturedetected = 0
