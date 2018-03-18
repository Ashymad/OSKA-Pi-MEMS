#!/usr/bin/env python3
from mma8451 import accel
import datetime
import time
import signal
import sys

def sigint_handler(signal, frame):
    print('Exiting...')
    MMA8451.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

MMA8451 = accel.Accel()

MMA8451.init_callback()
time.sleep(30)
MMA8451.cleanup()
