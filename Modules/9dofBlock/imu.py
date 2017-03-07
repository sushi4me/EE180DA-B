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

# Loop and read accel, mag, and gyro
while(1):
    imu.read_accel()
    imu.read_gyro()
    imu.read_mag()

    # Print the results
    print("AX: %.4f\tY: %.4f\tZ: %.4f\t| GX: %.4f\tY: %.4f\tZ: %.4f\t | MX: %.4f\tY: %.4f\tZ: %.4f\
            " % (imu.ax*10, imu.ay*10, imu.az*10, imu.gx, imu.gy, imu.gz, imu.mx*10, imu.my*10, imu.mz*10))

    # Sleep for 1/20th of a second
    time.sleep(0.05)
