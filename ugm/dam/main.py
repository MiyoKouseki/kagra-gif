#
#! coding:utf-8

from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('hoge.csv',delimiter=',')
minutes = data[:,0]*60 + data[:,1]*1
time = minutes*60 + float(tconvert('Jul 19 2019 00:00:00 JST'))
drain = data[:,2]/8000


value = np.fromfile('value') # fs=16
times = np.fromfile('time')
seis = TimeSeries(value,times=times,unit='um/sec',name='EYV_Z')
seis = seis.rms(60)
fig,ax = plt.subplots(1,1,figsize=(10,6))
ax.plot(seis)
ax.plot(time,drain,'ko',label='Water Drain [m3/s] /2000')
ax.set_ylabel('Ground Velocity [um/sec]')
ax.set_xlabel('GPS Time')
ax.legend(fontsize=20)
ax.set_ylim(0,0.025)
#ax.set_xscale('auto-gps')
plt.savefig('hoge.png')
plt.close()
