#!/bin/bash

iwlist wlan0 scan | grep 'Address:\|Signal' | sed 's/.*Address: //; s/.*\([0-9]\{2\}\) dbm/\1/' | sed 'N; s/\n/ /'
