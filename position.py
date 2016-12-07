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

    rawInput = getPairs(inputFile)

if __name__ == "__main__":
    main()
