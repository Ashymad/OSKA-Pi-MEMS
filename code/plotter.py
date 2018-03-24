import h5py as h5
import acoustics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
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

acc_x -= np.mean(acc_x)
acc_y -= np.mean(acc_y)
acc_z -= np.mean(acc_z)

frq = acoustics.signal.OctaveBand(fstart=0.5, fstop=100, fraction=3)
filt = acoustics.signal.Filterbank(frq, sample_frequency=fs)

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('text.latex', unicode=True)
plt.rc('lines', linewidth=0.5)

plot_N = 1000

plt.figure(1, figsize=(9,5))
plt.plot(t[0:plot_N], acc_x[0:plot_N])
plt.grid(True)
plt.xlabel(r'Czas [s]')
plt.ylabel(r'Przyspieszenie drgań [ms\textsuperscript{-2}]')
plt.savefig('figures/accel_x.pdf')

plt.figure(2, figsize=(9,5))
plt.plot(t[0:plot_N], acc_y[0:plot_N])
plt.grid(True)
plt.xlabel(r'Czas [s]')
plt.ylabel(r'Przyspieszenie drgań [ms\textsuperscript{-2}]')
plt.savefig('figures/accel_y.pdf')

plt.figure(3, figsize=(9,5))
plt.plot(t[0:plot_N], acc_z[0:plot_N])
plt.grid(True)
plt.xlabel(r'Czas [s]')
plt.ylabel(r'Przyspieszenie drgań [ms\textsuperscript{-2}]')
plt.savefig('figures/accel_z.pdf')

filt_x = filt.power(acc_x)
filt_y = filt.power(acc_y)
filt_z = filt.power(acc_z)

bar_width = 0.9

frq_rng = ['0,5', '0,63', '0,8', '1', '1,25', '1,6', '2', '2,5', '3,15', '4', '5', '6,3', '8', '10', '12,5', '16', '20', '25', '31,5', '40', '50', '63', '80', '100']
lin = np.arange(len(filt_x))

plt.figure(4, figsize=(9,5))
plt.bar(lin,filt_x,bar_width, tick_label=frq_rng)
plt.ylim([0, 0.0000025])
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%1.2g'))
plt.grid(True)
plt.xlabel(r'Częstotliwości środkowe pasm [Hz]')
plt.ylabel(r'Energia sygnału')
plt.savefig('figures/power_x.pdf')

plt.figure(5, figsize=(9,5))
plt.bar(lin,filt_y,bar_width, tick_label=frq_rng)
plt.ylim([0, 0.0000025])
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%1.2g'))
plt.grid(True)
plt.xlabel(r'Częstotliwości środkowe pasm [Hz]')
plt.ylabel(r'Energia sygnału')
plt.savefig('figures/power_y.pdf')

plt.figure(6, figsize=(9,5))
plt.bar(lin,filt_z,bar_width, tick_label=frq_rng)
plt.ylim([0, 0.0000025])
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%1.2g'))
plt.grid(True)
plt.xlabel(r'Częstotliwości środkowe pasm [Hz]')
plt.ylabel(r'Energia sygnału')
plt.savefig('figures/power_z.pdf')

# plt.show()

