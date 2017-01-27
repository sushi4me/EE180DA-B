#!/usr/bin/python

import sys
from os import listdir
from os.path import isfile, join
from optparse import OptionParser
from posutils import parse_as_dict, write_to_file

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

    input_file = args[0]

    # Collect files from reference db.
    db = "reference_database" if options.dir is None else options.dir
    files = [join(db, f) for f in listdir(db) if isfile(join(db, f))]
    
    # Parse RSSI, place in dictionary with MAC address as key.
    rssiObserved = parse_as_dict(input_file)
    rssiReferences = [parse_as_dict(f) for f in files]

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
    msg = "You are probably at " + files[pos]
    if options.file is not None:
        with open(options.file, "w") as f:
            f.write(msg + "\n")
    else:
        print msg

if __name__ == "__main__":
    main()
