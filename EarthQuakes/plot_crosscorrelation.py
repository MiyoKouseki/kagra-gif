#
#! coding:utf-8

import matplotlib.pyplot as plt
import scipy
import numpy as np
import matplotlib.animation as animation
import matplotlib
import numpy as np
from  check_fw import is_record_in_fw0
import sys
from scipy import signal
sys.path.append("../../../lib/miyopy/miyopy")
import spectrum
from mpio import fetch_data, dump, load
import mpplot as mpp
from _timeseries import *

'''
memo
M5.2, 2018-03-27-06:39:10(UTC), 1206167968, WS of Iwo Jima, Japan
M6.6, 2018-03-26-09:51:00(UTC), 1206093078, Kimbe, Papua New Guinea
M6.4, 2018-03-25-20:14:47(UTC), 1206044105, NW of Saumlaki, Indonesia
M5.0, 2018-03-25-15:36:24(UTC), 1206027402, SE of Hachijo-jima, Japan
'''

EQ_name = {
    'Kimbe':[1206093078,32*2*64],
    'Saumlaki':[1206044105,32*2*32],
    'Hachijo-jima':[1206027402,32*2*64],
    }

def CoherencePlot(x,y,fn,ave,cl,unwrap=True,xlim=(1e0,1e3)):
    fig = plt.figure()
    ax1 = fig.add_axes([0.12, 0.58, 0.80, 0.40])  # coherence [l,b,w,h]
    ax2 = fig.add_axes([0.12, 0.13, 0.80, 0.40])  # phase   
    f, coh = signal.coherence(x, y, 16, nperseg=len(x)/ave)
    ax1.semilogx(f,coh,linewidth=0.5,label='a',color='black') #for multi
    ax1.set_ylabel("Coherence")
    clfunc = lambda a: 1.0-(1.0-a/100.0)**(1./(ave-1))    
    ax1.text(f[1], clfunc(cl)*0.9, '{0:3.2f}%'.format(cl),bbox={'facecolor':'w', 'alpha':0.9, 'pad':0.5})# footter
    # Phase
    #ax2.grid(True, which="major",linestyle=':')
    #ax2.grid(True, which="minor",linestyle=':')
    ax2.set_xlabel("Frequency [Hz]")
    ax2.set_ylabel("Phase")
    _f,csd = signal.csd(
        x = x,
        y = y,
        fs = 16,
        nperseg = len(x)/ave,
        scaling = 'spectrum'
    )
    #exit()
    cohphase = np.arctan2(csd.imag,csd.real)
    ax2.semilogx(_f,cohphase,linewidth=0.5,label='b',color='black')
    ax1.set_ylim([0,1])
    ave    = ave # 16回平均
    nFFT   = len(x)/ave
    window = np.hanning(nFFT)
    enbw   = spectrum.enbw(spectrum.create_window(nFFT, 'hanning'))*16/nFFT
    text = '''StartGPSTime:{0}, Average:{1}, Overrap:50%, Window:Hanning, ENBW:{2:3.2e} Hz'''.format(gpsstart,ave,enbw)
    ax3 = fig.text(0.08, 0.01, text)              # footter
    # Close Graph   
    plt.savefig(fn)   
    plt.close()
    #return fig    
    
if __name__ == '__main__':
    name = 'Kimbe'
    gpsstart = EQ_name[name][0]
    duration = EQ_name[name][1]
    pm = TimeSeries(gpsstart,duration)
    data = pm.loadData_pickle()
    #
    start,end = 0,2**16
    start,end = 2**14,2**15
    #start,end = 0,2**16
    EX1_NS = data[pm.chdic['K1:PEM-EX1_SEIS_WE_SENSINF_OUT16']][start:end]
    EY1_NS = data[pm.chdic['K1:PEM-EY1_SEIS_NS_SENSINF_OUT16']][start:end]
    IY0_NS = data[pm.chdic['K1:PEM-IY0_SEIS_WE_SENSINF_OUT16']][start:end]
    #
    EX1_WE = data[pm.chdic['K1:PEM-EX1_SEIS_WE_SENSINF_OUT16']][start:end]
    EY1_WE = data[pm.chdic['K1:PEM-EY1_SEIS_WE_SENSINF_OUT16']][start:end]
    IY0_WE = data[pm.chdic['K1:PEM-IY0_SEIS_WE_SENSINF_OUT16']][start:end]
    #
    EX1_Z = data[pm.chdic['K1:PEM-EX1_SEIS_Z_SENSINF_OUT16']][start:end]
    EY1_Z = data[pm.chdic['K1:PEM-EY1_SEIS_Z_SENSINF_OUT16']][start:end]
    IY0_Z = data[pm.chdic['K1:PEM-IY0_SEIS_Z_SENSINF_OUT16']][start:end]
    time = np.arange(len(EX1_NS))/16.0
    #
    data = [[time,EX1_NS],[time,EX1_WE],[time,EX1_Z],
            [time,IY0_NS],[time,IY0_WE],[time,IY0_Z],
            [time,EY1_NS],[time,EY1_WE],[time,EY1_Z]]    
    title = ['EX1_NS','EX1_WE','EX1_Z',
             'IY0_NS','IY0_WE','IY0_Z',
             'EY1_NS','EY1_WE','EY1_Z']    
    mpplot.subplot33(data,'{0}_{1}.png'.format(name,gpsstart),title)
    #EX1_NS = np.sin(1./50*time+1)
    #EY1_NS = np.sin(1./50*time)
    Vx = EX1_WE
    Vy = EY1_NS
    plt.subplot(211)
    b, a = signal.butter(1, 6/2.0/np.pi, 'low', analog=True)
    print b,a
    def sekibun(v,dt):
        n = len(v)
        x = np.ones(n)*dt
        for i in range(n-1):
            x[i] = (v[i]+v[i+1])*x[i]
        return x[:-1]
    
    #b, a = [1], [1,0.01]
    #w, h = signal.freqs(b, a, plot=lambda w, h: plt.loglog(w, abs(h)))
    #plt.show()
    Y = sekibun(Vy,1.0/16)
    X = sekibun(Vx,1.0/16)
    print X
    #Y = Vy*1.0/16.0
    #X = Vx*1.0/16.0
    plt.plot(time[:-1],X-Y)
    plt.plot(time,Vx)
    plt.subplot(212)
    plt.plot(time,Vy)
    plt.savefig('hoge.png')
    plt.close()    
    CoherencePlot(Vx, Vy, fn='coherence_micns',ave=8,cl=99.99)
    
