#!/usr/bin/env python3
from mma8451 import mma8451
import time
import signal
import sys

def sigint_handler(signal, frame):
    print('Exiting...')
    MMA8451.cleanup()
    sys.exit(0)


MMA8451 = mma8451.Accel()

signal.signal(signal.SIGINT, signal.SIG_IGN)
MMA8451.init_callback()
signal.signal(signal.SIGINT, sigint_handler)
print('Finished initialization')
signal.pause()
