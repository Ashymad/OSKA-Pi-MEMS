import h5py as h5
import acoustics
import numpy as np
import matplotlib.pyplot as plt
from mma8451.files import dataread

with h5.File('data.h5','r') as f:
    data = dataread(f, "2018", '03', '23', '07')

mrange = 2
bits = 14
gravity = 9.81
max_val = 2**(bits-1)
fs = 800

N = len(data[:,0])
t = np.array(range(0,N,1))
t = t/fs

acc_x = data[:,0]/max_val*mrange*gravity
acc_y = data[:,1]/max_val*mrange*gravity
acc_z = data[:,2]/max_val*mrange*gravity

frq = acoustics.signal.OctaveBand(fstart=0.5, fstop=100, fraction=3)
filt = acoustics.signal.Filterbank(frq, sample_frequency=fs)

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('text.latex', unicode=True)
plt.rc('lines', linewidth=0.5)

plt.figure(1)
plt.plot(t[0:1000], acc_x[0:1000])
plt.grid(True)
plt.xlabel(r'Czas [s]')
plt.ylabel(r'Przyspieszenie drgań [ms\textsuperscript{-2}]')
plt.savefig('accel_x.pdf')

plt.figure(2)
plt.plot(t[0:1000], acc_y[0:1000])
plt.grid(True)
plt.xlabel(r'Czas [s]')
plt.ylabel(r'Przyspieszenie drgań [ms\textsuperscript{-2}]')
plt.savefig('accel_y.pdf')

plt.figure(3)
plt.plot(t[0:1000], acc_z[0:1000])
plt.grid(True)
plt.xlabel(r'Czas [s]')
plt.ylabel(r'Przyspieszenie drgań [ms\textsuperscript{-2}]')
plt.savefig('accel_z.pdf')

filt_x = filt.power(acc_x)
filt_y = filt.power(acc_y)
filt_z = filt.power(acc_z)

freqs = np.arange(len(filt_x))

plt.figure(4)
plt.bar(freqs,filt_x,1)
plt.grid(True)
plt.xlabel(r'Częstotliwości środkowe pasm [Hz]')
plt.ylabel(r'Energia sygnału')
plt.savefig('power_x.pdf')

plt.figure(5)
plt.bar(freqs,filt_y,1)
plt.grid(True)
plt.xlabel(r'Częstotliwości środkowe pasm [Hz]')
plt.ylabel(r'Energia sygnału')
plt.savefig('power_y.pdf')

plt.figure(6)
plt.bar(freqs,filt_z,1)
plt.grid(True)
plt.xlabel(r'Częstotliwości środkowe pasm [Hz]')
plt.ylabel(r'Energia sygnału')
plt.savefig('power_z.pdf')

plt.show()

