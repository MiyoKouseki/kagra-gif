#
#! coding:utf-8
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
#from miyopy.utils.tips import read
from miyopy.io import read 
from miyopy.signal import coherence,asd
from miyopy.plot import coherenceplot,asdplot
#import matplotlib.pyplot as plt
from miyopy.utils.trillium import H120QA,TRselfnoise
import sys
#sys.path.insert(0,'~/gwpy')
#import gwpy
#print(gwpy.__version__)
from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert
from gwpy.plot import Plot

import glue
#print(glue.__file__)

c2V = 10.0/2**15
deGain = 10**(-30.0/20.0)

__dumped_gwf_fmt = './data/{start}_{tlen}_{chname}.gwf'
dumped_gwf_fmt = './data/{start}_{end}_{chname}.gwf'

channels = ['K1:PEM-IXV_SEIS_NS_SENSINF_INMON.mean',
            'K1:PEM-IXV_SEIS_WE_SENSINF_INMON.mean',
            'K1:PEM-IXV_SEIS_Z_SENSINF_INMON.mean',
            'K1:PEM-EXV_SEIS_NS_SENSINF_INMON.mean',
            'K1:PEM-EXV_SEIS_WE_SENSINF_INMON.mean',
            'K1:PEM-EXV_SEIS_Z_SENSINF_INMON.mean',
            'K1:PEM-EYV_SEIS_NS_SENSINF_INMON.mean',
            'K1:PEM-EYV_SEIS_WE_SENSINF_INMON.mean',
            'K1:PEM-EYV_SEIS_Z_SENSINF_INMON.mean',
            'K1:PEM-IXV_SEIS_TEST_NS_SENSINF_INMON.mean',
            'K1:PEM-IXV_SEIS_TEST_WE_SENSINF_INMON.mean',
            'K1:PEM-IXV_SEIS_TEST_Z_SENSINF_INMON.mean']


def coh2snr(coh):
    '''
    
    '''
    _coh2snr = lambda x:  abs(x)/(1.0-abs(x))
    snr = [_coh2snr(_coh) for _coh in coh]
    return np.array(snr)



def sensor_noise(coh12,coh13,asd1,asd2,asd3):
    ''' Estimate the noise level of sensor using Peterson-Method(1980).
    
            
    Parameters
    ----------
    coh12 : numpy.array 
        The coherence between "adjacent two sensors" so that the 
        external noise from local environment is same each other.
    coh13 : numpy.array
        The coherence between "well-separate two sensors" so that the
        external noise from local environment dont have correlation
        earch other.        
    asd1 : numpy.array
       Amplitude spectrum density of the sensor1.
    asd2 : numpy.array
       Amplitude spectrum density of the sensor2.
    asd3 : numpy.array
       Amplitude spectrum density of the sensor3.
    
    Returns
    -------
    asd_x : numpy.array
        The noise existing globally with coherently. This noise could
        be called "signal", because this noise have coherent globally.
    asd_n : numpy.array
        The noise existing globally with incoherently. This noise could 
        be called "self-noise", because this incoherenct noise dont 
        disappear even separated well.
    asd_xb : numpy.array
        The noise existing locally with coherently. This noise is a 
        sum of the signal and local environmental noise.
    '''
    coh13 = np.sqrt(coh13)
    coh12 = np.sqrt(coh12)
    snr13 = coh2snr(coh13)
    snr12 = coh2snr(coh12)
    n12 = asd1*np.sqrt(1.0/(1+snr12))
    s12 = asd1*np.sqrt(1.0/(1+snr12)*snr12)
    s13 = np.sqrt(asd1*asd3*coh13)
    envnoise = s12 - s13
    asd_n = n12
    asd_x = s13
    asd_xb = s12
    return asd_x,asd_n,asd_xb




