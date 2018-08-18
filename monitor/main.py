#
#! coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 100000

from gwpy.timeseries import TimeSeries
from miyopy.timeseries import TimeSeries as ts
#from tips import *

from scipy.signal import butter,lfilter,freqz
from scipy import signal

def plot_bode(ax0,ax1,b,a,fs,label):
    w, h = freqz(b, a, worN=8000)
    mag = np.abs(h)
    phase = np.rad2deg(np.angle(h))
    if True in np.isinf(h):
        raise ValueError('Data have Inf value! \n Exit..')
    ax0.loglog((fs*0.5/np.pi)*w, mag, label=label)
    ax0.grid(which='major',linestyle='-', linewidth=1)
    ax0.grid(which='minor',linestyle=':', linewidth=1)
    ax0.set_ylim([1e-2,1e0])
    ax0.set_ylabel('Magnitude')            
    ax1.semilogx((fs*0.5/np.pi)*w,phase,label=label)
    ax1.grid(which='major',linestyle='-', linewidth=1)
    ax1.grid(which='minor',linestyle=':', linewidth=1)
    ax0.legend(loc='upper right')    
    ax1.legend(loc='upper right')
    return ax0,ax1

def _bandpass(data, lowcut, highcut, fs, order=3, w=None, passtype='band',**kwargs):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    if passtype=='band':
        b, a = butter(order, [low, high], btype='band',analog=False)
    elif passtype=='low':
        b, a = butter(order, low, btype='low',analog=False)
    elif passtype=='high':
        b, a = butter(order, high, btype='high',analog=False)
    else:
        raise ValueError('Invalid pass parameter: {}'.format(passtype))
    y = lfilter(b, a, data)
    return y,b,a


def main_diary(start,end,chname):
    print('Loading data from nds server... It may take few minutes..')
    print('ChannelName : {}'.format(chname))
    data = TimeSeries.fetch(chname,start, end, host='10.68.10.121', port=8088)
    print('Done.')
    value = data.value
    nlen = len(value)    
    tlen = float(end-start)
    fs = nlen/tlen
    time = np.arange(nlen)/fs/60.0 # min
    value_dc,b_dc,a_dc       = _bandpass(value,0.01,0.04,fs,passtype='low')
    value_low,b_low,a_low    = _bandpass(value,0.01 ,0.05 ,fs)    
    value_mid,b_mid,a_mid    = _bandpass(value,0.05  ,0.3 ,fs)
    value_high,b_high,a_high = _bandpass(value,0.3  ,1   ,fs)
    if False:
        fig, (ax0,ax1) = plt.subplots(2,1,figsize=(10,6),dpi=640)
        plt.subplots_adjust(hspace=0.05,top=0.92)        
        ax0, ax1 = plot_bode(ax0,ax1,b_dc,a_dc,fs,label='DC (-0.01 Hz)')
        ax0, ax1 = plot_bode(ax0,ax1,b_low,a_low,fs,label='Low (0.01-0.05 Hz)')        
        ax0, ax1 = plot_bode(ax0,ax1,b_mid,a_mid,fs,label='Mid (0.05-0.3 Hz)')
        ax0, ax1 = plot_bode(ax0,ax1,b_high,a_high,fs,label='High (0.3-1.0 Hz)')
        ax1.set_yticks(np.arange(-180,181,90))
        ax1.set_yticklabels(np.arange(-180,181,90))
        ax1.set_ylim([-200,200])
        ax1.set_ylabel('Phase [Degree]')                
        ax1.set_xlabel('Frequency [Hz]')                    
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.suptitle("Bandpass filter")        
        plt.savefig('bandpass.png')
        plt.close()        
        print('plot "bandpass.png"')
    if True:
        fig, (ax0,ax1,ax2,ax3,ax4) = plt.subplots(5,1,figsize=(10,6),dpi=640)
        plt.subplots_adjust(hspace=0.05,top=0.92)        
        max = np.max(value)
        min = np.min(value)
        ylim = (max-min)/2.0
        ax0.set_ylim(-ylim,ylim)
        ax1.set_ylim(-ylim,ylim)
        ax2.set_ylim(-ylim,ylim)
        ax3.set_ylim(-ylim,ylim)
        ax4.set_ylim(-ylim,ylim)
        ax0.plot(time,value,label='No filt',color='k')
        ax1.plot(time,value_dc,label='DC (-0.01 Hz)',color='k')       
        ax2.plot(time,value_low,label='Low (0.01-0.05 Hz)',color='k')
        ax3.plot(time,value_mid,label='Mid (0.05-0.3 Hz)',color='k')
        ax4.plot(time,value_high,label='High (0.3-1.0Hz)',color='k')
        ax0.legend()    
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax0.grid(which='major',linestyle='--', linewidth=1)
        ax1.grid(which='major',linestyle='--', linewidth=1)
        ax2.grid(which='major',linestyle='--', linewidth=1)
        ax3.grid(which='major',linestyle='--', linewidth=1)
        ax4.grid(which='major',linestyle='--', linewidth=1)
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_xticklabels(), visible=False)        
        ax_pos = ax4.get_position()
        fig.text(ax_pos.x1*1.01, ax_pos.y0,
                 'GPS: {0}\nChannelName: {1}'.format(start,chname),
                 rotation=90,verticalalignment='bottom')
        fig.text(.05, .5, 'Velocity [count]',
                 ha='center', va='center', rotation='vertical')        
        ax4.set_xlabel('Time [minutes]')
        plt.suptitle(chname)
        fname = 'TimeSeries_{0}_{1}_{2}.png'.format(start,end,chname)
        plt.savefig(fname)
        plt.close()
        print('plot {0}'.format(fname))


if __name__ == '__main__':
    import sys 
    argvs = sys.argv
    argc = len(argvs)
    if argc == 4:
        _,start,end,chname = argvs
    else:
        raise ValueError('Usage: # python {start} {end} {chname}')
    
    main_diary(int(start),int(end),chname)
