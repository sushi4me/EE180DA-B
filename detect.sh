#!/bin/bash

count=0
while [ $count -lt 1 ]; do
	iwlist wlan0 scan | grep 'Address\|Signal' | sed 's/^.*Address: //; s/^.*level=-\([0-9]\{2\}\) dBm/\1/' > E1.txt
	let count=count+1
	#sleep 15
done
