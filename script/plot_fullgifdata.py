
import numpy
from miyopy.gif import findfiles
from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert


''' GIFのデータからPDの信号を取り出してプロットするスクリプト

'''

if __name__=='__main__':
    start = tconvert('Feb 25 2019 15:00:00') # UTC
    end = tconvert('Feb 25 2019 15:01:00') # UTC
    
    # Read
    chname = 'X500_PD_PPOL_50k'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/Dropbox/KagraData/gif')
    source = [path for files in segments for path in files]
    ppol = TimeSeries.read(source=source, name=chname, format='gif', pad=numpy.nan, nproc=2)
    chname = 'X500_PD_SPOL_50k'    
    segments = findfiles(start,end,chname,prefix='/Users/miyo/Dropbox/KagraData/gif')
    source = [path for files in segments for path in files]
    spol = TimeSeries.read(source=source, name=chname, format='gif', pad=numpy.nan, nproc=2)
    
    # Crop
    ppol = ppol.crop(ppol.t0.value,ppol.t0.value+32)
    spol = spol.crop(spol.t0.value,spol.t0.value+32)
    if False:
        plot = ppol.plot()
        plot.savefig('hoge.png')
    
    # Calc Spectrum with percentile
    pdp = ppol.spectrogram2(fftlength=2, overlap=1, window='hanning') ** (1/2.)
    pdp_m = pdp.percentile(50)
    pdp_l = pdp.percentile(5)
    pdp_h = pdp.percentile(95)
    pds = spol.spectrogram2(fftlength=2, overlap=1, window='hanning') ** (1/2.)
    pds_m = pds.percentile(50)
    pds_l = pds.percentile(5)
    pds_h = pds.percentile(95)
    
    # Plot asd graph
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1, 50000), xlabel='Frequency [Hz]',
                  yscale='log', #ylim=(3e-24, 2e-20),
                  ylabel=r'Voltage [V/\rtHz]')
    ax.plot_mmm(pdp_m, pdp_l, pdp_h, color='gwpy:ligo-hanford',label='P-polarized signal')
    ax.plot_mmm(pds_m, pds_l, pds_h, color='gwpy:ligo-livingston',label='S-polarized signal')
    ax.set_title('PD voltage', fontsize=16)
    ax.legend()
    plot.savefig('asd.png')
