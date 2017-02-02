/*
Code modified from the following resource:
Author: http://HelloACM.com
http://CodingForSpeed.com
*/
#include <stdio.h>
#include <unistd.h> // for usleep function
 
const char iceball[] =
"            		\n\
          ___ 		\n\
         (   )		\n\
          ( )  		\n\
          | |	  	\n\
          | |	  	\n\
        `-\"\"\"-`	\n\
	 // \\\\  	\n\
	 // \\\\    	\n\
	  / \\     	\n\
	   |     	\n\
";
 
int main(void)
{
  int i;
  for (i = 0; i < 50; i ++) printf("\n"); // jump to bottom of console
  printf("%s", iceball);
  int j = 250000;
  for (i = 0; i < 50; i ++) {
    usleep(j); // move faster and faster,
    j = (int)(j*0.9); // so sleep less each time
    printf("\n"); // move rocket a line upward
  }
  return 0;
}
