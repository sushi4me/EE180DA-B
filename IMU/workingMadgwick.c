#include <stdio.h>
#include <stdlib.h>
#include <mraa/i2c.h>
#include "LSM9DS0.h"
#include "MadgwickAHRS.h"
#include <math.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#define pi 3.14159265359
#define degToRad pi/180.f //would be faster as a constant
#define microSeconds  100000 //0.1s or 10Hz
#define testTimeMS 4000000 // 5.0s each gesture will be recorded for testTime seconds
#define numDataPoints testTimeMS / microSeconds
char buffer[256];


void printHeader(void);

struct Angle
{
	double x;
	double y;
	double z;
}Omega,current_data,prev_data;


const double time_interval = (double)microSeconds/1000000;

int main() {
	data_t accel_data, gyro_data;
	data_t gyro_offset;
	float a_res, g_res;
	mraa_i2c_context accel, gyro;
	accel_scale_t a_scale = A_SCALE_2G;	//accel scale set to 2g (changed from 4)
	gyro_scale_t g_scale = G_SCALE_245DPS;	//gyro scale set to 245 dps (changed from 2000)

	//generate timestamp
	time_t rawtime;
	struct tm *timeinfo;
	const int NAME_SIZE = 25;
	char filename[NAME_SIZE], timestamp[NAME_SIZE];

	time(&rawtime);
	timeinfo = localtime(&rawtime);
	strftime(timestamp, NAME_SIZE, "%Y%m%d_%X", timeinfo);

	//initialize Omega to zero and prev_data
	Omega.x = 0;
	Omega.y = 0;
	Omega.z = 0;
	prev_data.x = 0;
	prev_data.y = 0;
	prev_data.z = 0;

	//initialize sensors, set scale, and calculate resolution.
	accel = accel_init();
	set_accel_scale(accel, a_scale);	
	a_res = calc_accel_res(a_scale);
	
	gyro = gyro_init();
	set_gyro_scale(gyro, g_scale);
	g_res = calc_gyro_res(g_scale);
	

	//print header
	printHeader();

	//find offset for the gyro sensor
	gyro_offset = calc_gyro_offset(gyro, g_res);
	
	//print offsets
	printf("x_offset: %f y_offset: %f z_offset: %f\n", gyro_offset.x, gyro_offset.y, gyro_offset.z);
	
	
	//Prompt user for gesture and print sensor data
	while(1) {
	  printf("\nEnter a gesture to record (1-5).  Press (q) to quit: ");
	  int i;
	  if (fgets(buffer, sizeof(buffer), stdin)) {
	    if (1 == sscanf(buffer, "%d", &i)) {
	      /* i can be safely used */
	      if (strlen(buffer) != 2) {
		printf("ERROR: Invalid gesture number!\n");
		continue;
	      }

	      switch(i){
	      case 1:
	      case 2:
	      case 3:
	      case 4:
	      case 5:
		{

		//Create new text file
		
		//snprintf(filename, NAME_SIZE, "%i_%s.txt", i, timestamp);
		sprintf(filename, "%i_%s.txt", i, timestamp);
		
		FILE *f = fopen(filename, "w");

		if (f == NULL)
		{
			printf("Error opening file!\n");
			exit(1);
		}

		//fprintf(f, "\n\t\tGyroscope\t\t\t||");
		//fprintf(f, "\t\t\t\tAccelerometer\t\t\t\t\t||\n");

		  for (i=0; i < numDataPoints; i++){
		accel_data = read_accel(accel, a_res);
		gyro_data = read_gyro(gyro, g_res);

		//calculates the angular rate of change in degrees per second
		current_data.x = gyro_data.x-gyro_offset.x;
		current_data.y = gyro_data.y-gyro_offset.y;
		current_data.z = gyro_data.z-gyro_offset.z;
		
		//convert angular rate of change to radians per second
		current_data.x *= degToRad;
		current_data.y *= degToRad;
		current_data.z *= degToRad;

		//perform the Madgwick Algorithm
		//with the Madgwick algorithm, in MadgwickAHRS.c
		//you will need to change the variable sampleFreq to the frequency that you are reading data in at
		//this is currently set to 10Hz
		MadgwickAHRSupdateIMU(current_data.x,current_data.y,current_data.z,accel_data.x,accel_data.y,accel_data.z);

		//convert the quaternion representation to Euler Angles in radians
		Omega.x = atan2(2*(q2*q3-q0*q1),2*q0*q0+2*q3*q3-1);
		Omega.y =-1*asin((double)(2*(q0*q2+q1*q3)));
		Omega.z = atan2(2*(q1*q2-q0*q3),2*q0*q0+2*q1*q1-1); 

		//convert Angles from  radians to degrees
		Omega.x *= 180 / pi;
		Omega.y *= 180 / pi;
		Omega.z *= 180 / pi;

  		fprintf(f, "X: %f\t Y: %f\t Z: %f\t||", gyro_data.x - gyro_offset.x, gyro_data.y - gyro_offset.y, gyro_data.z - gyro_offset.z);
		fprintf(f, "\tOmegaX: %f\t OmegaY: %f\t OmegaZ: %f\t||\n", Omega.x,Omega.y,Omega.z);

		usleep(microSeconds);
		fclose(f);

		  }
		break;
		}
	      default:
		{
		  printf("ERROR: Not a valid gesture!\n");
		  break;
		}
	      }
	    }
	    if(buffer[0] == 'q')
	      exit(0);
	  }
	}
	return 0;	
}

void printHeader(void) {
  printf("\
==============================================\n\
GESTURE DATA COLLECTION PROGRAM\n\
==============================================\n\
+----------+--------------------+\n\
| GESTURE  |        NAME        |\n\
+----------+--------------------+\n\
|    1     | Raise Hand         |\n\
+----------+--------------------+\n\
|    2     | Rotate Hand        |\n\
+----------+--------------------+\n\
|    3     | ENTER GESTURE      |\n\
+----------+--------------------+\n\
|    4     | ENTER GESTURE      |\n\
+----------+--------------------+\n\
|    5     | ENTER GESTURE      |\n\
+----------+--------------------+\n");
}

