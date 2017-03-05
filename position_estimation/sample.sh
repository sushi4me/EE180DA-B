#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Please provide a number of samples."
	exit 1
fi

NUMSAMPLES=$1

COUNTER=0

DIR="/home/root/EE180DA-B/position_estimation/observed_rssi/"

while [ $COUNTER -lt $NUMSAMPLES ]; do 
	FILENAME="${DIR}sample${COUNTER}.txt"
	iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*Address: //; s/.*\([0-9]\{2\}\) dBm/\1/' | sed 'N; s/\n/ /' > $FILENAME
	let COUNTER=COUNTER+1

	sleep 0
done
