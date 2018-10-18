#
#! coding:utf-8
import sys
sys.path.insert(0,'/Users/miyo/Dropbox/Git/gwpy/')
sys.path.insert(0,'/Users/miyo/Dropbox/Git/miyopy/')

from numpy import (array)
from gwpy.timeseries import TimeSeries
import gwpy

from miyopy.gif import (GifData)

if __name__=='__main__':
    prefix = '/Users/miyo/Dropbox/KagraData/gif/data1/PHASE/50000Hz/2018/10/14/00/'

    start = 1223478018
    start = 1222441218
    start = 1222786818 # 10/06 00:00:00 JST
    tlen = 3600*24*3
    chname = 'CALC_STRAIN'
    files = GifData.findfiles(start,tlen,chname,
                              prefix='/Users/miyo/Dropbox/KagraData/gif/')
    print('Found files')
    
    strain = TimeSeries.read(source=files,
                             name='CALC_STRAIN',
                             format='gif',
                             nproc=2)
    
    # plot timeseries
    plot = strain.plot(title='GIF strain data',
                       ylabel='Strain amplitude',
                       )
    plot.savefig('timeseries.png')
    plot.close()
    print('plot timeseries.png')
    
    # plot spectrogram
    stride = 2**12 # sec
    fftlength = 2**11 # sec
    spectrogram = strain.spectrogram(stride=stride, fftlength=fftlength) ** (1/2.)
    plot = spectrogram.imshow(norm='log', vmin=5e-12, vmax=1e-10)
    ax = plot.gca()
    ax.set_yscale('log')
    ax.set_ylim(1e-3, 10)
    ax.colorbar(
        label=r'GIF strain amplitude [strain/$\sqrt{\mathrm{Hz}}$]')
    plot.subplots_adjust(right=.86)
    plot.savefig('spectrogram.png')
    plot.close()
    print('plot spectrogram.png')
    
    # plot asd
    fftlength = 2**11
    overlap = 2
    sg = strain.spectrogram2(fftlength=fftlength,
                             overlap=overlap, window='hanning') ** (1/2.)
    median = sg.percentile(50)
    low = sg.percentile(5)
    high = sg.percentile(95)
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
