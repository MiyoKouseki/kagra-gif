#
#! coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal 
from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    #
    fname = 'figure_lowpassfilter.png'
    w, h = signal.freqs(b, a)
    plt.loglog(w, abs(h))
    #plt.title('Butterworth filter frequency response')
    #plt.xlabel('Frequency [radians / second]')
    #plt.ylabel('Amplitude [dB]')
    #plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    plt.savefig(fname)
    return y


#
fs = 8.0
v = np.loadtxt('./sample.txt')#[:2**9]
v_ = signal.detrend(v)
v_ = v
t = np.arange(len(v))/fs
v1 = butter_bandpass_filter(v_,0.05,0.1,fs,order=3)
v2 = butter_bandpass_filter(v_,0.1,0.25,fs,order=3)
v3 = butter_bandpass_filter(v_,0.3,0.5,fs,order=3)
#
f, psd = signal.welch(x=v,fs=fs,nperseg=len(v)/2,window='hanning')
f, psd_1 = signal.welch(x=v1,fs=fs,nperseg=len(v)/2,window='hanning')
f, psd_2 = signal.welch(x=v2,fs=fs,nperseg=len(v)/2,window='hanning')
f, psd_3 = signal.welch(x=v3,fs=fs,nperseg=len(v)/2,window='hanning')

fname = 'figure_timeseries.png'
plt.figure(figsize=(12,6),dpi=100)
plt.plot(t,v_,'ko-',linewidth=1,markersize=1)
plt.plot(t,v1,'ro-',linewidth=1,markersize=1)
plt.plot(t,v2,'go-',linewidth=1,markersize=1)
#plt.plot(t,v3,'bo-',linewidth=1,markersize=1)
plt.savefig(fname)
plt.close()

fname = 'figure_asd.png'
plt.figure(figsize=(6,6),dpi=100)
plt.loglog(f,np.sqrt(psd),'ko-',linewidth=1,markersize=1)
plt.loglog(f,np.sqrt(psd_1),'ro-',linewidth=1,markersize=1)
plt.loglog(f,np.sqrt(psd_2),'go-',linewidth=1,markersize=1)
plt.loglog(f,np.sqrt(psd_3),'bo-',linewidth=1,markersize=1)
plt.ylim(1e-10,1e-6)
plt.savefig(fname)
plt.close()
