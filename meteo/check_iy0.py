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
#from gwpy.plotter import TimeSeriesPlot,Plot,text
from gwpy.plot import Plot,text
from matplotlib.artist import setp

'''
好きな時間の気象計のデータをプロットする。
'''

c2V = 2.0*10.0/2**15 *u.V/u.ct

def v2temp(v,gif=False,**kwargs):
    if not v.unit == 'V':
        raise ValueError('!')
    ohm = v/78.0/(0.001*u.A)
    temp = (ohm-100.0*u.ohm)/(0.388*u.ohm/u.deg_C)
    return temp.decompose()


def v2humd(v,**kwargs):
    if not v.unit == 'V':
        raise ValueError('!')
    if  np.nanmean(v)<0:
        v = -v
    val = v/5.0/2.0*(100.0*u.pct/u.V)
    return val


def v2baro(v,**kwargs):
    if not v.unit == 'V':
        raise ValueError('!')
    val = v/2.0/5.0*(1100.0-800.0)*(u.hPa/u.V)+800.0*u.hPa
    return val



start = tconvert('Nov 26 2018 11:10:00 JST') # installed time
start = tconvert('Nov 27 2018 09:35:00 JST') # open door time
start = tconvert('Nov 27 2018 11:15:00 JST') # mounted time iyc
start = tconvert('Nov 27 2018 12:10:00 JST') #
start = tconvert('Nov 27 2018 16:35:00 JST') #
start = tconvert('Nov 27 2018 23:00:00 JST') # rename iyc
start = tconvert('Nov 29 2018 06:00:00 JST') # rename iyc
start = tconvert('Nov 28 2018 20:00:10 JST') # restart daq after rename
#start = tconvert('Nov 29 2018 09:00:10 JST') # 
end = tconvert('Nov 29 2018 11:01:00 JST')

chlst = [
    'K1:PEM-IY0_SENSOR5_OUTMON',
    'K1:PEM-IY0_SENSOR6_OUTMON',
    'K1:PEM-IY0_SENSOR7_OUTMON',
    'K1:PEM-IY0_SENSOR8_OUTMON',
    'K1:PEM-IY0_SENSOR9_OUTMON',
    'K1:PEM-IY0_SENSOR10_OUTMON',
    'K1:PEM-IY0_SENSOR11_OUTMON',
    'K1:FEC-99_STATE_WORD_FE',    
    'K1:FEC-121_STATE_WORD_FE',
    ]
    
cache = './hoge'
data = TimeSeriesDict.read(source,channels,start,end,verbose=True,pad=np.nan,format='gwf.lalframe',nproc=2)

daq_iy0 = data['K1:FEC-99_STATE_WORD_FE']
daq_ix1 = data['K1:FEC-121_STATE_WORD_FE']
no5_temp = data['K1:PEM-IXV_SENSOR5_OUTMON']
no5_humd = data['K1:PEM-IXV_SENSOR6_OUTMON']
no5_baro = data['K1:PEM-IXV_SENSOR7_OUTMON']
no6_temp = data['K1:PEM-IXV_SENSOR9_OUTMON']
no6_humd = data['K1:PEM-IXV_SENSOR10_OUTMON']
no6_baro = data['K1:PEM-IXV_SENSOR11_OUTMON']

daq_iy0_ok = daq_iy0 == 0
segments_daq_iy0_ok = daq_iy0_ok.to_dqflag(round=False)
daq_ix1_ok = daq_ix1 == 0
segments_daq_ix1_ok = daq_ix1_ok.to_dqflag(round=False)
#sdf_iy0_ok = sdf == 0
#segments_sdf_iy0_ok = sdf_iy0_ok.to_dqflag(round=False)
#sdf_ix1_ok = sdf == 0
#segments_sdf_ix1_ok = sdf_ix1_ok.to_dqflag(round=False)


# TimeSeries_temp.png
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

if True:
    plot_timeseries(no5_temp,no6_temp,ylim=[25,30],
                    fname='TimeSeries_temp.png',title='Temperature')
    plot_timeseries(no5_humd,no6_humd,ylim=[30,50],
                    fname='TimeSeries_humd.png',title='Humidity')
    plot_timeseries(no5_baro,no6_baro,ylim=[970,980],
                    fname='TimeSeries_baro.png',title='Air Pressure')
    
exit()
ASD.png
fftlength = 2**11
asd_no5_temp = no5_temp.asd(fftlength=fftlength)
asd_no6_temp = no6_temp.asd(fftlength=fftlength)
asd_no5_humd = no5_humd.asd(fftlength=fftlength)
asd_no6_humd = no6_humd.asd(fftlength=fftlength)
asd_no5_baro = no5_baro.asd(fftlength=fftlength)
asd_no6_baro = no6_baro.asd(fftlength=fftlength)
plot, (ax0,ax1,ax2) = plt.subplots(nrows=3, figsize=(8, 10), sharex=True)
ax0.loglog(asd_no5_temp,label='No5(IXV)')
ax0.loglog(asd_no6_temp,label='No6(IYC)')
ax1.loglog(asd_no5_humd,label='No5(IXV)')
ax1.loglog(asd_no6_humd,label='No6(IYC)')
ax2.loglog(asd_no5_baro,label='No5(IXV)')
ax2.loglog(asd_no6_baro,label='No6(IYC)')
fs = no5_temp.sample_rate.value
xlimmax = fs/2.0#/2.0
xlimmin = asd_no5_baro.frequencies[1].value
ax0.set_xlim(xlimmin,xlimmax)
ax1.set_xlim(xlimmin,xlimmax)
ax2.set_xlim(xlimmin,xlimmax)
ax0.legend()
ax1.legend()
ax2.legend()
ax0.set_ylabel(text.unit_as_label(no5_temp.unit))
ax1.set_ylabel(text.unit_as_label(no5_humd.unit))
ax2.set_ylabel(text.unit_as_label(no5_baro.unit))
ax2.set_xlabel('Frequency [Hz]')
plot.savefig('ASD.png')
