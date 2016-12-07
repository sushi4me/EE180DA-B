#!/usr/bin/python

def getPairs(filename):
    dict = {}
    
    with open(filename) as f:
        for line in f:
            key, val = line.split()
            dict[key + "\n"] = val

    return dict
