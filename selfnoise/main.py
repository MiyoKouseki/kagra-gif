#
#! coding:utf-8
import sys
sys.path.insert(0,'/Users/miyo/Dropbox/Git/gwpy/')
import gwpy
#print gwpy.__file__

from gwpy.frequencyseries import FrequencySeries

from gwpy.timeseries import TimeSeries
from gwpy.spectrogram import Spectrogram

from gwpy.time import tconvert
from gwpy.plot import Plot

from _file import (get_timeseries,get_specgram,get_csd_specgram,
                   to_gwffname,to_pngfname,to_hdf5fname)

from _plot import (plot_asd,plot_coherence,plot_spectrogram)                



if __name__ == '__main__':
    fmt = 'K1:PEM-{seismometer}_{dof}_SENSINF_IN1_DQ'
    
    start = tconvert('Nov 12 3:0:0') # work finish at 12:00 JST
    # Lack of Data!! 2018-11-12T12:48:14  --- 2018-11-12T12:50:54
    #start = tconvert('Nov 12 14:30:0') # after daq restart
    #start = tconvert('Nov 13 00:30:0') # after lack of data
    start = tconvert('Dec 6 12:00:00 JST') #
    #end = tconvert('Nov 14 0:0:0') #
    fftlength = 2**8
    end = start + fftlength*256
    
    chname1 = 'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ'
    chname2 = 'K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ'
    chname3 = 'K1:PEM-EXV_GND_TR120Q_X_OUT_DQ'
    
    kwargs = {}
    kwargs['start'] = start
    kwargs['end'] = end
    kwargs['nds'] = True
    
    #timeseries1 = get_timeseries(chname1,remake=True,fftlength=fftlength,**kwargs)
    #timeseries2 = get_timeseries(chname2,remake=True,fftlength=fftlength,**kwargs)
    psd_specgram1 = get_specgram(chname1,remake=False,fftlength=fftlength,**kwargs)
    psd_specgram2 = get_specgram(chname2,remake=False,fftlength=fftlength,**kwargs)
    psd_specgram3 = get_specgram(chname3,remake=False,fftlength=fftlength,**kwargs)
    csd_specgram12 = get_csd_specgram(chname1,chname2,remake=False,
                                    fftlength=fftlength,**kwargs)
    csd_specgram13 = get_csd_specgram(chname1,chname3,remake=False,
                                    fftlength=fftlength,**kwargs)
    psd1 = psd_specgram1.mean(axis=0)
    psd2 = psd_specgram2.mean(axis=0)
    psd3 = psd_specgram3.mean(axis=0)
    csd_mag12 = csd_specgram12.mean(axis=0).abs()
    csd_mag13 = csd_specgram13.mean(axis=0).abs()
    coh12 = csd_mag12/psd1**(1/2.0)/psd2**(1/2.)
    angle12 = csd_specgram12.mean(axis=0).angle().rad2deg()    
    coh13 = csd_mag13/psd1**(1/2.0)/psd3**(1/2.)
    angle13 = csd_specgram13.mean(axis=0).angle().rad2deg()
    #
    #print psd_specgram1
    median1 = psd_specgram1.percentile(50)**(1/2.)
    low1 = psd_specgram1.percentile(5)**(1/2.)
    high1 = psd_specgram1.percentile(95)**(1/2.)    
    median2 = psd_specgram2.percentile(50)**(1/2.)
    noise_median = median1*(1.0-coh12)
    noise_low = low1*(1.0-coh12)
    noise_high = high1*(1.0-coh12)
    from miyopy.utils import trillium    
    from _calibration import vel2vel
    _f, _selfnoise = trillium.selfnoise(trillium='120QA',psd='ASD',unit='velo')    
    _selfnoise = _selfnoise*1e6

    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 3e2), xlabel='Frequency [Hz]',
                  #yscale='log', ylim=(1e-11, 3e-6),
                  yscale='log', ylim=(1e-5, 3e-0),
                  ylabel=r'Velocity [m/sec/\rtHz]')
    ax.plot(_f,_selfnoise,'-',linewidth=1,color='gray')
    #ax.plot_mmm(median1, low1, high1, color='gwpy:ligo-livingston')
    median1=vel2vel(median1)
    median2=vel2vel(median2)
    noise_median=vel2vel(noise_median)
    noise_low=vel2vel(noise_low)
    noise_high=vel2vel(noise_high)
    ax.plot(median1)
    ax.plot(median2)
    ax.plot_mmm(noise_median, noise_low, noise_high, color='gwpy:ligo-livingston')    
    #ax.plot(noise)
    ax.set_xscale('log')    
    ax.legend(labels=['Selfnoise','Measurement'])
    pngfname = 'ASD.png'
    plot.savefig(pngfname)
    print 'plot in ASD.png'

    # plot coherence
    import matplotlib.pyplot as plt
    plot, (ax_mag,ax_angle) = plt.subplots(nrows=2, sharex=True, figsize=(8, 6))
    ax_mag.plot(coh13)
    ax_mag.plot(coh12)
    ax_mag.set_ylim(0,1)
    ax_mag.set_xscale('log')
    ax_mag.set_ylabel('Coherence')
    ax_angle.plot(angle13)    
    ax_angle.plot(angle12)
    ax_angle.set_ylim(-181,181)
    ax_angle.set_yticks(range(-180,181,90))    
    ax_angle.set_xscale('log')
    ax_angle.set_ylabel('Phase [deg]')
    ax_angle.set_xlabel('Frequency [Hz]')
    plot.savefig('Coherence.png')
    print 'plot in coherence.png'    
    #
    

    #exit()
    
    
    plot_asd(psd_specgram1,replot=True,**kwargs)
    plot_asd(psd_specgram2,replot=True,plot=plot,**kwargs)
    plot_spectrogram(psd_specgram1,replot=True,**kwargs)
    plot_spectrogram(psd_specgram2,replot=True,**kwargs)
    #plot_spectrogram(coherence_mag_specgram,replot=True,normlog=False,**kwargs)
    #plot_coherence(csd_specgram,specgram1,specgram2,fftlength=fftlength,**kwargs)
    

    
    #coherence2_mag_specgram = csd_specgram.abs()#**2.0/specgram1/specgram2
    #coherence2_angle_specgram = csd_specgram.angle()
    #coherence_mag_specgram = coherence2_mag_specgram#**(1/2.0)
    #print coherence_mag_specgram#.mean(axis=0)

    #coherencegram  = timeseries1.coherence_spectrogram(timeseries2,
    #                                                   stride=fftlength*2.0,
    #                                                   fftlength=fftlength,
    #                                                   overlap=0)
    #coherence_mag_specgram = coherencegram    
    #print coherence_mag_specgram
    
