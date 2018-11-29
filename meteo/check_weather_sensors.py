#
#! coding:utf-8
import warnings
import numpy as np
import matplotlib
matplotlib.rcParams['backend'] = 'TkAgg'
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.units import Unit
from gwpy.detector import ChannelList
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
from gwpy.plotter import TimeSeriesPlot,Plot
from gwpy.plotter import text as plotter_text
from gwpy.plot import Plot,text
from matplotlib.artist import setp
from gwpy.plot import Plot
from matplotlib.artist import setp
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_timeseries(*data,**kwargs):
    title = kwargs.pop('title',None)
    ylim = kwargs.pop('ylim',None)
    fname = kwargs.pop('fname','TimeSeries.png')
    plot = Plot(figsize=(15,10))
    ax0 = plot.gca()
    ax0.plot(*data)
    ax0.legend([text.to_string(_data.name) for _data in data],fontsize=20)
    ax0.set_xscale('auto-gps')
    ax0.set_ylabel(text.to_string(data[0].unit))
    plot.add_state_segments(segments_daq_iy0_ok,label='IY0 DAQ State')
    plot.add_state_segments(segments_daq_ix1_ok,label='IX1 DAQ State')    
    plot.suptitle(title,fontsize=40)
    if ylim:
        ax0.set_ylim(ylim[0],ylim[1])
    plot.savefig(fname)
    plot.close()


def plot_coherence():
    fftlength = 2**11
    coh_temp = no5_baro.coherence(no6_temp,fftlength=fftlength)
    coh_humd = no5_baro.coherence(no6_humd,fftlength=fftlength)
    coh_baro = no5_baro.coherence(no6_baro,fftlength=fftlength)
    plot, (ax0,ax1,ax2) = plt.subplots(nrows=3, figsize=(9, 10), sharex=True)
    ax0.semilogx(coh_temp,label='No6(IYC)/No5(IXV)')
    ax1.semilogx(coh_humd,label='No6(IYC)/No5(IXV)')             
    ax2.semilogx(coh_baro,label='No6(IYC)/No5(IXV)')
    ax0.set_ylabel('Temperature')
    ax1.set_ylabel('Humidity')
    ax2.set_ylabel('Air pressure')
    ax2.set_xlabel('Frequency [Hz]')
    ax0.set_ylim(0,1)
    ax1.set_ylim(0,1)
    ax2.set_ylim(0,1)
    ax0.legend(loc='upper right')
    ax1.legend(loc='upper right')
    ax2.legend(loc='upper right')
    plot.suptitle('Coherence',fontsize=30)
    plot.savefig('Coherence.png')


def plot_asd():    
    fftlength = 2**11    
    asd_no5_temp = no5_temp.asd(fftlength=fftlength)
    asd_no6_temp = no6_temp.asd(fftlength=fftlength)
    asd_no5_humd = no5_humd.asd(fftlength=fftlength)
    asd_no6_humd = no6_humd.asd(fftlength=fftlength)
    asd_no5_baro = no5_baro.asd(fftlength=fftlength)
    asd_no6_baro = no6_baro.asd(fftlength=fftlength)
    plot, (ax0,ax1,ax2) = plt.subplots(nrows=3, figsize=(9, 10), sharex=True)
    ax0.loglog(asd_no5_temp,label='No5(IXV)')
    ax0.loglog(asd_no6_temp,label='No6(IYC)')
    ax1.loglog(asd_no5_humd,label='No5(IXV)')
    ax1.loglog(asd_no6_humd,label='No6(IYC)')
    ax2.loglog(asd_no5_baro,label='No5(IXV)')
    ax2.loglog(asd_no6_baro,label='No6(IYC)')
    fs = no5_temp.sample_rate.value
    xlimmax = fs/2.0/2.0
    xlimmin = asd_no5_baro.frequencies[1].value
    ax0.set_xlim(xlimmin,xlimmax)
    #ax0.set_ylim(1e-2,2e2)
    #ax1.set_ylim(1e-2,2e2)
    #ax2.set_ylim(1e-2,2e2)
    ax0.axhline(1e-4,xlimmin,xlimmax,linestyle='--',color='k',label='Circuit Noise')
    ax1.axhline(1e-4,xlimmin,xlimmax,linestyle='--',color='k',label='Circuit Noise')
    ax2.axhline(1e-4,xlimmin,xlimmax,linestyle='--',color='k',label='Circuit Noise')
    ax1.set_xlim(xlimmin,xlimmax)
    ax2.set_xlim(xlimmin,xlimmax)
    ax0.legend(loc='upper right')
    ax1.legend(loc='upper right')
    ax2.legend(loc='upper right')
    ax0.set_ylabel('Temperature\n'+plotter_text.unit_as_label(no5_temp.unit).replace(']','/rtHz]'),fontsize=15)
    ax1.set_ylabel('Humidity\n'+plotter_text.unit_as_label(no5_humd.unit).replace(']','/rtHz]'),fontsize=15)
    ax2.set_ylabel('Air Pressure\n'+plotter_text.unit_as_label(no5_baro.unit).replace(']','/rtHz]'),fontsize=15)
    ax2.set_xlabel('Frequency [Hz]')
    plot.suptitle('Amplitude Spectrum Density',fontsize=30)
    plot.savefig('ASD.png')


    

