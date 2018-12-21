#
#! coding:utf-8

import matplotlib.pyplot as plt
import numpy as np

from gwpy.frequencyseries import FrequencySeries
from gwpy.timeseries import TimeSeries
from gwpy.spectrogram import Spectrogram

from gwpy.time import tconvert
from gwpy.plot import Plot

from _file import (get_timeseries,get_specgram,get_csd_specgram,
                   to_gwffname,to_pngfname,to_hdf5fname,
                   get_asd,get_csd,get_coherence)

from _plot import (plot_asd,plot_coherence,plot_spectrogram)

from miyopy.utils import trillium    
from _calibration import vel2vel


if __name__ == '__main__':    
    start = tconvert('Dec 6 12:00:00 JST')
    fftlength = 2**9
    ave = 256
    overlap = 0.5
    end = start + fftlength*(ave*(1.0-overlap))
    
    kwargs = {}
    kwargs['start'] = start
    kwargs['end'] = end
    kwargs['nds'] = True
    kwargs['overlap'] = fftlength*overlap
    kwargs['remake'] = True
    kwargs['fftlength'] = fftlength
    kwargs['nproc'] = 2    

    # get data
    chname1 = 'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ'
    chname2 = 'K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ'
    chname3 = 'K1:PEM-EXV_GND_TR120Q_X_OUT_DQ'
    # psd_specgram1 = get_specgram(chname1,**kwargs)
    # psd_specgram2 = get_specgram(chname2,**kwargs)
    # psd_specgram3 = get_specgram(chname3,**kwargs)
    # csd_specgram12 = get_specgram(chname1,chname2,**kwargs)
    # csd_specgram13 = get_specgram(chname1,chname3,**kwargs)
    # calc mean
    # psd1 = psd_specgram1.mean(axis=0)
    # psd2 = psd_specgram2.mean(axis=0)
    # psd3 = psd_specgram3.mean(axis=0)
    # csd12 = csd_specgram12.mean(axis=0).abs()
    # csd13 = csd_specgram13.mean(axis=0).abs()
    # angle12 = csd_specgram12.mean(axis=0).angle().rad2deg()        
    # angle13 = csd_specgram13.mean(axis=0).angle().rad2deg()
    
    print('get data')    
    asd1 = get_asd(chname1,**kwargs)
    fseries = asd1
    c2V = 10.0/2**15
    V2vel = 1/1202.5
    adc_noise = np.ones(len(fseries))*1e-2*c2V*V2vel*1e6*10**(-30.0/20.0)
    f0 = fseries.f0
    df = fseries.df   
    adc = FrequencySeries(adc_noise,df=df,f0=f0+df)
    #print adc_noise
    #print asd1
    #exit()
    asd2 = get_asd(chname2,**kwargs)
    asd3 = get_asd(chname3,**kwargs)
    csd12 = get_csd(chname1,chname2,**kwargs)
    csd13 = get_csd(chname1,chname3,**kwargs)    
    coh12 = get_coherence(chname1,chname2,**kwargs)
    coh13 = get_coherence(chname1,chname3,**kwargs)
    angle12 = csd12.angle().rad2deg()
    angle13 = csd13.angle().rad2deg()
    print('calc mean')
    
    # calc median
    # median1 = asd_specgram1.percentile(50)**(1/2.)
    # median2 = asd_specgram2.percentile(50)**(1/2.)        
    # print('calc median')

    # plot coherence
    plot, (ax_mag,ax_angle) = plt.subplots(nrows=2, sharex=True, figsize=(8, 6))
    ax_mag.plot(coh13,'o',label='coh13',markersize=1)
    ax_mag.plot(coh12,'o',label='coh12',markersize=1)
    ax_mag.set_ylim(0,1)
    ax_mag.set_xscale('log')
    ax_mag.set_ylabel('Coherence')
    ax_mag.legend(loc='best')
    ax_angle.plot(angle13,'o',markersize=1)
    ax_angle.plot(angle12,'o',markersize=1)
    ax_angle.set_ylim(-181,181)
    ax_angle.set_yticks(range(-180,181,90))    
    ax_angle.set_xscale('log')
    ax_angle.set_ylabel('Phase [deg]')
    ax_angle.set_xlabel('Frequency [Hz]')
    plot.savefig('Coherence.png')
    print 'plot in coherence.png'    
    
    # calc noise
    noise12 = asd1*(1.0-coh12.value)
    noise13 = asd1*(1.0-coh13.value)
    print('calc asd')

    # calcl signal
    signal12 = asd1*coh12
    signal13 = asd1*coh13
    signal_local = signal12-signal13
    
    # selfnoise
    _f, _selfnoise = trillium.selfnoise(trillium='120QA',psd='ASD',unit='velo')    
    _selfnoise = _selfnoise*1e6
    
    # convert with tf
    asd1 = vel2vel(asd1)
    asd2 = vel2vel(asd2)
    asd3 = vel2vel(asd3)
    adc = vel2vel(adc)
    noise12 = vel2vel(noise12)
    noise13 = vel2vel(noise13)
    signal12 = vel2vel(signal12)
    signal13 = vel2vel(signal13)    
    print('convert with tf')

    # plot psd with noise    
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 3e2), xlabel='Frequency [Hz]',
                  yscale='log', ylim=(1e-5, 3e-0),
                  ylabel=r'Velocity [um/sec/\rtHz]')
    ax.plot(_f,_selfnoise,'-',linewidth=1,color='gray')
    ax.plot(asd1,label='1',color='black',linewidth=3)
    #ax.plot(asd2,label='2',color='red',linewidth=1)
    #ax.plot(asd3,label='3',color='blue',linewidth=1)
    #ax.plot(adc,label='adc',color='green',linewidth=1)
    #ax.plot(noise13,'o',label='Noise13 : IXV*(1-coh13) ',markersize=1)
    #ax.plot(noise12,'o',label='Noise12 : IXV*(1-coh12) ',markersize=1)
    ax.plot(signal13,label='Signal13 : IXV*coh13 ',markersize=1)
    ax.plot(signal12,label='Signal12 : IXV*coh12 ',markersize=1)
    #ax.plot(signal_local,label='Local Signal')    
    ax.legend()
    plot.savefig('ASD.png')
    print 'plot in ASD.png'
    exit()
    plot_asd(specgram1,replot=True,**kwargs)
    plot_asd(specgram2,replot=True,**kwargs)
    plot_spectrogram(specgram1,replot=True,**kwargs)
    plot_spectrogram(specgram2,replot=True,**kwargs)
    plot_spectrogram(coherence_mag_specgram,replot=True,normlog=False,**kwargs)
    plot_coherence(csd_specgram,specgram1,specgram2,fftlength=fftlength,**kwargs)    
