#!/usr/bin/python

from SF_9DOF import IMU
import time

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

# count and occurences used to detect gesture
gestureoccured = 10
posthreshold = 0.8
negthreshold = -0.8
count = 0
occurence = 0

# Loop and read accel, mag, and gyro
while(1):
    imu.read_accel()
    imu.read_gyro()

    # Print the results
    print("Accel-X: %.8f\tY: %.8f\tZ: %.8f\t|  Gyro-X: %.8f\tY: %.8f\tZ: %.8f\
            " % (imu.ax*10, imu.ay*10, imu.az*10, imu.gx, imu.gy, imu.gz))

    # Sleep for 1/20th of a second
    time.sleep(0.05)
