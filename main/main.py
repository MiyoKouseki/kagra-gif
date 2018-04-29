#
#! coding:utf-8

import sys 
import numpy as np
from scipy import signal
from miyopy.types import Seismometer
import miyopy.io.reader as reader
import miyopy.plot.mpplot as mpplot
import subprocess
from scipy.signal import spectral
from miyopy.parse.arg import get_gpstime


EQ_name = {
    'Tottori':[1207240372,2**12],
    'Tottori_P-Wave':[1207240372,2**12],
    'Kimbe':[1206093078,32*2*64],
    'Kimbe_P-Wave':[1206093078+440,2**7],
    'Kimbe_S-Wave':[1206093078+800,2**11],
    'Kimbe_S-Wave':[1206093078+1200,2**9],
    'Kimbe_Other-Wave':[1206093078+1200,2**11],        
    'Saumlaki':[1206044105,32*2*32],
    'Hachijo-jima':[1206027402,32*2*64],
    'Example_MidNight':[1207407618,2**10], # 4/10 24:00
    'Example_MidNight':[1207407618,2**10], # 4/10 24:00
    'Example_MidNight2':[1207411218,2**10], # 4/10 25:00
    'Example_MidNight_Long':[1207234818,2**15], # 4/08 24:00        
    'Example_MidNight_Long2':[1207152018,2**16], # 4/08 24:00
    'Example_Night_Long':[1207213218,2**15], # 4/08 24:00
    'Example_Long_1day':[1207440018,2**16], # 04/11 09:00, 18hour
    #'Example_Long_1day':[1207440018,2**10], # 04/11 09:00, 18hour
    '0413_20h00m':[1207652418,2**14],
    '0413_20h00m':[1207652418,2**13], # 2**13 Ok KAGRA,GIF, 2**16made
    '0416_00h00m':[1207839618,2**13],        #2**15made
    '0416_13h00m':[1207886418,2**13], # 2**13 ok 
    '0416_16h00m':[1207897218,2**13], # OK
    '0416_19h00m':[1207908018,2**13], # OK
    '0416_22h00m':[1207918818,2**13], # OK
    '0417_01h00m':[1207929618,2**13], # OK 
    '0417_17h00m':[1207987218,2**13], # OK,2**16 made
    '0417_20h00m':[1207998018,2**13], # OK ,2**16 made
    '0417_23h00m':[1208008818,2**13], # OK ,2**16 made
    '0421chiba_all':[1208339257-2**10+100,2**11],
    '0421chiba_p':[1208339257+45,2**4],
    '0421chiba_pslove':[1208339257+45,2**7],
    '0421chiba_ps':[1208339257+40,2**6],
    '0421chiba':[1208339257-2**10,2**7],
    '0423shimane':[1208448078-2**6,2**9],
    '0425_heavy_rain':[],
    '0425_00':[1208617218,2**16],
    '0424_23':[1208617218-3600,2**10],
    }


