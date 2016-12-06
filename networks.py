#!/usr/bin/python

# Takes two files containing MAC addresses and
# signal values formatted in columns. Script
# will output addresses contained in both files.

import sys
from optparse import OptionParser

def getPairs(filename):
    MAC_ADDR = {}
    with open(filename) as f:
        for line in f:
            key, val = line.split()
            MAC_ADDR[key] = val
    
    return MAC_ADDR

def compareAddresses(dict1, dict2):
    return {x:dict1[x] for x in dict1 if x in dict2}
 
def main():
    version_msg = "%prog 1.0"
    usage_msg = """%prog [OPTION]... MACADDR_FILE1 MACADDR_FILE2
    Output MAC addresses common to both files."""

    parser = OptionParser(version=version_msg, usage=usage_msg)
    parser.add_option("-o", "--output", action="store", dest="file",
            help="Write output to FILE")

    options, args = parser.parse_args(sys.argv[1:])

    if len(args) != 2:
        parser.error("Wrong number of operands.")

    deviceFile1 = args[0]
    deviceFile2 = args[1]
    
    MAC_ADDR1 = getPairs(deviceFile1)
    MAC_ADDR2 = getPairs(deviceFile2)

    commonAddr = compareAddresses(MAC_ADDR1, MAC_ADDR2)

    if options.file is not None:
        with open(options.file, "a") as f:
            for key,val in commonAddr.items():
                f.write(key + " " + val + "\n")
    else:
        for key,val in commonAddr.items():
            print key, val

if __name__=="__main__":
    main()
