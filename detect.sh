#!/bin/bash

printf "Choose a spot <0, 17, 25, 35, 41, 47> : "
read POSITION

while [ "$POSITION" -ne 0 ] && [ "$POSITION" -ne 17 ] && [ "$POSITION" -ne 25 ] && [ "$POSITION" -ne 35 ] && [ "$POSITION" -ne 41 ] && [ "$POSITION" -ne 47 ]; do
	printf "Wrong starting location, try again: "
	unset POSITION
	read POSITION
done

while [ 0 ]; do

	TSTAMP=$(date +%s)
	FILENAME="${POSITION}_${TSTAMP}.txt"

	printf "SCANNING Position $POSITION... PLEASE WAIT!\n"
	iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*Address: //; s/.*\([0-9]\{2\}\) dBm/\1/' | sed 'N; s/\n/ /' > $FILENAME
	printf "DONE SCANNING!\n"	

	printf "Go to next position (f) or rescan current position (r).  Use (q) to quit. <q, f, r> : "
	read VAR

	case $VAR in
	"q")
		printf "Quitting!\n"
		exit
		;;
	"f")
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
