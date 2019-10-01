#
#! coding:utf-8

from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('waterdrain.csv',delimiter=',')
minutes = data[:,0]*60 + data[:,1]*1
time = minutes*60 + float(tconvert('Jul 19 2019 00:00:00 JST'))
drain = data[:,2]/8000

if True: # Download samewhere. I forgot.
    value = np.fromfile('eyv_z_out16_value') # fs=16
    times = np.fromfile('eyv_z_out16_time')
    seis = TimeSeries(value,times=times,unit='um/sec',name='EYV_Z')
    seis = seis.rms(60)

if False: # No data in Kamioka NDS...
    start,end = time[0],time[-1]
    print(tconvert(start))
    print(start)
    print(tconvert(end))
    chname = 'K1:PEM-SEIS_EYV_GND_Z_OUT16'
    seis = TimeSeries.fetch(chname,start,end,host='10.68.10.121',port=8088)
    print(seis)
    

fig,ax = plt.subplots(1,1,figsize=(10,6))
ax.plot(seis,label='EXV')
ax.plot(time,drain,'ko',label='Water Drain [m3/s] /8000')
ax.set_ylabel('Ground Velocity [um/sec]')
#ax.set_xlabel('GPS Time')
ax.legend(fontsize=20)
ax.set_ylim(0,0.025)
ax.set_xscale('auto-gps')
plt.savefig('result.png')
plt.close()
