from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert
import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np

#/opt/rtcds/userapps/release/lsc/k1/guardian
start = tconvert('Nov 25 2019 21:00:00 JST')
end   = tconvert('Nov 25 2019 22:00:00 JST')
end   = tconvert('Nov 26 2019 09:00:00 JST')
#end   = tconvert('Nov 26 2019 06:00:00 JST')
channels = ['K1:LSC-MICH1_INMON.rms,s-trend',
            'K1:GRD-LSC_LOCK_STATE_N.mean,s-trend',
            'K1:PEM-SEIS_IXV_GND_X_BLRMS_100M_300M_OUT16.rms,s-trend',
            'K1:PEM-SEIS_IXV_GND_X_BLRMS_300M_1_OUT16.rms,s-trend',
            'K1:PEM-SEIS_IXV_GND_X_BLRMS_1_3_OUT16.rms,s-trend',
]
data = TimeSeriesDict.fetch(channels,start,end,host='10.68.10.121',
                            port=8088,verbose=True)
error = data[channels[0]]
lock_state = data[channels[1]]
exv_mid = data[channels[2]]
exv_high = data[channels[3]]
exv_veryhigh = data[channels[4]]
# FPMI_LOCKED = 60
__lock_state = data[channels[1]] == 60.0*u.V
__lock_state_loss = data[channels[1]] != 60.0*u.V
flag = __lock_state.value
flag_loss = __lock_state_loss.value
_error = error[flag]
_lock_state = lock_state[flag]
_exv_mid = exv_mid[flag]
_exv_mid_loss = exv_mid[flag_loss]
_exv_high = exv_high[flag]
_exv_high_loss = exv_high[flag_loss]
_exv_veryhigh = exv_veryhigh[flag]
_exv_veryhigh_loss = exv_veryhigh[flag_loss]

if True:
    fig, ax = plt.subplots(3,1,figsize=(10,10))
    #
    n, bins, patches = ax[0].hist(_exv_mid_loss.value,bins=50,
                                  density=1,label='lost lock (100m - 300m Hz)',
                                  histtype='step',cumulative=True)
    patches[0].set_xy(patches[0].get_xy()[:-1])    
    n, bins, patches = ax[0].hist(_exv_mid.value,bins=50,
                                  histtype="step",label='stayed locked (100m - 300m Hz)',
                                  density=1,cumulative=True)
    patches[0].set_xy(patches[0].get_xy()[:-1])    
    ax[0].set_xscale('log')
    ax[0].legend()
    ax[0].set_ylim(0,1)
    ax[0].set_xlim(5e-2,1e1)
    ax[0].set_xlabel('um/sec')
    #
    n, bins, patches = ax[1].hist(_exv_high_loss.value,bins=50,
                                  density=1,label='lost lock (300m - 1 Hz)',
                                  histtype='step',cumulative=True)
    patches[0].set_xy(patches[0].get_xy()[:-1])    
    n, bins, patches = ax[1].hist(_exv_high.value,bins=50,
                                  histtype="step",label='stayed locked (300m - 1 Hz)',
                                  density=1,cumulative=True)
    patches[0].set_xy(patches[0].get_xy()[:-1])    
    ax[1].set_xscale('log')
    ax[1].legend()
    ax[1].set_ylim(0,1)
    ax[1].set_xlabel('um/sec')    
    #ax[1].set_xlim(5e-2,1e1)
    #
    n, bins, patches = ax[2].hist(_exv_veryhigh_loss.value,bins=50,
                                  density=1,label='lost lock (1 - 3 Hz)',
                                  histtype='step',cumulative=True)
    patches[0].set_xy(patches[0].get_xy()[:-1])    
    n, bins, patches = ax[2].hist(_exv_veryhigh.value,bins=50,
                                  histtype="step",label='stayed locked (1 -3 Hz)',
                                  density=1,cumulative=True)
    patches[0].set_xy(patches[0].get_xy()[:-1])    
    ax[2].set_xscale('log')
    ax[2].legend()
    ax[2].set_ylim(0,1)
    ax[2].set_xlabel('um/sec')    
    #ax[2].set_xlim(5e-2,1e1)
    #
    plt.savefig('huge.png')
    plt.close()
    
if True:
    fig, ax = plt.subplots(4,1,figsize=(10,10),sharex=True)
    #ax[0].plot(error,label='MICH ERROR')
    #ax[0].plot(_error,linestyle='none',marker='o',ms=1)
    ax[0].plot(lock_state,label='MICH STATUS N')
    ax[0].plot(_lock_state,linestyle='none',marker='o',ms=1)
    ax[1].plot(exv_mid,label='100m - 300m Hz')
    ax[1].plot(_exv_mid,linestyle='none',marker='o',ms=1)
    ax[2].plot(exv_high,label='300 - 1 Hz')
    ax[2].plot(_exv_high,linestyle='none',marker='o',ms=1)
    ax[3].plot(exv_veryhigh,label='1 - 3 Hz')
    ax[3].plot(_exv_veryhigh,linestyle='none',marker='o',ms=1)    
    ax[2].set_xscale('auto-gps')
    ax[1].set_ylim(0,2.5)
    ax[2].set_ylim(0,1)
    ax[3].set_ylim(0,0.1)
    ax[0].set_ylabel('[Count]')
    ax[1].set_ylabel('Velocity [um/sec]')
    ax[2].set_ylabel('Velocity [um/sec]')
    ax[3].set_ylabel('Velocity [um/sec]')
    ax[0].legend()
    ax[1].legend()
    ax[2].legend()
    ax[3].legend()
    plt.savefig('hoge.png')
    plt.close()
