#!/usr/bin/python

# Takes any number of files containing MAC addresses and
# signal values formatted in columns.
# Output will be the intersection of the addresses.

import sys
from optparse import OptionParser
from utilities import getPairs
    
def intersect(macAddrs):
    return list(set(macAddrs[0]).intersection(*macAddrs[1:]))

def extractAddress(dictList):
    macAddr = []
    for dict in dictList:
        macAddr.append(dict.keys())

    return macAddr

def main():
    version_msg = "%prog 1.0"
    usage_msg = """%prog [OPTION]... MACADDR_FILE1 MACADDR_FILE2
    Output MAC addresses common to both files."""

    parser = OptionParser(version=version_msg, usage=usage_msg)
    parser.add_option("-o", "--output", action="store", dest="file",
            help="Write output to FILE")

    options, args = parser.parse_args(sys.argv[1:])

    if len(args) < 2:
        parser.error("Wrong number of operands.")

    # Read MAC addresses and signal strength from files.
    dictList = []
    for file in args:
        dictList.append(getPairs(file))

    # Extract MAC addresss values from each dictionary
    # and find intersection.
    macAddr = extractAddress(dictList) 
    commonAddr = intersect(macAddr)

    # Write output to specified file or stdout.
    if options.file is not None:
        with open(options.file, "w") as f:
            f.writelines(commonAddr)
    else:
        for addr in commonAddr:
            sys.stdout.write(addr)

if __name__=="__main__":
    main()
