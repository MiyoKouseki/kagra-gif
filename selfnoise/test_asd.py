import sys
sys.path.insert(0,'/Users/miyo/Dropbox/Git/gwpy/')
import gwpy
print gwpy.__file__

from gwpy.frequencyseries import FrequencySeries

from gwpy.timeseries import TimeSeries
from gwpy.spectrogram import Spectrogram

from gwpy.time import tconvert
from gwpy.plot import Plot

from _file import (get_timeseries,get_specgram,get_csd_specgram,
                   to_gwffname,to_pngfname,to_hdf5fname)

from _plot import (plot_asd,plot_coherence,plot_spectrogram)                
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

if __name__ == '__main__':
    
    start = tconvert('Nov 13 01:00:0') 
    fftlength = 2**7
    end = start + fftlength*2**4
    
    chname1 = 'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ'
    chname2 = 'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ'
    
    kwargs = {}
    kwargs['start'] = start
    kwargs['end'] = end

    timeseries1 = get_timeseries(chname1,remake=True,fftlength=2**6,**kwargs)
    timeseries2 = get_timeseries(chname2,remake=True,fftlength=2**6,**kwargs)
    
    # calc scipy
    fs = 1./timeseries1.dt
    fs = fs.value
    fs = timeseries1.sample_rate.decompose().value
    x = timeseries1.value
    nperseg = int(fftlength*fs)
    f, asd_scipy = signal.welch(x,fs,nperseg=nperseg,noverlap=0)
    mag_scipy = asd_scipy ** (1.0/2.)
    
    # calc gwpy
    asd_specgram = timeseries1.spectrogram(stride=fftlength,
                                           fftlength=fftlength,
                                           overlap=0,
                                           method='scipy-welch',
                                           window='hanning') 
    mag_gwpy = asd_specgram.mean(axis=0)** (1/2.)#.abs()
    plot, (ax0,ax1) = plt.subplots(nrows=2, sharex=True, figsize=(8, 6))
    ax0.plot(mag_gwpy,label='gwpy')
    ax0.plot(f,mag_scipy,label='scipy')
    ax0.legend()
    ax0.set_ylim(1e-2,1e2)
    ax0.set_yscale('log')
    ax0.set_xscale('log')
    ax0.set_ylabel('Frequency [Hz]')
    plot.savefig('Test_ASD.png')
    print '--- Result ---'
    result = {True:'passed!', False:'not passed..'}    
    magtest = np.all(np.isclose(mag_gwpy.value,mag_scipy))
    print 'Magnitude Matching : ', magtest
    print 'Matching result is : ', result[magtest]
