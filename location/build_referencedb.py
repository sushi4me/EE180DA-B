#!/usr/bin/python

import sys
from os import listdir
from operator import itemgetter
from os.path import isdir, isfile, join
from optparse import OptionParser
from posutils import parse_as_dict, file_as_dict, write_to_file

def calculate_average_rssi(files):
    dicts = []

    # Let's parse each file...
    for f in files:
        print "Parsing %s..." % f
        dicts.append(file_as_dict(f))
        print "Done parsing %s..." % f

    # Create a new dictionary to contain all "found" MAC addresses.
    all_addrs = set().union(*dicts)
    running_sum = {addr: 0 for addr in all_addrs}

    # Keep track of how many times we "see" a MAC address.
    num_occurrences = {addr: 0 for addr in all_addrs}

    # Compute running sum at each MAC address.
    for addr in all_addrs:
        for d in dicts:
            if addr in d:
                running_sum[addr] += d[addr]
                num_occurrences[addr] += 1
    
    # Compute average rssi value for each MAC address.
    average_rssi = {}
    for addr in all_addrs:
        average_rssi[addr] = running_sum[addr] / num_occurrences[addr]

    #trunc_rssi = dict(sorted(average_rssi.iteritems(), key=itemgetter(1), reverse=True)[:25])

    return average_rssi

def main():
    version_msg = "%prog 1.0"
    usage_msg   = """%prog [OPTION]... DIRECTORY
    Compile RSSI samples (found in DIRECTORY) 
    with the same file prefix into a 
    single file."""

    parser = OptionParser(version=version_msg, usage=usage_msg)
    parser.add_option("-n", "--numpositions", action="store", dest="npositions", default=61)

    options, args = parser.parse_args(sys.argv[1:])

    if len(args) != 1:
        parser.error("Wrong number of operands")

    # Generate list of all files in directory "d".
    d = args[0]

    if(not isdir(d)):
        print "The path:", d, "is not an exisiting directory. Exiting..."
        sys.exit(1)

    referencedb = "/home/root/EE180DA-B/reference_database"

    files = [f for f in listdir(d) if isfile(join(d, f))]

    npositions = options.npositions
    files_by_position = [[] for i in range(npositions)]
    
    # Collect all files with the same file prefix.
    for position in range(npositions):
        for f in files:
            if f.startswith("%s_" % position):
                files_by_position[position].append(join(d, f))

    # Calculate rssi average and write resuls to file.
    for position in range(npositions):
        avg_rssi = calculate_average_rssi(files_by_position[position])
        
        filename = join(referencedb, "position%s_reference" % position)
        write_to_file(filename, avg_rssi)

if __name__ == "__main__":
    main()
