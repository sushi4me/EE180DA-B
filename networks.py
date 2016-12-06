#!/usr/bin/env python

import sys
from optparse import OptionParser

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

    with open(deviceFile1) as f:
        MAC_ADDR1 = f.readlines()

    with open(deviceFile2) as f:
        MAC_ADDR2 = f.readlines()

    commonAddr = [line for line in MAC_ADDR1 if line in MAC_ADDR2]

    if options.file is not None:
        with open(options.file) as f:
            f.writelines(commonAddr)
    else:
        for line in commonAddr:
            sys.stdout.write(line)

if __name__=="__main__":
    main()
