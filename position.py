#!/usr/bin/python

import sys
from os import listdir
from os.path import isfile, join
from optparse import OptionParser

def getPairs(filename):
    dict = {}

    with open(filename) as f:
        for line in f:
            key, val = line.split()
            dict[key + "\n"] = int(val)

    return dict

def main():
    version_msg = "%prog 1.0"
    usage_msg = """%prog [OPTION]... FILE
    Output best guess at player's position
    based on RSSI values found in FILE."""

    parser = OptionParser(version=version_msg, usage=usage_msg)
    parser.add_option("-o", "--output", action="store", dest="file",
            help="Write position to FILE")
    parser.add_option("-d", "--directory", action="store", dest="dir",
            help="Use DIR as reference database.")

    options, args = parser.parse_args(sys.argv[1:])

    if len(args) != 1:
        parser.error("Wrong number of operands.")

    inputFile = args[0]

    # Collect files from reference db.
    if options.dir is not None:
        locationsDir = options.dir
    else:
        locationsDir = "locations_data"
    locationFiles = [join(locationsDir, f) for f in listdir(locationsDir) if isfile(join(locationsDir, f))]
    
    # Parse RSSI, place in dictionary with MAC address as key.
    rssiObserved = getPairs(inputFile)
    rssiReferences = [getPairs(file) for file in locationFiles]

    distances = [[] for i in range(len(rssiReferences))] # Euclidean distances.

    # For each file in reference db, compute euclidean distance
    # between observed RSSI and reference RSSI.
    for i, rssiReference in enumerate(rssiReferences):
        for addr, rssi in rssiReference.items():
            if addr in rssiObserved:
                dist = pow(rssiObserved[addr] - rssi, 2)
            else: # MAC Address not found, add arbitrarily large value.
                dist = 100 # TO-DO: Replace value.

            distances[i].append(dist)

    scores = [sum(d) for d in distances]

    pos = scores.index(min(scores))

    # TO-DO: Print coordinates of location instead of location filename.
    msg = "You are probably at " + locationFiles[pos]
    if options.file is not None:
        with open(options.file, "w") as f:
            f.write(msg + "\n")
    else:
        print msg

if __name__ == "__main__":
    main()
