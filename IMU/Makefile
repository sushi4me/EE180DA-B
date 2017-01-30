
CC=gcc
CFLAGS= -lmraa -lm -lncurses

.SILENT:
	
DEFAULT: LSM9DS0.h
	$(CC) -o imu workingMadgwick.c MadgwickAHRS.c LSM9DS0.c $(CFLAGS)
