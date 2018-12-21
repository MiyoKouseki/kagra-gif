#
#! coding:utf-8
import sys
sys.path.insert(0,'/Users/miyo/Dropbox/Kagra/Git/gwpy/')
sys.path.insert(0,'/Users/miyo/Dropbox/Git/miyopy/')
#import warnings
#warnings.filterwarnings("ignore",category =RuntimeWarning)

import numpy
from numpy import (array)
from gwpy.timeseries import TimeSeries
import gwpy

from miyopy.gif import (GifData)

if __name__=='__main__':
    prefix = '/Users/miyo/Dropbox/KagraData/gif/data1/PHASE/50000Hz/2018/10/14/00/'
    #
    start = 1223478018 # UTC 2018-10-13T15:00:00
    start = 1222441218 # UTC 2018-10-01T15:00:00
    start = 1222009218 # UTC 2018-09-26T15:00:00
    start = 1222095618 # UTC 2018-09-27T15:00:00
    #start = 1219849218 # UTC 2018-09-01T15:00:00
    start = 1222700418 # UTC 2018-10-04T15:00:00
    #start = 1222786818 # 10/06 00:00:00 JST
    tlen = 3600*24#*14
    #tlen = 
    chname = 'CALC_STRAIN'
    segments = GifData.findfiles(start,tlen,chname,
                                 prefix='/Users/miyo/Dropbox/KagraData/gif/')
    #
    allfiles = [path for files in segments for path in files]    
    strain = TimeSeries.read(source=allfiles,
                             name='CALC_STRAIN',
                             format='gif',
                             pad=numpy.nan,
                             nproc=2)
    strain.write('strain_{start}_{end}.csv'.format(start=start,end=start+tlen))
    #exit()
    #
    #
    # 
    #print(strain.t0)
    #print(start)
    #strain = strain.crop(start,start+tlen)
    # 
    # from gwpy.signal.filter_design import bandpass
    # from gwpy.plot import BodePlot
    # zpk = bandpass(1e-3, 1e0, 8, analog=True)
    # plot = BodePlot(zpk, analog=True, title='40-1000\,Hz bandpass filter')
    # #plot.show()
    # #
    # strain = strain.zpk([1e0], [1e-3], 1)
    # plot timeseries
    plot = strain.plot(title='GIF strain data',
                       ylabel='Strain amplitude')
    plot.subplots_adjust(right=.86)
    plot.savefig('timeseries.png')   
    plot.close()
    print('plot timeseries.png')
    #exit()
    # plot spectrogram
    stride = 2**17 # sec
    fftlength = 2**16 # sec
    print()
    spectrogram = strain.spectrogram(stride=stride, fftlength=fftlength) ** (1/2.)
    plot = spectrogram.imshow(norm='log', vmin=5e-12, vmax=1e-8)
    ax = plot.gca()
    ax.set_yscale('log')
    ax.set_ylim(1e-3, 10)
    ax.colorbar(label=r'GIF strain amplitude [strain/$\sqrt{\mathrm{Hz}}$]')
    plot.subplots_adjust(right=.86)
    plot.savefig('spectrogram.png')
    plot.close()
    print('plot spectrogram.png')
    
    # plot asd   
    badtimes = numpy.isnan(spectrogram[:,0])
    goodtimes = numpy.logical_not(badtimes)
    xindex = spectrogram.xindex[goodtimes]
    start, end = xindex[0].value, xindex[-1].value
    gooddata = spectrogram.crop(start,end)
    #        
    #
    median = gooddata.percentile(50)
    low = gooddata.percentile(5)
    high = gooddata.percentile(95)
    
    #
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-7, 10), xlabel='Frequency [Hz]',
                yscale='log', ylim=(5e-14, 1e-5),
                ylabel=r'Strain noise [1/\rtHz]')
    ax.plot_mmm(median, low, high, color='gwpy:ligo-hanford')
    ax.set_title('GIF strain',
                fontsize=16)
    plot.savefig('asd.png')
    plot.close()
    print('plot asd.png')
