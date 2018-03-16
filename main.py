#!/usr/bin/env python3
from mma8451 import accel
import datetime
import time
import signal
import sys

def sigint_handler(signal, frame):
    print('Exiting...')
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

MMA8451 = accel.Accel()
MMA8451.init()

def printAcceleration(xaccel, yaccel, zaccel):
    print("   x (m/s2)= %+.3f" % (xaccel))
    print("   y (m/s2)= %+.3f" % (yaccel))
    print("   z (m/s2)= %+.3f" % (zaccel))

if MMA8451.whoAmI() != accel.deviceName:
    print("Error! Device not recognized! (" + str(accel.deviceName) + ")")
    sys.exit()

while True:  # forever loop
    print ("\nCurrent Date-Time: " + str(datetime.datetime.now()))
#    axes = MMA8451.getAxisValue()
#    printAcceleration(axes['x'], axes['y'], axes['z'])
    test_val = MMA8451.getFifoValues()
    print(test_val)
    time.sleep(0.5)
