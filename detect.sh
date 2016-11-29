#!/bin/bash

iwlist wlan0 scan | sed -n -e 's/^.*\(Address\)/\1/p; s/^.*\(Signal\)/\1/p' | awk '!(NR%2){print p "\t" $0} {p=$0}' 
