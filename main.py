#!/usr/bin/env python3
from mma8451 import accel
import acoustics.signal
import datetime
import time
import signal
from scipy.constants import g
import numpy as np
import sys
import numpy as np

def sigint_handler(signal, frame):
    print('Exiting...')
    MMA8451.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

MMA8451 = accel.Accel()

MMA8451.init_callback()
time.sleep(5)
MMA8451.cleanup()

data = MMA8451.getQueue()

divider = 4096/g
prec = 14

def reg2float(msb, lsb):
    num = ((msb << 8) | lsb) >> 2
    maxn = 2**(prec-1)-1
    signed_maxn = 2**prec
    num -= signed_maxn if num > maxn else 0
    return float(num)/divider

def prepare_data(bitvec):
    data = np.zeros([len(bitvec)//6,3])
    for i in range(0, len(bitvec), 6):
        data[i//6,0] = reg2float(bitvec[i],bitvec[i+1])
        data[i//6,1] = reg2float(bitvec[i+2],bitvec[i+3])
        data[i//6,2] = reg2float(bitvec[i+4],bitvec[i+5])
    return data

sigdta = prepare_data(data.get())
while not data.empty():
    sigdta = np.append(sigdta,prepare_data(data.get()), axis=0)

np.savetxt("out.txt",sigdta)

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
