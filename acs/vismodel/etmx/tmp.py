#
#! coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert
from gwpy.frequencyseries import FrequencySeries

import re
import warnings
warnings.filterwarnings('ignore')

# Utils
def degwrap(phases):
    '''
    phases :  float
        phase of degree.
    '''
    phases = np.deg2rad(phases)
    phases = ( phases + np.pi) % (2 * np.pi ) - np.pi
    phases = np.rad2deg(phases)
    return phases

import control
from control import matlab
def tf(sys,omega):
    print ('calc sys.freqresp')
    mag, phase, omega = control.matlab.bode(sys,omega,Plot=False)
    mag = np.squeeze(mag)
    phase = np.squeeze(phase)
    G = mag*np.exp(1j*phase)
    freq = omega/(2.0*np.pi)
    print('calc sys.freqresp. Convert FreqSeries')
    hoge = FrequencySeries(G,frequencies=freq)
    return hoge


''' 
センサーコレクションされたLVDTの信号がGeophoneと比べてどう違うかしらべた。
条件：IPのループを閉じた状態でLVDTの信号を地震計の信号を引いてコレクションした。

結果: butter10mHz.png
結果: elipse10mHz.png


'''
# LVDT Noise
_freq, f0gas, h1, h2, h3 = np.loadtxt('../noise/LVDTnoiseETMX_disp.dat').T
lvdt = np.sqrt(h1**2 + h2**2 + h3**2)
nlvdt = FrequencySeries(lvdt,frequencies=_freq,name='ETMX_LVDT_L',unit='um') # m/rtHz
nlvdt.override_unit('m')
#_lvdt = lvdt.interpolate(0.0009765625)

# Geophone
_freq, geo = np.loadtxt('../noise/GEOnoiseproto_vel.dat').T
geo = np.sqrt(3)*geo
geo = FrequencySeries(geo,frequencies=_freq,name='ETMX_GEO_L',unit='um/sec') # m/rtHz
#Ge = 276 #[V/(m/s)], sensitivity
Ge = 1 #[V/(m/s)], sensitivity
eta = 0.28 # [], damping ratio
w0 = 1*2*np.pi # [rad/sec], resonant frequency
num = [-Ge,0,0]
den = [1,2*eta*w0,w0**2]
geo_tf = matlab.tf(num,den)
_omega = _freq*2.0*np.pi
geo_tf = tf(geo_tf,_omega)
ngeo = (geo/(geo_tf*(1j*_omega))).abs()


# case1: Use Butter Filter (10mHz)   
start = tconvert('Sep 02 2019 12:14:00 JST')
end   = tconvert('Sep 02 2019 13:24:00 JST')

# case2: Use Eliptic Filter (10mHz)
#start = tconvert('Sep 02 2019 17:06:00 JST')
#end   = tconvert('Sep 02 2019 18:06:00 JST')

kwargs = {'host':'10.68.10.122','port':8088,'verbose':True,'pad':0.0}
seis = TimeSeries.fetch('K1:PEM-SEIS_EXV_GND_X_OUT_DQ',start,end,**kwargs)
lvdt = TimeSeries.fetch('K1:VIS-ETMX_IP_BLEND_LVDTL_IN1_DQ',start,end,**kwargs)
geo = TimeSeries.fetch('K1:VIS-ETMX_IP_BLEND_ACCL_IN1_DQ',start,end,**kwargs)

lvdt = lvdt.resample(512)
geo = geo.resample(512)

# Timeseries
t0 = seis.t0.value
_seis = seis.crop(t0,t0+50)
_geo = geo.crop(t0,t0+50)
_lvdt = lvdt.crop(t0,t0+50)

fig,ax = plt.subplots(3,1,figsize=(8,6),sharex=True)
ax[0].plot(seis,label='seis')
ax[1].plot(lvdt,label='lvdt')
ax[2].plot(geo,label='geo')
ax[0].set_ylim(-1,1)
ax[1].set_ylim(-1,1)
ax[2].set_ylim(-3,3)
ax[0].legend()
ax[1].legend()
ax[2].legend()
ax[0].set_xscale('auto-gps')
ax[1].set_xscale('auto-gps')
ax[2].set_xscale('auto-gps')
plt.savefig('huge.png')
plt.close()

# differential motion 
diff = lvdt - geo


# Spectrum
fftlen = 2**6
ovlp = fftlen/2
coh = lvdt.coherence(geo, fftlength=fftlen, overlap=ovlp) # 2**7 = 128
#coh1 = lvdt.coherence(seis, fftlength=fftlen, overlap=ovlp) # 2**7 = 128
#coh2 = seis.coherence(geo, fftlength=fftlen, overlap=ovlp) # 2**7 = 128
gndfft = lvdt.average_fft(fftlen, ovlp, window='hamming')
hpifft = geo.average_fft(fftlen, ovlp, window='hamming')
size = min(gndfft.size, hpifft.size)
tf = hpifft[:size]/1j / gndfft[:size]

seis  =  seis.asd(fftlength=fftlen, overlap=ovlp)
lvdt = lvdt.asd(fftlength=fftlen, overlap=ovlp)
diff = diff.asd(fftlength=fftlen, overlap=ovlp)
geo = geo.asd(fftlength=fftlen, overlap=ovlp)
freq = seis.frequencies.value
omega = 2.0*np.pi*freq
seis = seis/omega
geo = geo/omega

# plot
fig,(ax0,ax1,ax2) = plt.subplots(3,1,figsize=(8,8))
#ax0.loglog(seis,label='GND',color='k')
ax0.loglog(lvdt,label='Corrected LVDT',color='b',linestyle='-')
ax0.loglog(nlvdt*0.3,label='Noise LVDT',color='b',linestyle=':',alpha=0.3)
ax0.loglog(geo,label='Geophone',color='r',linestyle='-')
ax0.loglog(ngeo,label='Noise Geophone',color='r',linestyle=':',alpha=0.3)
#ax0.loglog(diff,label='LVDT - GEOPHONE',color='g',linestyle='-')
ax0.legend(fontsize=10,loc='upper right')
ax0.set_ylabel('Diplacement [um/rtHz]')
ax0.set_ylim(1e-4,2e-1)
ax0.set_xlim(1e-2, 10)
ax1.semilogx(coh,label='LVDT vs Geophone',color='k',linestyle='-')
#ax1.semilogx(coh1,label='LVDT vs Seis',color='b',linestyle='-')
#ax1.semilogx(coh2,label='Seis vs Geophone',color='r',linestyle='-')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Coherence')
ax1.set_ylim(0, 1)
ax1.set_xlim(1e-2, 10)
# ax3.loglog(tf.abs(),label='seis vs Geophone',color='k',linestyle='-')
# ax3.set_xlabel('Frequency [Hz]')
# ax3.set_ylabel('Coherence')
# ax3.set_xlim(1e-2, 10)
phase = degwrap(np.rad2deg(np.unwrap(tf.angle().value)-np.pi))
print tf.angle().value
phase = tf.angle().rad2deg()
print phase.shape
ax2.semilogx(phase,label='LVDT vs Geophone',color='k',linestyle='-')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_xlim(1e-2, 10)
ax2.set_ylim(-180, 180)
ax2.set_yticks(range(-180, 181, 90))
ax1.legend(fontsize=12,loc='upper right')
ax2.legend(fontsize=12,loc='upper right')
#plt.savefig('results_butter10mHz.png') # case1
plt.savefig('results_elipse10mHz.png') # case2
plt.close()
