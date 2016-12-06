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

def compareAddresses(myaddrs):
    mysets = (set(x.items()) for x in myaddrs)
    return reduce(lambda a,b: a.intersection(b), mysets)
 
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

    addresses = []
    for file in args:
        addresses.append(getPairs(file))

    commonAddr = compareAddresses(addresses)
    
    if options.file is not None:
        with open(options.file, "a") as f:
            for key,val in commonAddr:
                f.write(key + " " + val + "\n")
    else:
        for key,val in commonAddr:
            print key, val

if __name__=="__main__":
    main()
