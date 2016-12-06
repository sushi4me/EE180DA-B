#!/bin/bash

LOCATION=$1 # Text file to save output.	


iwlist wlan0 scan | grep 'Address\|Signal' | \
	sed 's/^.*Address: //; s/^.*\([0-9]\{2\}\) dBm/\1/' | \
	sed 'N; s/\n/ /' > $LOCATION
