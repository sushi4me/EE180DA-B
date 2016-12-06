#!/bin/bash

iwlist wlan0 scan | grep 'Address\|Signal' | sed 's/^.*Address: //; s/^.*level=-\([0-9]\{2\}\) dBm/\1/' > E1.txt