def main():
    t0,tlen,title = get_gpstime(EQ_name)
    channels = ['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16']
    theta = 0
    ave = 2**7
    '''
    for theta in range(0,180,1):
        ex1 = Seismometer(t0,tlen,'EX1',theta=theta)
        ey1 = Seismometer(t0,tlen,'EY1',theta=theta)
        cen = Seismometer(t0,tlen,'IY0',theta=theta)
        # Yend-Xend
        ey1.x.get_coherence(ex1.x,ave=ave,plot=False)
        fname = '{0}/Coherence_{1:03d}_Xarm_YendXend'.format(title,theta)
        mpplot.CoherencePlot(ey1.x,fname,ave=ave,cl=99)
        # Yend-Cent
        ey1.x.get_coherence(cen.x,ave=ave,plot=False)
        fname = '{0}/Coherence_{1:03d}_Xarm_YendCent'.format(title,theta)
        mpplot.CoherencePlot(ey1.x,fname,ave=ave,cl=99)
        # Xend-Cent
        ex1.x.get_coherence(cen.x,ave=ave,plot=False)
        fname = '{0}/Coherence_{1:03d}_Xarm_XendCent'.format(title,theta)
        mpplot.CoherencePlot(ex1.x,fname,ave=ave,cl=99)
'''
    for theta in range(0,180,1):
        ex1 = Seismometer(t0,tlen,'EX1',theta=theta)
        ey1 = Seismometer(t0,tlen,'EY1',theta=theta)
        cen = Seismometer(t0,tlen,'IY0',theta=theta)
        # Yend-Xend
        ey1.y.get_coherence(ex1.y,ave=ave,plot=False)
        fname = '{0}/Coherence_{1:03d}_Yarm_YendXend'.format(title,theta)
        mpplot.CoherencePlot(ey1.y,fname,ave=ave,cl=99)
        # Yend-Cent
        ey1.y.get_coherence(cen.y,ave=ave,plot=False)
        fname = '{0}/Coherence_{1:03d}_Yarm_YendCent'.format(title,theta)
        mpplot.CoherencePlot(ey1.y,fname,ave=ave,cl=99)
        # Xend-Cent
        ex1.y.get_coherence(cen.y,ave=ave,plot=False)
        fname = '{0}/Coherence_{1:03d}_Yarm_XendCent'.format(title,theta)
        mpplot.CoherencePlot(ex1.y,fname,ave=ave,cl=99)
        
    
def main():
    t0,tlen,title = get_gpstime(EQ_name)
    print title
    theta = 21
    ave = 64
    ex1 = Seismometer(t0,tlen,'EX1',theta=theta)
    ey1 = Seismometer(t0,tlen,'EY1',theta=theta)
    cen = Seismometer(t0,tlen,'IY0',theta=theta)
    # Yend-Xend
    ey1.x.get_coherence(ex1.x,ave=ave,plot=False)
    fname = '{0}/Coherence_{1:03d}_Xarm_YendXend'.format(title,theta)
    mpplot.CoherencePlot(ey1.x,fname,ave=ave,cl=99)
    # 有意なところだけ抜きだす。
    clfunc = lambda a: 1.0-(1.0-a/100.0)**(1./(ave-1))    
    idx = np.where(ey1.x._coh>clfunc(99))
    phase = np.rad2deg(ey1.x._cohphase[idx])
    f = ey1.x._f[idx]
    idx = np.where(f>1.0)
    f = f[idx]
    phase = phase[idx]
    idx = np.where(f<2.0)
    f = f[idx]
    phase = phase[idx] #+ 180
    # 
    #
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit    
    f_ = np.logspace(-1,1,1e5)
    w = 2.0*f_
    def phasedelay(w,c):
        tau = 3.0*np.sqrt(2.0)*np.cos(np.deg2rad(20.0))/c
        #print tau*c
        print c,tau
        return np.angle(np.exp(-1j*tau*w))
    phase_ = phasedelay(w,c=0.32)
    phase_ = np.rad2deg(phase_)
    phase__ = phasedelay(w,c=5.5)
    phase__ = np.rad2deg(phase__)
    plt.semilogx(f,phase,'ko')
    plt.semilogx(f_,phase_,label='c=330 m/s')
    plt.semilogx(f_,phase__,label='c=5500 m/s')
    plt.legend(loc='upper left')
    plt.xlabel('Freqency [Hz]')
    plt.ylabel('Phase [degree]')
    plt.xlim(1e-1,1e1)
    plt.ylim(-180,180)
    plt.savefig('hoge.png')
    plt.close()    
    
