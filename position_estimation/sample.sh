#!/bin/bash

COUNTER=0

DIR="/home/root/EE180DA-B/position_estimation/observed_rssi/"

while [ $COUNTER -lt 5 ]; do 
	FILENAME="${DIR}sample${COUNTER}.txt"
	iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*Address: //; s/.*\([0-9]\{2\}\) dBm/\1/' | sed 'N; s/\n/ /' > $FILENAME
	let COUNTER=COUNTER+1

	sleep 0
done
