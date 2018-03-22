#!/usr/bin/env python3
from mma8451 import mma8451
from threading import Lock
import time
import signal
import sys

def sigint_handler(signal, frame):
    print('Exiting...')
    MMA8451.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

MMA8451 = mma8451.Accel()

MMA8451.init_callback()
print('Finished initialization')
t = 60*60*8
time.sleep(t)
MMA8451.cleanup()
