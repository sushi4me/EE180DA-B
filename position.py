#!/usr/bin/python

import sys
from optparse import OptionParser
from utilities import getPairs

def main():
    version_msg = "%prog 1.0"
    usage_msg = """%prog [OPTION]... FILE
    Output best guess at player's position
    based on RSSI values found in FILE."""

    parser = OptionParser(version=version_msg, usage=usage_msg)
    parser.add_option("-o", "--output", action="store", dest="file",
            help="Write position to FILE")

    options, args = parser.parse_args(sys.argv[1:])

    if len(args) != 1:
        parser.error("Wrong number of operands.")

    inputFile = args[0]
    networksFile = "locations_data/networks.txt"
    locData1 = "locations_data/location1.txt"
    locData2 = "locations_data/location2.txt"

    rawInput = getPairs(inputFile)
    loc1 = getPairs(locData1)
    loc2 = getPairs(locData2)
    with open(networksFile) as f:
        networksList = f.readlines()

    dist1 = []
    dist2 = []
    
    for line in networksList:
        if line in rawInput:
            dist1.append(pow(rawInput[line] - loc1[line], 2))
            dist2.append(pow(rawInput[line] - loc2[line], 2))
        else:
            dist1.append(0)
            dist2.append(0)
    
    score1 = sum(dist1)
    score2 = sum(dist2)

    msg = ""
    if score1 < score2:
        msg = "You are probably at position 1"
    else:
        msg = "You are probably at position 2"

    print msg

if __name__ == "__main__":
    main()
