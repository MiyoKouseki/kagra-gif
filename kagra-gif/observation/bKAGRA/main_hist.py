import numpy as np

from astropy import units as u
import matplotlib.pyplot as plt

from gwpy.timeseries import StateTimeSeries
from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert

''' 

1. bKAGRA_rms_ground_velocity_hor.gwf

Start : 2018-04-07 00:00:42 JST 
End   : 2018-06-01 00:00:42 JST 
Channel : 'K1:PEM-EX1_SEIS_WE_BLRMS_LOW_OUT_DQ.rms'
- RMS of horizontal ground velocity at the site within a 10-minute interval
after a band-bass filter (0.01-1Hz).

2. bKAGRA_mich_state.gwf
Start : 2018-04-07 00:00:42 JST 
End   : 2018-06-01 00:00:42 JST 


'''

__author__ = 'Koseki.miyo'

seis = TimeSeries.read('bKAGRA_rms_ground_velocity_hor.gwf',
                       'K1:PEM-EX1_SEIS_WE_BLRMS_LOW_OUT_DQ.rms',
                       format='gwf.lalframe')*1e6
#s = 
#seis[:2000] = np.zeros(2000)

mich = TimeSeries.read('bKAGRA_mich_state.gwf',
                       'K1:GRD-LSC_MICH_STATE_N',
                       start=tconvert('Apr 28 2018 09:00:00 JST'),
                       end=tconvert('May 6 2018 09:00:00 JST')+78,   
                       format='gwf.lalframe')
start = tconvert('May 5 2018 1:0:0 JST')
end   = tconvert('May 5 2018 7:0:0 JST')
_seis = seis.crop(start,end)
_mich = mich.crop(start,end)
start = tconvert('May 5 2018 8:59:0 JST')
end   = tconvert('May 5 2018 9:0:0 JST')
__seis = seis.crop(start,end)
__mich = mich.crop(start,end)
start = tconvert('Apr 28 2018 9:0:0 JST')
end   = tconvert('May 5 2018 0:0:0 JST')
seis = seis.crop(start,end)
mich = mich.crop(start,end)
seis = seis.append(_seis,gap='pad',pad=0.0,inplace=False)
mich = mich.append(_mich,gap='pad',pad=0.0,inplace=False)
seis = seis.append(__seis,gap='pad',pad=0.0,inplace=False)
mich = mich.append(__mich,gap='pad',pad=0.0,inplace=False)
print(seis)
mich = mich.resample(1./600.0)
_mich = (mich == 100).value
_mich_loss = (mich < 100).value

seis_loss = seis[_mich_loss]
print(seis)
print(mich)
fig, ax = plt.subplots(1,1,figsize=(9,6))
ax.plot(seis,color='black')
ax.plot(seis_loss,color='red',linestyle='none',markersize=1,marker='o')
ax.set_xscale('auto-gps')
ax.set_ylim(0,2)
plt.savefig("hoge.png")
plt.close()

if True:
    fig, ax = plt.subplots(1,1,figsize=(7,6))
    #
    bins = 50
    n, bins, patches = ax.hist(seis.value,bins=bins,density=1,color='blue',
                                  label='stayed locked (0.01 - 1 Hz)',   
                                  histtype='step',cumulative=True)
    patches[0].set_xy(patches[0].get_xy()[:-1])
    bins = 50
    n, bins, patches = ax.hist(seis_loss.value,bins=bins,color='red',
                                  histtype="step",
                                  label='lock lost (0.01 - 1 Hz)',
                                  density=1,cumulative=True)
    patches[0].set_xy(patches[0].get_xy()[:-1])    
    ax.set_xscale('log')
    ax.legend(loc='upper left')
    ax.set_ylim(0,1)
    ax.set_xlim(1e-2,5e0)
    ax.set_xlabel('Velocity [um/sec]')
    ax.set_ylabel('Cumulative\n Distribution function')
    #    
    #ax.set_xscale('auto-gps')
    plt.savefig("huge.png")
    plt.close()
