
import numpy
from miyopy.gif import findfiles
from gwpy.timeseries import TimeSeries
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert
from gwpy.plot import Plot

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__=='__main__':
    start = tconvert('Apr 23 2019 00:00:00 JST') # Before Replacement (b)
    end = tconvert('Apr 23 2019 00:01:00 JST') # Before replacement (b) 
    #start = tconvert('Apr 24 2019 00:00:00 JST') # After Replacement (a)
    #end = tconvert('Apr 24 2019 00:01:00 JST') # After replacement (a)
    chname = 'X500_PD_PPOL_50k'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/KagraData/gif')
    source = [path for files in segments for path in files]    
    ppol = TimeSeries.read(source=source,
                           name=chname,
                           format='gif',
                           pad=numpy.nan,
                               nproc=1)
    ppol =  ppol.crop(ppol.t0.value,ppol.t0.value+32)

    chname = 'X500_PD_SPOL_50k'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/KagraData/gif')
    source = [path for files in segments for path in files]    
    spol = TimeSeries.read(source=source,
                           name=chname,
                           format='gif',
                           pad=numpy.nan,
                               nproc=1)
    spol =  spol.crop(spol.t0.value,spol.t0.value+32)
    
    print ppol.shape
    print ppol
    #plot = Plot()
    #ax = plot.gca()
    #ax.set_title('P-polarization')
    #ax.plot(spol,ppol)
    #plot.savefig('hoge.png')
    #exit()
    if False:
        sg = ppol.spectrogram2(fftlength=1, overlap=0.5, window='hanning') ** (1/2.)
        p_median = sg.percentile(50)
        p_low = sg.percentile(5)
        p_high = sg.percentile(95)        
        p_median.write('p_b_median.hdf5','hdf5')
        p_low.write('p_b_low.hdf5','hdf5')
        p_high.write('p_b_high.hdf5','hdf5')    
    if False:
        sg = spol.spectrogram2(fftlength=1, overlap=0.5, window='hanning') ** (1/2.)
        s_median = sg.percentile(50)
        s_low = sg.percentile(5)
        s_high = sg.percentile(95)        
        s_median.write('s_b_median.hdf5','hdf5')
        s_low.write('s_b_low.hdf5','hdf5')
        s_high.write('s_b_high.hdf5','hdf5')
    #exit()
    a_median = FrequencySeries.read('s_a_median.hdf5','hdf5')
    a_low = FrequencySeries.read('s_a_low.hdf5','hdf5')
    a_high = FrequencySeries.read('s_a_high.hdf5','hdf5')
    b_median = FrequencySeries.read('s_b_median.hdf5','hdf5')
    b_low = FrequencySeries.read('s_b_low.hdf5','hdf5')
    b_high = FrequencySeries.read('s_b_high.hdf5','hdf5')
    
    plot = Plot()
    ax = plot.gca(xscale='log', #xlim=(10, 1500),
                  xlabel='Frequency [Hz]',
                  yscale='log', ylim=(1e-6, 1e-3),
                  ylabel=r'Voltage [V/$\sqrt{\mathrm{Hz}}$]')
    ax.plot(b_median)    
    ax.plot(a_median,alpha=0.7)
    #ax.plot_mmm(a_median, a_low, a_high, color='gwpy:ligo-hanford')
    #ax.plot_mmm(b_median, b_low, b_high, color='gwpy:ligo-livingston')
    ax.set_title('S-polarization',fontsize=16)
    ax.legend(['Before','After'])
    plot.savefig('huge.png')
