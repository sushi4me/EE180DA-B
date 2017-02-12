import sys

def file_as_dict(filename):
    with open(filename) as f:
        return parse_as_dict(f)
    
def parse_as_dict(data):
    dict = {}

    for line in data:
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
