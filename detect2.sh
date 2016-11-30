#!/bin/bash

count=0
while [ $count -lt 15 ]; do
	iwlist wlan0 scan | sed -n -e 's/^.*\(Address: \)//p' >> E1.txt
	let count=count+1
	sleep 15
done
