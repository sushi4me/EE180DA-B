#!/bin/bash

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
Choose a starting position [0 - 60]: "
read POSITION

while [ 0 ]; do
	if [[ "$POSITION" =~ ^[0-9]+$ ]] && [ "$POSITION" -ge 0 -a "$POSITION" -le 60 ]; then
		break
	fi
	printf "Invalid entry, please try again: "
	unset POSITION
	read POSITION
done

# Create "locations_data" directory in working directory to store data files
if [ ! -d "locations_data" ]; then
	mkdir locations_data
fi

while [ 0 ]; do

	printf "You are at position $POSITION.\n"
	printf "Scan current position (s), go to previous position (p), go to next position (n), quit (q) <s, p, n, q> : "
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
		continue
		;;
	"p")
		if [ $POSITION == 0 ]
		then
			POSITION=60
		else
			((POSITION--))
		fi
		continue
		;;
	"s")
		;;
	*)
		printf "Invalid option, try again...\n"	
		continue
		;;
	esac


	# Retrieve time stamp
	TSTAMP=$(date +%s)
	FILENAME="locations_data/${POSITION}_${TSTAMP}.txt"

	printf "SCANNING Position $POSITION... PLEASE WAIT!\n"
	iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*Address: //; s/.*\([0-9]\{2\}\) dBm/\1/' | sed 'N; s/\n/ /' | sort > $FILENAME
	printf "DONE SCANNING!\n\n"	

	# If reached last position allow user to start from position 0
	if [ $POSITION == 60 ]
	then
		printf "REACHED LAST POSITION!\nSELECTING (n) WILL SCAN POSITION 0\n"	
	fi


done
