#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Enter a position"
	exit 1
fi

POSITION=$1

COUNT=0

while [ $COUNT -lt 10 ]; do

TIMESTAMP=$(date +%s)
DIR="/home/root/EE180DA-B/locations_data"
FILENAME="${DIR}/${POSITION}_${TIMESTAMP}.txt"

iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*\([0-9]\{2\}\) dBm/\1/' | sed 'N; s/\n/ /' > $FILENAME

let COUNT=$COUNT+1

sleep 0

done