if __name__=='__main__':    
    start = tconvert('Nov 28 2018 18:00:00 JST') # before daq killed
    #start = tconvert('Nov 28 2018 21:30:10 JST') # after daq killed
    start = tconvert('Nov 29 2018 00:00:10 JST') # data stable
    end = tconvert('Nov 29 2018 09:00:00 JST') # stable continuously
    
    chlst = [
        'K1:PEM-IXV_WEATHER_TEMP_INMON',
        'K1:PEM-IXV_WEATHER_HUMD_INMON',
        'K1:PEM-IXV_WEATHER_PRES_INMON',
        'K1:PEM-IYC_WEATHER_TEMP_INMON',
        'K1:PEM-IYC_WEATHER_HUMD_INMON',
        'K1:PEM-IYC_WEATHER_PRES_INMON',
        'K1:FEC-99_STATE_WORD_FE',    
        'K1:FEC-121_STATE_WORD_FE',
        ]

    kwargs = {}
    kwargs['verbose'] = True
    kwargs['pad'] = np.nan
    kwargs['port'] = 8088
    kwargs['host'] = '10.68.10.121'
    data = TimeSeriesDict.fetch(chlst,start,end,**kwargs)
    
    c2V = 2.0*10.0/2**15*u.V/u.ct
    no5_temp = data['K1:PEM-IXV_WEATHER_TEMP_INMON']*c2V
    no5_humd = data['K1:PEM-IXV_WEATHER_HUMD_INMON']*c2V
    no5_baro = data['K1:PEM-IXV_WEATHER_PRES_INMON']*c2V
    no6_temp = data['K1:PEM-IYC_WEATHER_TEMP_INMON']*c2V
    no6_humd = data['K1:PEM-IYC_WEATHER_HUMD_INMON']*c2V
    no6_baro = data['K1:PEM-IYC_WEATHER_PRES_INMON']*c2V
    daq_iy0 = data['K1:FEC-99_STATE_WORD_FE']
    daq_ix1 = data['K1:FEC-121_STATE_WORD_FE']
    
    daq_iy0_ok = daq_iy0 == 0
    daq_ix1_ok = daq_ix1 == 0    
    segments_daq_iy0_ok = daq_iy0_ok.to_dqflag(round=False)
    segments_daq_ix1_ok = daq_ix1_ok.to_dqflag(round=False)
    
    if True:
        plot_timeseries(no5_temp,no6_temp,ylim=[25,30],
                        fname='TimeSeries_temp.png',title='Temperature')
        plot_timeseries(no5_humd,no6_humd,ylim=[30,50],
                        fname='TimeSeries_humd.png',title='Humidity')
        plot_timeseries(no5_baro,no6_baro,ylim=[970,980],
                        fname='TimeSeries_baro.png',title='Air Pressure')
    
    plot_coherence()
    plot_asd()
    
