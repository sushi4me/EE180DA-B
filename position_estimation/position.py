#!/usr/bin/python

import sys
import subprocess
from operator import itemgetter
from os import listdir
from os.path import isfile, join
from optparse import OptionParser
from posutils import file_as_dict, write_to_file

def sample_current_location():
    # Run sample collection script.
    exe = "/home/root/EE180DA-B/position_estimation/sample.sh"
    subprocess.call([exe])
    
    # Need to parse the five files generated from script.
    sampledir = "/home/root/EE180DA-B/position_estimation/observed_rssi"
    samplefiles = [join(sampledir, f) for f in listdir(sampledir) if isfile(join(sampledir, f))]

    rssiObserved = [file_as_dict(f) for f in samplefiles]
    
    return rssiObserved

def compute_distance_scores(rssiObserved, rssiReferences):    
    distances = [[] for i in range(len(rssiReferences))] # Euclidean distances.

    # For each file in reference db, compute euclidean distance
    # between observed RSSI and reference RSSI.
    for i, rssiReference in enumerate(rssiReferences):
        for addr, rssi in rssiReference.items():
            if addr in rssiObserved:
                euclDist = pow(rssiObserved[addr] - rssi, 2)
            else: # MAC Address not found, add arbitrarily large value.
                euclDist = 100 # TO-DO: Replace value.

            distances[i].append(euclDist)

    # Compute a score for each reference file.
    scores = [sum(d) for d in distances] 
    
    return scores

def position_estimate(rssiObserved, rssiReferences):
    indicesOfMinScores = [] # Collect indices of minimum scores.
   
    # For each observed sample, make a 
    # guess at the probable position.
    for sample in rssiObserved:
        scores = compute_distance_scores(sample, rssiReferences)
        indicesOfMinScores.append(scores.index(min(scores)))

    # Our guess will be the mode of the set.
    position = max(set(indicesOfMinScores), key=indicesOfMinScores.count)

    return position

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

    # Collect files from reference db.
    db = "/home/root/EE180DA-B/reference_database" if options.dir is None else options.dir
    files = [join(db, f) for f in listdir(db) if isfile(join(db, f))]
    
    # Parse RSSI, place in dictionary with MAC address as key.
    rssiObserved = sample_current_location()
    rssiReferences = [file_as_dict(f) for f in files]

    pos = position_estimate(rssiObserved, rssiReferences)
    
    # TO-DO: Print coordinates of location instead of location filename.
    msg = "You are probably at " + files[pos]
    if options.file is not None:
        with open(options.file, "w") as f:
            f.write(msg + "\n")
    else:
        print msg

if __name__ == "__main__":
    main()
