#!/usr/bin/python

from SF_9DOF import IMU
import time
import os
from time import gmtime, strftime
import sys

# Globals 
WAITSECS = 0.02;
NUMDATAPOINTS = 100;
DIRECTORY = "gesture_data"

# Create Directory for file if does not exist
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

# Print Program Header
print("\
=======================================\n\
STARTING GESTURE RECORDING TOOL\n\
=======================================")

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


def recordData(x):
    tstamp = strftime("_%Y-%m-%d%H:%M:%S", gmtime())
    file = DIRECTORY + '/' + str(x) + tstamp + ".txt"
    fd = open(file, 'w')

    # Loop and read accel, mag, and gyro
    for i in range(NUMDATAPOINTS):
        imu.read_accel()
        imu.read_gyro()

        # Print the results
        fd.write("Accel-X: %.8f\tY: %.8f\tZ: %.8f\t|  Gyro-X: %.8f\tY: %.8f\tZ: %.8f\n\
        " % (imu.ax*10, imu.ay*10, imu.az*10, imu.gx, imu.gy, imu.gz))

        # Sleep for 1/10th of a second
        time.sleep(WAITSECS)
    fd.close()

while(1):
    try:
        input = int(raw_input('Choose a gesture (1-9): '))
    except ValueError: # just catch the exceptions you know!
        print("That\'s not a number!")
    else:
        if 1 <= input <= 9: # this is faster
            for i in range(3):
                os.system('clear')
                sys.stdout.write("Will begin recording in: ")
                sys.stdout.write(str(3 - i))
                sys.stdout.flush()
                time.sleep(1)
            print("")
            print("RECORDING DATA...")
            recordData(input)
            print("COMPLETE!")
        else:
            print 'Not a valid entry. Try again'


