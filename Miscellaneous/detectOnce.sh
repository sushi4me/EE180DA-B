#!/bin/bash

# Create "locations_data" directory in working directory to store data files
if [ ! -d "demo_calib_data" ]; then
	mkdir demo_calib_data
fi

POSITION=$1

# Retrieve time stamp
TSTAMP=$(date +%s)
DIR="demo_calib_data"
FILENAME="${DIR}/${POSITION}_${TSTAMP}.txt"

iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*Address: //; s/.*\([0-9]\{2\}\) dBm/\1/' | sed 'N; s/\n/ /' | sort > $FILENAME

cat $FILENAME | tr '\n' ' ' | tr ':' '.' > $DIR/CURRENTSAMPLE.txt
