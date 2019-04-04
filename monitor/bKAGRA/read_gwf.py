import numpy as np

from astropy import units as u

from gwpy.timeseries import StateTimeSeries
from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert

''' 

1. bKAGRA_rms_ground_velocity_hor.gwf

Start : 2018-04-07 00:00:42 JST 
End   : 2018-06-01 00:00:42 JST 
Channel : 'K1:PEM-EX1_SEIS_WE_BLRMS_LOW_OUT_DQ.rms'
- RMS of horizontal ground velocity at the site within a 10-minute interval
after a band-bass filter (0.01-1Hz).

2. 


'''

__author__ = 'Koseki.miyo'

seis = TimeSeries.read('bKAGRA_rms_ground_velocity_hor.gwf',
                       'K1:PEM-EX1_SEIS_WE_BLRMS_LOW_OUT_DQ.rms',
                       format='gwf.lalframe')

plot = seis.plot(
    figsize=(15,5),
    color='black',
    ylim=(0,3e-6),
    xlim=(seis.t0.value,seis.t0.value+60*60*24*7*8),
    epoch=seis.t0,
    ylabel='Velocity [m/s]',
    title='RMS of horizontal ground velocity at the site',
    )

print seis.value.shape
_n = seis.value.shape
_dt = 1/seis.dt
_t0 = seis.t0
_bit = seis.times > int(tconvert('Apr 28 2018 9:0:0 JST'))*u.s
bit = _bit * (seis.times < int(tconvert('May 8 2018 9:0:0 JST'))*u.s )
phase1 = StateTimeSeries(bit,sample_rate=_dt, epoch=_t0).to_dqflag(round=True)

ax = plot.gca()
ax.legend([seis.name.replace('_','\_')])
#plot.add_segments_bar(h1segs,label='MICH_LOCK')
plot.add_segments_bar(phase1,label='bKAGRA phase1')
plot.savefig('bKAGRA_rms_ground_velocity_hor.png')

