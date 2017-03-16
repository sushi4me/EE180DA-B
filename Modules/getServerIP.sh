#!/bin/sh
#--------------------------------------
# Script: getServerIP.sh
# Description:
#	Uses gdrive to search through a list of files on 
#	google drive.  It parses the list to obtain the
#	file ID and then uses gdrive download FILEID to
#	download the file
#--------------------------------------

FILE=ipaddress.txt
FILEID=`gdrive list | grep $FILE | awk '{print $1}'`
gdrive download $FILEID > /dev/null