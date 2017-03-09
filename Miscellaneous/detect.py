import sys
import subprocess
from os       import listdir
from os.path  import isfile, join, basename

def sample_location_number(location):
    # Run sample collection script.
    exe = "/home/root/EE180DA-B/Miscellaneous/detectOnce.sh"
    subprocess.call([exe, str(location)])

    locationdata = ""
    with open("demo_calib_data/CURRENTSAMPLE.txt", 'r') as fin:
    	locationdata = fin.read()
    fin.close()

    return locationdata