def huge(t1,t2,t3,start,end,fs,ave=32):
    t1_we,t1_ns,t1_zz = t1
    t2_we,t2_ns,t2_zz = t2
    t3_we,t3_ns,t3_zz = t3
    f_, asd1_we = asd(t1_we,fs,ave=ave)
    f_, asd2_we = asd(t2_we,fs,ave=ave)
    f_, asd3_we = asd(t3_we,fs,ave=ave)    
    asd1_we = asd1_we/H120QA(f_)
    asd2_we = asd2_we/H120QA(f_)
    asd3_we = asd3_we/H120QA(f_)    
    asdplot([[f_,asd1_we],[f_,asd2_we],[f_,asd3_we]],
            legend=['1_we','2_we','3_we'],
            fname='asd')

    
def plot_asd_all(t1,t2,t3,start,end,fs,ave=32):
    #
    t1_we,t1_ns,t1_zz = t1
    t2_we,t2_ns,t2_zz = t2
    t3_we,t3_ns,t3_zz = t3
    f_, asd1_we = asd(t1_we,fs,ave=ave)
    f_, asd2_we = asd(t2_we,fs,ave=ave)
    f_, asd3_we = asd(t3_we,fs,ave=ave)    
    asd1_we = asd1_we/H120QA(f_)
    asd2_we = asd2_we/H120QA(f_)
    asd3_we = asd3_we/H120QA(f_)
    f, coh13_wewe, deg13_wewe = coherence(t1_we,t3_we,fs,ave=ave)
    f, coh12_wewe, deg12_wewe = coherence(t1_we,t2_we,fs,ave=ave)
    #
    asd_x,asd_n,asd_xb = sensor_noise(coh12_wewe,coh13_wewe,asd1_we,asd2_we,asd3_we)
    #
    snr13_wewe = coh2snr(coh13_wewe)
    snr12_wewe = coh2snr(coh12_wewe)
    asdplot([[f_,snr12_wewe],[f_,snr13_wewe]],
            legend=['1_we','2_we'],
            fname='snr')
    #
    f,_selfnoise = TRselfnoise(acc='velo')    
    asdplot([[f,_selfnoise],[f_,asd_x],[f_,asd_n],[f_,asd_xb]],
            legend=['Self-Noise',
                    '1_we',
                    'x : Coherent Signal b/w 1 and 3 (Global Noise)',
                    'n : Incoherent Signal b/w 1 and 2 (Internal Instrument Noise)',
                    'x+b : Coherent Signal b/w 1 and 2 (Local Noise)',       
                    ],
            linestyle=[':o','-','-','-'],
            ylim=[1e-11,5e-6],
            xlim=[min(f_[1:]),200],
            fname='selfnoise')    

   
def dump(chname,start,tlen):    
    end = start + tlen
    from glue.lal import Cache
    from gwpy.timeseries import TimeSeries

    gwf_cache = 'K-K1_C.Oct1-Oct21.cache'
    gwf_cache = 'trend_Oct1-Oct21.cache'
    gwf_cache = 'trend_Sep1-Oct21.cache'
    with open(gwf_cache, 'r') as fobj:
        cache = Cache.fromfile(fobj)
    #print cache
    #cache = '/data//trend/minute/12228/K-K1_M-1222801200-3600.gwf'    
    data = TimeSeries.read(cache,chname,verbose=True,nproc=8,pad=np.nan)
    data.write('{start}_{tlen}_{ch}.gwf'.format(ch=chname,start=start,tlen=tlen)
               ,format='gwf.lalframe')



def main_dump(start,end):
    for channel in channels:
        dump(channel,start,tlen)
    exit()



