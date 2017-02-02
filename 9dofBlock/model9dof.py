#!/usr/bin/python
from __future__ import print_function
from SF_9DOF import IMU
import time
import sys
import os

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

cols = 60 
rows = 30
grid = [[' ' for x in range(cols)] for y in range(rows)]

def clearGrid():
    for i in range(rows):
        for j in range(cols):
            if i != int(rows/2):
                if j != int(cols/2):
                    grid[i][j] = ' ' 
                else:
                    grid[i][j] = '|'
            else:
                grid[i][j] = '_'

def printImage(x, y):
    clearGrid()
    grid[int(rows/2) - x][int(cols/2) + y] = '*'
    grid[-(int(rows/2) - x)][-(int(cols/2) + y)] = '*'
    for i in range(rows):
        print(*grid[i], sep='')

# Loop and read accel, mag, and gyro
while(1):
    imu.read_accel()
    imu.read_gyro()

    # Print the results
    #print("Accel-X: %.8f\tY: %.8f\tZ: %.8f\t|  Gyro-X: %.8f\tY: %.8f\tZ: %.8f\
    #        " % (imu.ax*10, imu.ay*10, imu.az*10, imu.gx, imu.gy, imu.gz))
    
    os.system('clear')
    c = min(-int(cols/2) + 1, int(imu.ay * 10))
    c = max(int(cols/2) - 1, int(imu.ay * 10))
    r = min(-int(rows/2) + 1, int(imu.ax * 10))
    r = max(int(rows/2) - 1, int(imu.ax * 10))
    printImage(int(imu.ax * 10), int(imu.ay * 10))
    print("imu.ax: %d\timu.ay: %d" % (int(imu.ax * 10), int(imu.ay * 10)))

