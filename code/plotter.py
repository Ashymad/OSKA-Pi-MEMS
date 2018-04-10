#!/usr/bin/env python3

import h5py as h5
import acoustics
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.constants import g as gravity
from mma8451.files import dataread
import locale
import sys
import re
import os
import platform
import io

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_NUMERIC, 'Polish')
else:
    locale.setlocale(locale.LC_NUMERIC, ('pl_PL', 'UTF-8'))

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]  

mrange = 2
bits = 14
max_val = 2**(bits-1)
fs = 800
def toint(d): return d/max_val*mrange*gravity
def rms(d): return np.sqrt(np.mean(np.square(d)))
def gent(N, fs=800): return np.array(range(0,N,1))/fs

mpl.use("pgf")

axes = ['x', 'y', 'z']



def plot1():
    # Przebieg czasowy pomiaru w D-1
    with h5.File('data.h5','r') as f:
        data = toint(dataread(f, "2018", '03', '23', '07'))

    plot_N = 1000
    t = gent(plot_N)

    for i in range(0,3):
        plt.figure()
        plt.xlabel(r'Czas [\si{\second}]')
        plt.ylabel(r'Przyspieszenie drgań [\si{\meter\per\second\squared}]')
        plt.plot(t, acc[0:plot_N,i])
        plt.savefig('../artykul/plots/accel_' + axes[i] + ".pgf")

def plot2():
    # Wyniki pomiaru w D-1 w postaci tercji
    with h5.File('data.h5','r') as f:
        data = toint(dataread(f, "2018", '03', '23', '07'))
    frq = acoustics.signal.OctaveBand(fstart=0.5, fstop=350, fraction=3)
    filtbank = acoustics.signal.Filterbank(frq, sample_frequency=fs)
    frq_rng = [str(s).replace('.', ',') for s in np.round(frq.nominal, 14)]
    bar_width = 0.9

    for i in range(0,3):
        filt = np.sqrt(filtbank.power(acc[:,i]))
        lin = np.arange(len(filt))
        plt.figure()
        plt.bar(lin, filt, bar_width)
        plt.xticks(lin, frq_rng, rotation=70)
        plt.xlabel(r'Częstotliwości środkowe pasm [\si{\hertz}]')
        plt.ylabel(r'Amplituda sygnału [\si{\meter\per\second\squared}]')
        plt.savefig('../artykul/plots/ghost_' + axes[i] + ".pgf")


def plot3():
    # Pomiar obratu w ręce
    with h5.File('data2.h5','r') as f:
        data2 = toint(dataread(f, "2018"))

    plot_S = 1400
    plot_E = 6700
    t = gent(plot_E-plot_S)

    plt.figure()
    plt.xlabel(r'Czas [\si{\second}]')
    plt.ylabel(r'Przyspieszenie drgań [\si{\meter\per\second\squared}]')
    for i in range(0,3):
        plt.plot(t, acc2[plot_S:plot_E,i])
    plt.legend(["oś " + ax for ax in axes])
    plt.savefig('../artykul/plots/accel_2_xyz.pgf')

def plot4():
    # Charakterystyka częstotliwościowa w osi Y
    with h5.File('./Rasp/data.frqamp.h5','r') as f:
        data_mems = dataread(f, "2018", "04", "06", "11", merge=False)
        data_mems.extend(dataread(f, "2018", "04", "06", "12", [0, 37],
                                  merge=False))
        data_mems = [rms(toint(el[:,1]) - np.mean(toint(el[:,1]))) for el in data_mems]

    data_ni = list()
    path = "./NI/freq_char"
    files = os.listdir(path)
    files.sort(key=natural_sort_key)
    for file in files:
        data_ni.append(rms(np.loadtxt(path+"/"+file)))

    data_diff = 10*np.log10(np.divide(data_mems,data_ni))

    frq = np.append(np.arange(15, 106, 10),np.arange(150, 400, 50))
    bar_width = 0.9
    lin = np.arange(len(data_diff))
    plt.figure()
    plt.bar(lin, data_diff, bar_width)
    plt.xticks(lin, frq, rotation=70)
    plt.xlabel(r'Częstotliwości badane [\si{\hertz}]')
    plt.ylabel(r'Róznica [\si{\decibel}]')
    plt.savefig('../prez/char.pdf')

def plot5():
    # Czułość
    with h5.File('./Rasp/data.frqamp.h5','r') as f:
        data_mems = toint(dataread(f, "2018", "04", "06", "12", "43")[:,1])
    data_mems -= np.mean(data_mems)
    s = open('./NI/sensitivity.txt').read().replace(',','.')
    data_ni = np.loadtxt(io.StringIO(s))
    data_ni -= np.mean(data_ni)

    plt.figure()
    plt.xlabel(r'Czas [\si{\second}]')
    plt.ylabel(r'Przyspieszenie drgań [\si{\meter\per\second\squared}]')
    t1 = gent(len(data_mems))
    t2 = gent(len(data_ni), fs=10240)
    plt.subplot(211)
    plt.plot(t1,data_mems)
    plt.xlim(25, 27)
    plt.ylim(-0.1,0.1)
    plt.legend("MEMS")
    plt.subplot(212)
    plt.plot(t2,data_ni)
    plt.xlim(26.20, 28.20)
    plt.ylim(-0.1,0.1)
    plt.legend("PCB")
    plt.savefig('../prez/sens.pdf')

{# This works!
    '1': plot1,
    '2': plot2,
    '3': plot3,
    '4': plot4,
    '5': plot5,
}[sys.argv[1]]()