def main(channel,start,end):

    data = TimeSeries.read(
        dumped_gwf_fmt.format(start=start,end=end,chname=channel),
        channel, verbose=True ,nproc=8)
    
    timeseriesplot_fname_fmt = 'TimeSeries_{channel}.png'
    spectrogramplot_fname_fmt = 'Spectrogram_{channel}.png'
    asdplot_fname_fmt = 'ASD_{channel}.png'

    # Filtering
    from gwpy.signal import filter_design
    bp_high = filter_design.highpass(0.3, data.sample_rate)
    bp_mid = filter_design.bandpass(0.05, 0.3, data.sample_rate)
    bp_low = filter_design.lowpass(0.05, data.sample_rate)

    data_high = data.filter(bp_high, filtfilt=True)
    data_high = data_high.crop(*data_high.span.contract(1))
    data_mid = data.filter(bp_mid, filtfilt=True)
    data_mid = data_mid.crop(*data_mid.span.contract(1))
    data_low = data.filter(bp_low, filtfilt=True)
    data_low = data_low.crop(*data_low.span.contract(1))

    
    # Plot TimeSeries
    title = channel[3:].replace('_',' ')
    labels = ['No filt', 'High (300mHz-)', 'Mid (50mHz-300mHz)', 'Low (-50mHz)']
    if data.unit == ' ':
        yaxis_label = 'Count'
    else:
        yaxis_label = data.unit

    from gwpy.plot import Plot    
    data_set = [data,data_high, data_mid, data_low]
    plot = Plot(*data_set,
                separate=True, sharex=True, sharey=True,
                color='gwpy:ligo-livingston',
                figsize=[10,10])
    
    axes = plot.get_axes()
    for i,ax in enumerate(axes):
        ax.legend([labels[i]],loc='upper left')

    plot.text(0.04, 0.5, yaxis_label, va='center', rotation='vertical',fontsize=16)
    #plot.text(0.5, 0.93, title, va='center',ha='center',rotation='horizontal',fontsize=16)
    axes[0].set_title(title,fontsize=16)
    axes[-1].set_xscale('Hours', epoch=start)
    plot.savefig(timeseriesplot_fname_fmt.format(channel=channel))
    plot.close()


    # Plot ASD
    fftlen = 2**7
    specgram = data.spectrogram2(fftlength=fftlen, 
                                 overlap=2, 
                                 window='hanning') ** (1/2.)
    median = specgram.percentile(50)
    low = specgram.percentile(5)
    high = specgram.percentile(95)
    plot = Plot()
    ylabel_fmt = r'{yaxis_label} [{yaxis_label}/\rtHz]'
    ax = plot.gca(xscale='log', xlim=(1e-3, 10), 
                  xlabel='Frequency [Hz]',
                  yscale='log', #ylim=(3e-24, 2e-20),
                  ylabel=ylabel_fmt.format(yaxis_label=yaxis_label))
    ax.plot_mmm(median, low, high, color='gwpy:ligo-livingston')
    ax.set_title(title,fontsize=16)
    plot.savefig(asdplot_fname_fmt.format(channel=channel))
    plot.close()

    # Plot Spectrogram
    specgram = data.spectrogram(fftlen*2, fftlength=fftlen, overlap=.5) ** (1/2.)
    plot = specgram.imshow(norm='log')
    ax = plot.gca()
    ax.set_yscale('log')
    ax.set_ylim(1e-3, 10)
    ax.set_title(title,fontsize=16)
    ax.colorbar(label=ylabel_fmt.format(yaxis_label=yaxis_label))
    plot.savefig(spectrogramplot_fname_fmt.format(channel=channel))


if __name__ == "__main__":
    tlen = 2**16
    #start = 1222354818 # UTC 2018-09-30T15:00:00
    if False:
        start, end = 'Sep30 15:00:00', 'Oct20 15:00:00'
    if True:
        start,end = 'Sep30 15:00:00', 'Oct01 09:12:16'

    start = tconvert(start)
    end = tconvert(end)
    channel = 'K1:PEM-IXV_SEIS_NS_SENSINF_INMON'    
    
    # --------------------
    # 
    #main_dump(start,tlen)

    # --------------------
    #
    main(channel,start,end)
    
    
