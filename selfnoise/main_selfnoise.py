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
    from gwpy.plot import BodePlot
    import numpy
    bp_high = filter_design.highpass(0.3, data.sample_rate, analog=True,
                                     ftype='butter',
                                     gpass=2,gstop=30#,fstop()
    )
    bp_mid = filter_design.bandpass(0.05, 0.3, data.sample_rate, analog=True,
                                    ftype='butter',
                                    gpass=2, gstop=30#,fstop=(0.01,0.5)
    )
    bp_low = filter_design.lowpass(0.05, data.sample_rate,analog=True, 
                                   ftype='butter',
                                   gpass=2, gstop=30#, fstop=2
    )
    filters = [bp_high,bp_mid,bp_low]

    plot = BodePlot(*filters, analog=True,
                    frequencies=numpy.logspace(-3,1,1e5),
                    dB=False,unwrap=False,
                    title='filter')
    axes = plot.get_axes()
    axes[0].set_yscale('log')
    axes[0].set_ylim(1e-4,2e0)
    axes[-1].set_xlim(1e-2,1e0)
    axes[-1].set_ylim(-180,180)
    plot.savefig('Bodeplot_BandPass.png')
    plot.close()

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
    
    
