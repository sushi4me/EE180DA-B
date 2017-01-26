#!/bin/bash

# Analysis File Name
TSTAMP=$(date +%s)
AF=ANALYSIS.TXT.$TSTAMP
touch $AF

# Position Index
POSITION=0

printf "===========================================
GENERATING ANALYSIS REPORT.  \nPLEASE WAIT"

while [ "$POSITION" -ne 61 ]; do
    # Label each position data block
    printf "POSITION $POSITION DATA\n" >> $AF

    # List of File Names to Process
    ls | grep ^$POSITION\_ > TEMP.TXT
    sed -i -e 's/^/\ \<\(sort\ /;s/$/\)/' TEMP.TXT
    sed -n 3,100p TEMP.TXT > TEMP2.TXT
    sed -i -e 's/^/\ \|\ \join\ \-\ /' TEMP2.TXT
    export FILES="join"
    export FILES=$FILES`head -n 2 TEMP.TXT`
    export FILES=$FILES`cat TEMP2.TXT`
    eval $FILES >> $AF
    ((POSITION++))
    printf "."
done
rm TEMP.TXT
rm TEMP2.TXT
printf "\nANALYSIS REPORT COMPLETE!\n"
printf "Analysis Report is located at the following path:\n"
printf "$(pwd)/$AF\n"
printf "===========================================\n"
