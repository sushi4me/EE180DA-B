#!/bin/sh
#--------------------------------------
# Script: uploadIPAddress
# Description:
# 	Takes IP Address as a parameter and stores
#	address in a file name ipaddress.txt.  It
#	then uses gdrive to upload file to the drive
#--------------------------------------

FILE=ipaddress.txt
host $1 | sed 's/.*\(wifi-\)/\1/; s/.$//g' > $FILE
FILEID=`gdrive list | grep $FILE | awk '{print $1}'`
gdrive delete $FILEID > /dev/null
gdrive upload $FILE > /dev/null