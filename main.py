#!/usr/bin/env python3
from mma8451 import accel
import acoustics.signal
import datetime
import time
import signal
import sys
import numpy as np

def sigint_handler(signal, frame):
    print('Exiting...')
    MMA8451.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

#MMA8451 = accel.Accel()

#MMA8451.init_callback()


f1 = 50
f2 = 120
f3 = 180

fs = 1000

t = np.arange(0,2,0.001)
y = np.sin(2*np.pi*t*f1) + np.sin(2*np.pi*t*f2) + np.sin(2*np.pi*t*f3)

low_f = [11.2, 14.1, 17.8, 22.4, 28.2, 35.5, 44.7, 56.2, 70.8, 89.1, 112, 141, 178]
cen_f = [12.5, 16,   20,   25,   31.5, 40,   50,   63,   80,   100,  125, 160, 200]
upp_f = [14.1, 17.8, 22.4, 28.2, 35.5, 44.7, 56.2, 70.8, 89.1, 112,  141, 178, 224]

frq = acoustics.signal.Frequencies(low_f,cen_f,upp_f)
frq.sample_frequency = fs
filter = acoustics.signal.Filterbank(frq)
y_f = filter.power(y)

print(y_f)


#time.sleep(5)
#MMA8451.cleanup()
