#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt


olddata = 'IMCOOL.dat'
newdata = 'freqnoise.txt'


A = np.loadtxt(olddata)

plt.figure(101)
plt.loglog(A[:,0], A[:,1], label='old noise model')


B = np.loadtxt(newdata)
plt.loglog(B[:,0], B[:,1], label='updated noise model')
plt.grid()

plt.xlabel('Frequency [Hz]')
plt.ylabel('Frequency noise [Hz/rtHz]')

plt.savefig('freqnoise_comparison.png', transparent=True)
plt.savefig('freqnoise_comparison.pdf')
plt.show()