def plot_spectrogram():
    data = ey1.x.timeseries
    samp_rate = ex1.x._fs
    nfft = ex1.x._nlen/ave
    mult=8.0 # 2**N 
    per_lap=0.9
    if mult is not None:
        mult = int(_nearest_pow_2(mult))
        mult = mult * nfft
    nlap = int(nfft * float(per_lap))
    from matplotlib import mlab
    from matplotlib.colors import Normalize
    specgram, freq, time = mlab.specgram(data, Fs=samp_rate, NFFT=nfft,
                                         pad_to=mult, noverlap=nlap)
    specgram = np.sqrt(specgram)
    freq = freq[1:]
    clip = [1e-10, 1e-2]
    _range = float(specgram.max() - specgram.min())
    vmin, vmax = clip
    vmin = specgram.min() + vmin * _range
    vmax = specgram.min() + vmax * _range
    norm = Normalize(vmin, vmax, clip=True)
    import matplotlib.pyplot as plt
    if True:
        halfbin_time = (time[1] - time[0]) / 2.0
        halfbin_freq = (freq[1] - freq[0]) / 2.0
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # pcolor expects one bin more at the right end
        freq = np.concatenate((freq, [freq[-1] + 2 * halfbin_freq]))
        time = np.concatenate((time, [time[-1] + 2 * halfbin_time]))
        # center bin
        time -= halfbin_time
        freq -= halfbin_freq
        # Log scaling for frequency values (y-axis)
        ax.set_yscale('log')
        # Plot times
        zorder = None
        end = len(data) / samp_rate
        #kwargs = {k: v for k, v in (('cmap', 'jet'), ('zorder', zorder))
        #        if v is not None}
        #print kwargs
        #from matplotlib.ticker import LogLocator        
        pcm = ax.pcolormesh(time, freq, specgram, norm=norm)
        #cb = fig.colorbar(pcm, ticks = LogLocator())
        #cb.ax.minorticks_on()        
        ax.axis('tight')
        ax.set_xlim(0, end)
        ax.grid(False)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Frequency [Hz]')
        plt.savefig('huge.png')   
    #
    
def plot_spectrogram_():
    from matplotlib import mlab
    from matplotlib.colors import Normalize
    import matplotlib.pyplot as plt
    data = ey1.x.timeseries
    samp_rate = ex1.x._fs
    nfft = ex1.x._nlen/ave
    specgram, freq, time = mlab.specgram(data,Fs=samp_rate,NFFT=nfft,)
    specgram = np.sqrt(specgram)
    #
    clip=[1e-10, 1e-2]
    _range = float(specgram.max() - specgram.min())
    vmin, vmax = clip
    vmin = specgram.min() + vmin * _range
    vmax = specgram.min() + vmax * _range
    norm = Normalize(vmin, vmax, clip=True)
    #
    fig = plt.figure()
    ax = fig.add_subplot(111)        
    ax.set_yscale('log')
    pcm = ax.pcolormesh(time, freq, specgram, norm=norm)
    print specgram
    ax.axis('tight')
    ax.grid(False)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Frequency [Hz]')
    plt.savefig('huge.png')       
    
    
if __name__ == '__main__':
    #main() # backup
    #exit()
    t0,tlen,title = get_gpstime(EQ_name)
    theta = 0
    ave = 16
    ex1 = Seismometer(t0,tlen,'EX1',theta=theta)
    ey1 = Seismometer(t0,tlen,'EY1',theta=theta)
    cen = Seismometer(t0,tlen,'IY0',theta=theta)
    # Yend-Xend
    ex1.x.get_coherence(ex1.y,ave=ave,plot=False)
    print ex1.x.psd.max()
    print ex1.x.psd.min()
    fname = '{0}/Coherence_{1:03d}_Xend_xy'.format(title,theta)
    mpplot.CoherencePlot(ex1.x,fname,ave=ave,cl=99)
    #
    from spectrogram import spectrogram
    data = ex1.x.timeseries
    samp_rate = ex1.x._fs
    print data
    print samp_rate
    spectrogram(data, samp_rate, per_lap=0.9, wlen=None, log=True,
                outfile=None, fmt=None, axes=None, dbscale=False,
                mult=8.0, zorder=None, title=None,
                show=True, sphinx=False, clip=[1e-10, 1e-2])
    #
    exit()
    # 有意なところだけ抜きだす。
    clfunc = lambda a: 1.0-(1.0-a/100.0)**(1./(ave-1))
    idx = np.where(ey1.x._coh>clfunc(99))
    phase = np.rad2deg(ey1.x._cohphase[idx])
    f = ey1.x._f[idx]
    idx = np.where(f>1.0)
    f = f[idx]
    phase = phase[idx]
    idx = np.where(f<2.0)
    f = f[idx]
    phase = phase[idx] #+ 180
