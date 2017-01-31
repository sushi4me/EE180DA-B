CC=gcc
CFLAGS= -lmraa -lm -Wall
#-lm -lncurses -g -Wall
EXEC=imu
DEP= workingMadgwick.c MadgwickAHRS.c LSM9DS0.c 

.SILENT:
DEFAULT: MadgwickAHRS.h
	$(CC) -o $(EXEC) $(DEP) $(CFLAGS)

clean:
	rm -f *~ .*~ $(EXEC)
