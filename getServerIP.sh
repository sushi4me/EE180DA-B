#!/bin/sh

FILEID=`gdrive list | grep ipaddress.txt | awk '{print $1}'`
gdrive download $FILEID


