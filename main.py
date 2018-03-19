#!/usr/bin/env python3
from mma8451 import accel
import datetime
import time
import signal
from scipy.constants import g
import numpy as np
import sys

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
