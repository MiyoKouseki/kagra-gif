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
    chname2 = 'K1:PEM-IXV_SEIS_TEST_NS_SENSINF_IN1_DQ'
    
    kwargs = {}
    kwargs['start'] = start
    kwargs['end'] = end

    timeseries1 = get_timeseries(chname1,remake=True,fftlength=2**7,**kwargs)
    timeseries2 = get_timeseries(chname2,remake=True,fftlength=2**7,**kwargs)
    
    psd_specgram1 = get_specgram(chname1,remake=True,fftlength=2**7,**kwargs)
    psd_specgram2 = get_specgram(chname2,remake=True,fftlength=2**7,**kwargs)
    csd_specgram = get_csd_specgram(chname1,chname2,remake=True,
                                    fftlength=2**6,**kwargs)

    # calc scipy
    fs = 1./timeseries1.dt
    fs = fs.value
    x = timeseries1.value
    y = timeseries2.value
    nperseg = int(fftlength*fs)
    f, csd = signal.csd(x,y,fs,nperseg=nperseg,noverlap=0)
    f, psd1 = signal.welch(x,fs,nperseg=nperseg,noverlap=0)
    f, psd2 = signal.welch(y,fs,nperseg=nperseg,noverlap=0)
    mag_scipy = (np.abs(csd)**2.0/psd1/psd2)**(1/2.)
    angle_scipy = np.angle(csd)
    angle_scipy = np.rad2deg(angle_scipy)

    # calc gwpy    
    csd_specgram = timeseries1.csd_spectrogram(timeseries2,
                                               stride=fftlength,
                                               fftlength=fftlength,
                                               overlap=0,
                                               window='hanning',
                                               nproc=2)

    angle_gwpy = csd_specgram.mean(axis=0).angle().rad2deg()
    psd_specgram1 = psd_specgram1.mean(axis=0)
    psd_specgram2 = psd_specgram2.mean(axis=0)    
    csd_mag = csd_specgram.mean(axis=0).abs()
    mag_gwpy = csd_mag/psd_specgram1**(1/2.0)/psd_specgram2**(1/2.)
    

    plot, (ax0,ax1) = plt.subplots(nrows=2, sharex=True, figsize=(8, 6))
    ax0.plot(mag_gwpy,label='gwpy')
    ax0.plot(f,mag_scipy,label='scipy')
    ax0.legend()
    ax0.set_ylim(0,1)
    ax0.set_xscale('log')
    ax0.set_xlabel('Frequency [Hz]')
    ax1.plot(angle_gwpy)
    ax1.plot(f,angle_scipy)
    ax1.set_xscale('log')    
    plot.savefig('Test_Coherence.png')
    print '--- Result ---'
    result = {True:'passed!', False:'not passed..'}    
    magtest = np.all(np.isclose(mag_gwpy.value,mag_scipy))
    angtest = np.all(np.isclose(angle_gwpy.value,angle_scipy))
    print 'Magnitude Matching : ', magtest
    print 'Angle Matching     : ', angtest
    print 'Matching result is : ', result[magtest and angtest]
