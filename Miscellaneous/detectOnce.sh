#!/bin/bash

DIR="/home/root/EE180DA-B/demo_calib_data"
# Create "locations_data" directory in working directory to store data files
if [ ! -d "${DIR}" ]; then
	mkdir $DIR
fi

POSITION=$1

# Retrieve time stamp
TSTAMP=$(date +%s)
FILENAME="${DIR}/${POSITION}_${TSTAMP}.txt"

iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*Address: //; s/.*\([0-9]\{2\}\) dBm/\1/' | sed 'N; s/\n/ /' | sort > $FILENAME

cat $FILENAME | tr '\n' ' ' | tr ':' '.' > $DIR/CURRENTSAMPLE.txt
