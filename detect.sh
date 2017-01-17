#!/bin/bash

if [ $# -eq 0 ]
then
	echo -e "Error: Wrong number of operands\nUsage: $0 FILE_PREFIX"
	exit 1
fi

POSITION=$1
TSTAMP=$(date +%s)
FILENAME="${POSITION}_${TSTAMP}.txt"

iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*Address: //; s/.*\([0-9]\{2\}\) dBm/\1/' | sed 'N; s/\n/ /' > $FILENAME
