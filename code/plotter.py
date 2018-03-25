import h5py as h5
import acoustics
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
from scipy.constants import g as gravity
from mma8451.files import dataread
import locale

locale.setlocale(locale.LC_NUMERIC, ('pl_PL', 'UTF-8'))

with h5.File('data.h5','r') as f:
    data = dataread(f, "2018", '03', '23', '07')

mrange = 2
bits = 14
max_val = 2**(bits-1)
fs = 800

N = len(data[:,0])
t = np.array(range(0,N,1))
t = t/fs

acc = data/max_val*mrange*gravity

frq = acoustics.signal.OctaveBand(fstart=0.5, fstop=100, fraction=3)
filtbank = acoustics.signal.Filterbank(frq, sample_frequency=fs)


mpl.use("pgf")

axes = ['x', 'y', 'z']

plot_N = 1000
frq_rng = [str(s).replace('.', ',') for s in np.round(frq.nominal, 14)]
bar_width = 0.9

for i in range(0,3):
    pl = plt.figure()
    plt.xlabel(r'Czas [\si{\second}]')
    plt.ylabel(r'Przyspieszenie drgań [\si{\meter\per\second\squared}]')
    plt.plot(t[0:plot_N], acc[0:plot_N,i])
    plt.savefig('../artykul/plots/accel_' + axes[i] + ".pgf")


    filt = np.sqrt(filtbank.power(acc[:,i]))
    lin = np.arange(len(filt))
    plt.figure()
    plt.bar(lin, filt, bar_width)
    plt.xticks(lin, frq_rng, rotation=70)
    plt.xlabel(r'Częstotliwości środkowe pasm [\si{\hertz}]')
    plt.ylabel(r'Amplituda sygnału [\si{\meter\per\second\squared}]')
    plt.savefig('../artykul/plots/ghost_' + axes[i] + ".pgf")
