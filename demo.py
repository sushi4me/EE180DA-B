#!/usr/bin/python
import time
time.sleep(5)
from multiprocessing import Process
import subprocess, signal
import mraa
import os

def runDemo():
    os.system("/home/root/EE180DA-B/main.py")

def killProcess():
    p = subprocess.Popen(['ps'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if 'main.py' in line:
            pid = int(line.split(None, 1)[0])
            print "killing process" + str(pid)
            os.kill(pid, signal.SIGKILL)

BUTTON_A = mraa.Gpio(47)
BUTTON_B = mraa.Gpio(32)
BUTTON_A.dir(mraa.DIR_IN)
BUTTON_B.dir(mraa.DIR_IN)

def waitForButtonPress():
    while(BUTTON_A.read() != 0 and BUTTON_B.read() != 0):
        time.sleep(3)

def checkButtonHold():
    i = 0
    while(BUTTON_A.read() == 0 and BUTTON_B.read() == 0):
        time.sleep(1)
        i += 1
        if i > 3:
            return True
    return False
p = []
print "Creating New demo.py Process"
temp = Process(target=runDemo)
print "starting new process"
temp.start()
print "continue checking for reset"
p.append(temp)

while True:
    waitForButtonPress()
    if checkButtonHold() == True:
        killProcess()
        print "Creating New demo.py Process"
        temp = Process(target=runDemo)
        print "starting new process"
        temp.start()
        print "continue checking for reset"
        p.append(temp)

for i in p:
    print "joined new process"
    i.join()
