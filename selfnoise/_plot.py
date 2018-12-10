import os
import warnings

import matplotlib.pyplot as plt
import numpy as np

from gwpy.frequencyseries import FrequencySeries
from gwpy.timeseries import TimeSeries
from gwpy.spectrogram import Spectrogram
from gwpy.plot import Plot

from miyopy.utils import trillium

from _file import (get_timeseries,get_specgram,get_csd_specgram,
                   to_gwffname,to_pngfname,to_hdf5fname)
from _calibration import count2vel,vel2vel
    
def plot_spectrogram(data,replot=False,fftlength=2**7,show=False,normlog=True,**kwargs):
    if isinstance(data,TimeSeries):
        chname = data.name            
        specgram = data.spectrogram2(fftlength=fftlength,
                                     overlap=fftlength/2.0,
                                     window='hanning')
    elif isinstance(data,Spectrogram):
        chname = data.name
        specgram = data
        
    c2v = 10.0/2**15
    v2vel = 1./1208
    #specgram = psd_specgram*c2v*v2vel #** (1/2.)
    specgram = psd_specgram
    
    pngfname = to_pngfname(chname,ftype='Spectrogram')
    if not replot and os.path.exists(pngfname):
        print('Skip plot {0}'.format(pngfname))
        return None
    
    #plot, ax0 = plt.subplots(nrows=1, sharex=True, figsize=(15, 6))
    plot, (ax0,ax1) = plt.subplots(nrows=2, sharex=True, figsize=(15, 9))    
    if normlog:
        #ax0.imshow(specgram,norm='log', vmin=1e-9, vmax=1e-5, cmap='viridis')
        ax0.imshow(specgram,norm='log', vmin=1e-5, vmax=1e2, cmap='viridis')
    else:
        #ax0.imshow(specgram,norm='log', vmin=1e-2, vmax=1.0, cmap='viridis')
        ax0.imshow(specgram, vmin=0, vmax=1.0, cmap='viridis')
        
    ax0.set_ylim(1e-2, 400)
    ax0.set_yscale('log')
    ax0.set_ylabel('Frequency [Hz]')
    ax0.colorbar(label='ASD [m/sec/$\sqrt{\mathrm{Hz}}$]')
    #ax0.set_xscale('auto-gps')    
    specgram = specgram.ratio('median')
    ax1.imshow(specgram,norm='log', vmin=1e-3, vmax=1e3, cmap='Spectral_r')
    ax1.set_ylim(1e-2, 400)
    ax1.set_ylabel('Frequency [Hz]')    
    ax1.set_yscale('log')
    ax1.set_xscale('auto-gps')    
    plt.setp(ax0.get_xticklabels(),visible=False)    
    ax1.colorbar(label='Relative ASD [m/sev/$\sqrt{\mathrm{Hz}}$]')
    if not chname:
        plt.suptitle('None')
    else:
        plt.suptitle(chname.replace('_',' '),fontsize=30)
    plot.savefig(pngfname)
    print 'plot in ', pngfname
    #return plot
    
    
def plot_asd(data,replot=False,fftlength=2**7,show=False,**kwargs):
    if isinstance(data,TimeSeries):
        chname = data.name            
        psd_specgram = data.spectrogram2(fftlength=fftlength,
                                     overlap=fftlength/2.0,
                                     window='hanning')
        
    elif isinstance(data,Spectrogram):
        chname = data.name
        specgram = data

        
    pngfname = to_pngfname(chname,ftype='ASD')
    if not replot and os.path.exists(pngfname):
        print('Skip plot {0}'.format(pngfname))
        return None
    
    median = specgram.percentile(50)
    low = specgram.percentile(5)
    high = specgram.percentile(95)
    
    median = vel2vel(median)
    low = vel2vel(low)
    high = vel2vel(high)
    
    _f, _selfnoise = trillium.selfnoise(trillium='120QA',psd='ASD',unit='velo')    
    _selfnoise = _selfnoise*1e6
    
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 3e2), xlabel='Frequency [Hz]',
                  #yscale='log', ylim=(1e-11, 3e-6),
                  yscale='log', ylim=(1e-5, 3e-0),
                  ylabel=r'Velocity [m/sec/\rtHz]')
    ax.plot(_f,_selfnoise,'-',linewidth=1,color='gray')
    ax.plot_mmm(median, low, high, color='gwpy:ligo-livingston')
    ax.set_title(chname.replace('_',' '),fontsize=16)
    ax.legend(labels=['Selfnoise','Measurement'])
    plot.savefig(pngfname)
    print 'plot in ',pngfname
    return plot
    
def plot_coherence(*args,**kwargs):
    fftlength = kwargs.pop('fftlength',2**7)
    N = len(args)
    if N==3:
        warnings.warn('! Dont use specgram')
        csd_specgram,psd_specgram1,psd_specgram2 = args
        angle = csd_specgram.mean(axis=0).angle().rad2deg()
        psd_specgram1 = psd_specgram1.mean(axis=0)
        psd_specgram2 = psd_specgram2.mean(axis=0)
        csd_mag = csd_specgram.mean(axis=0).abs()
        mag = csd_mag/psd_specgram1**(1/2.0)/psd_specgram2**(1/2.)
        plot, (ax_mag,ax_angle) = plt.subplots(nrows=2, sharex=True, figsize=(8, 6))
        ax_mag.plot(mag)
        ax_mag.set_xscale('log')
        ax_mag.set_ylabel('Coherence')        
        ax_angle.plot(angle)
        ax_angle.set_ylim(-180,180)
        ax_angle.set_xscale('log')
        ax_angle.set_ylabel('Phase [deg]')
        ax_angle.set_xlabel('Frequency [Hz]')
        plot.savefig('Coherence_with_cdsspectrogram.png')
        print 'plot in csd_spectrogram'
    elif N==2:
        chname1, chname2 = args
        timeseries1 = get_timeseries(chname1,from_nds=False,**kwargs)
        timeseries2 = get_timeseries(chname2,from_nds=False,**kwargs)
        kwargs.pop('start')
        kwargs.pop('end')
        coh = timeseries1.coherence(timeseries2,
                                    fftlength=fftlength,
                                    overlap=0,
                                    window='hanning',
                                    **kwargs)
        plot, (ax_mag,ax_angle) = plt.subplots(nrows=2, sharex=True, figsize=(8, 6))
        mag = coh
        ax_mag.plot(mag)
        ax_mag.set_ylim(0,1)
        ax_mag.set_xscale('log')
        ax_mag.set_ylabel('Coherence')        
        #ax_angle.plot(angle)
        ax_angle.set_ylim(-180,180)
        ax_angle.set_xscale('log')
        ax_angle.set_ylabel('Phase [deg]')
        ax_angle.set_xlabel('Frequency [Hz]')
        plot.savefig('Coherence_with_pure_coherenc.png')
        print 'plot in csd_spectrogram'
