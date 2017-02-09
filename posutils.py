import sys

def parse_as_dict(dataobj):
    dict = {}

    for line in dataobj:
        try: 
            key, val = line.split()
            dict[key] = int(val)
        except ValueError:
            continue

    return dict

def write_to_file(filename, dictionary):
    with open(filename, 'w') as f:
        print "Writing to %s..." % filename
        for addr, rssi in dictionary.items():
            f.write(str(addr) + " " + str(rssi) + "\n")

        print "Done writing to %s..." % filename
