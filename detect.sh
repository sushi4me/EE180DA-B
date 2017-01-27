#!/bin/bash

<<<<<<< HEAD
# UCLA EE 180D data collection script.
# The script expects one argument:
# 	./detect.sh position(num)
#
# This argument must not contain any
# spaces.
#
# example:
#	./detect.sh position5

if [ $# -ne 1 ]
then
	echo -e "Error: Wrong number of operands\nUsage: $0 FILE_PREFIX"
	exit 1
=======
printf "=============================================== 
UCLA EIV 4th Floor WLAN SCAN ACCESS POINTS SSID
===============================================
(0)  Hallway 1              41----47
(17) Hallway 2               |    |
(25) Hallway 3      25------35    |
(35) Hallway 4       |            |
(41) Hallway 5       |            |
(47) Hallway 6      17------------0 (EIV 44110)
================================================
Choose a starting position < 0, 17, 25, 35, 41, 47 > : "
read POSITION

while [ "$POSITION" -ne 0 ] && [ "$POSITION" -ne 17 ] && [ "$POSITION" -ne 25 ] && [ "$POSITION" -ne 35 ] && [ "$POSITION" -ne 41 ] && [ "$POSITION" -ne 47 ]; do
	printf "Wrong starting location, try again: "
	unset POSITION
	read POSITION
done

# Create "locations_data" directory in working directory to store data files
if [ ! -d "locations_data" ]; then
	mkdir locations_data
>>>>>>> bfa7d1adbbbb5bced7b456a144c10fd439d2be45
fi

while [ 0 ]; do

	TSTAMP=$(date +%s)
	FILENAME="locations_data/${POSITION}_${TSTAMP}.txt"



	printf "SCANNING Position $POSITION... PLEASE WAIT!\n"
	iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*Address: //; s/.*\([0-9]\{2\}\) dBm/\1/' | sed 'N; s/\n/ /' | sort > $FILENAME
	printf "DONE SCANNING!\n\n"	

	if [ $POSITION == 60 ]
	then
		printf "REACHED LAST POSITION!\nSELECTING (n) WILL SCAN POSITION 0\n"	
	fi

	printf "Go to next position (n) or rescan current position (r).  Use (q) to quit <n, r, q> : "
	read VAR

	case $VAR in
	"q")
		printf "Quitting!\n"
		exit
		;;
	"n")
		if [ $POSITION == 60 ]
		then
			POSITION=0
		else
			((POSITION++))
		fi
		;;
	"r")
		printf "Repeating...\n"
		;;
	*)
		printf "Invalid option, repeating...\n"		
		;;
	esac

done
