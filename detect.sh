#!/bin/bash

if [ ! -d "locations_data" ]; then
	mkdir locations_data
fi

printf "Choose a spot <0, 17, 25, 35, 41, 47> : "
read POSITION

while [ "$POSITION" -ne 0 ] && [ "$POSITION" -ne 17 ] && [ "$POSITION" -ne 25 ] && [ "$POSITION" -ne 35 ] && [ "$POSITION" -ne 41 ] && [ "$POSITION" -ne 47 ]; do
	printf "Wrong starting location, try again: "
	unset POSITION
	read POSITION
done

while [ 0 ]; do

	TSTAMP=$(date +%s)
	FILENAME="locations_data/${POSITION}_${TSTAMP}.txt"



	printf "SCANNING Position $POSITION... PLEASE WAIT!\n"
	iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*Address: //; s/.*\([0-9]\{2\}\) dBm/\1/' | sed 'N; s/\n/ /' > $FILENAME
	printf "DONE SCANNING!\n"	

[D	printf "Go to next position (n) or rescan current position (r).  Use (q) to quit <n, r, q> : "
	read VAR

	case $VAR in
	"q")
		printf "Quitting!\n"
		exit
		;;
	"f")
		if [ $POSITION == 60 ]
			POSITION=0
		fi
		((POSITION++))
		;;
	"r")
		printf "Repeating...\n"
		;;
	*)
		printf "Invalid option, repeating...\n"		
		;;
	esac

done
