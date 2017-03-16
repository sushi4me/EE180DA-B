#!/bin/sh
#--------------------------------------
# Script: uploadIPAddress
# Description:
# 	Takes IP Address as a parameter and stores
#	address in a file name ipaddress.txt.  It
#	then uses gdrive to upload file to the drive
#--------------------------------------

FILE=ipaddress.txt
echo $1 > $FILE
gdrive upload $FILE
