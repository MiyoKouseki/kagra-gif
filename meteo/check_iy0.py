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
from gwpy.plotter import TimeSeriesPlot,Plot,text
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
    if np.all(v < 0):
        v = -v
    val = v/5.0/2.0*(100.0*u.pct/u.V)
    return val


def v2baro(v,**kwargs):
    if not v.unit == 'V':
        raise ValueError('!')
    val = v/2.0/5.0*(1100.0-800.0)*(u.hPa/u.V)+800.0*u.hPa
    return val



start = tconvert('Nov 26 2018 11:10:00 JST')
end = tconvert('Nov 26 2018 17:20:00 JST')

chname_wether = 'K1:PEM-IY0_SENSOR*_INMON'
chlst = ChannelList.query_nds2([chname_wether],host='10.68.10.121',port=8088)
chlst = [ ch.name for ch in chlst]
data = TimeSeriesDict.fetch(chlst,start,end,host='10.68.10.121',port=8088,verbose=True,pad=np.nan)
no4_temp = v2temp(data['K1:PEM-IY0_SENSOR5_INMON']*c2V)
no4_humd = v2humd(data['K1:PEM-IY0_SENSOR6_INMON']*c2V)
no4_baro = v2baro(data['K1:PEM-IY0_SENSOR7_INMON']*c2V)
x500_sub_temp = v2temp(data['K1:PEM-IY0_SENSOR9_INMON']*c2V)
x500_sub_humd = v2humd(data['K1:PEM-IY0_SENSOR10_INMON']*c2V)
x500_sub_baro = v2baro(data['K1:PEM-IY0_SENSOR11_INMON']*c2V)

plot, (ax0,ax1,ax2) = plt.subplots(nrows=3, figsize=(10, 10), sharex=True)
ax0.plot(no4_temp,label='No4')
ax0.plot(x500_sub_temp,label='x500 sub')
ax0.legend()
ax0.set_ylabel(text.unit_as_label(no4_temp.unit))
ax1.plot(no4_humd,label='No4')
ax1.plot(x500_sub_humd,label='x500 sub')
ax1.legend()
ax1.set_ylabel(text.unit_as_label(no4_humd.unit))
ax2.plot(no4_baro,label='No4')
ax2.plot(x500_sub_baro,label='x500 sub')
ax2.legend()
ax2.set_xscale('auto-gps')
ax2.set_ylabel(text.unit_as_label(no4_baro.unit))
plot.suptitle('Air environment monitor\n Temperature,Humidity,AirPressure.',fontsize=30)
plot.savefig('TimeSeries.png')
