#!/usr/bin/env python3
from mma8451 import accel
import acoustics.signal
import datetime
import time
import signal
from scipy.constants import g
from scipy.io import wavfile
import numpy as np
import sys

def sigint_handler(signal, frame):
    print('Exiting...')
    MMA8451.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

MMA8451 = accel.Accel()

MMA8451.init_callback()
t = 10
time.sleep(t)
MMA8451.cleanup()

data = MMA8451.getQueue()

divider = 4096/g
prec = 14
fs = 800

def reg2float(msb, lsb):
    num = ((int(msb) << 8) | int(lsb)) >> 2
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

def reg2uint(msb, lsb):
    num = ((int(msb) << 8) | int(lsb)) >> 2
    maxn = 2**(prec-1)-1
    signed_maxn = 2**prec
    num -= signed_maxn if num > maxn else 0
    return np.int16(num)

def prepare_wavd(bitvec):
    data = np.zeros([len(bitvec)//6,3], dtype=np.int16)
    for i in range(0, len(bitvec), 6):
        data[i//6,0] = reg2uint(bitvec[i],bitvec[i+1])
        data[i//6,1] = reg2uint(bitvec[i+2],bitvec[i+3])
        data[i//6,2] = reg2uint(bitvec[i+4],bitvec[i+5])
    return data

sigdta = prepare_wavd(data.get())

while not data.empty():
    sigdta = np.append(sigdta,prepare_wavd(data.get()), axis=0)

wavfile.write("x_data.wav",fs,sigdta[:,0])
wavfile.write("y_data.wav",fs,sigdta[:,1])
wavfile.write("z_data.wav",fs,sigdta[:,2])
#
#np.savetxt("out.txt",sigdta)
#
#
#frq = acoustics.signal.OctaveBand(fstart=0.5, fstop=100, fraction=3)
#
#filt = acoustics.signal.Filterbank(frq, sample_frequency=fs)
#
#y_f = filt.filtfilt(sigdta[:,0])
#
#filt_data = list(y_f)
#
#result = np.zeros(len(filt_data))
#for it in range(len(filt_data)):
#    #result[it] = np.sqrt(np.mean(np.square(filt_data[it])))
#    result[it] = np.max(filt_data[it])
#    print(result[it])
