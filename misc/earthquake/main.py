import numpy as np

from astropy import units as u

from gwpy.timeseries import StateTimeSeries
from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert

''' 

1.
M6.7, Iburi,  2018/09/06 03:07:59.3
M5.2, Nagano, 2018/05/25 21:13:42.2

'''

__author__ = 'Koseki.miyo'

seis = TimeSeries.read('bKAGRA_rms_ground_velocity_hor.gwf',
                       'K1:PEM-EX1_SEIS_WE_BLRMS_LOW_OUT_DQ.rms',
                       format='gwf.lalframe')
mich = TimeSeries.read('bKAGRA_mich_state.gwf',
                       'K1:GRD-LSC_MICH_STATE_N',
                       start=tconvert('Apr 28 2018 09:00:00 JST'),
                       end=tconvert('May 6 2018 09:00:00 JST')+78,   
                       format='gwf.lalframe')
_mich = (mich >= 100).value
print mich.t0
print mich.dt
print mich.shape
print _mich.shape
print _mich.shape[0]-16*60*60*24*8
#print float(_mich.shape[0])/(16*60*60*24)
_mich = np.average(_mich.reshape(16*60*60*24,_mich.shape[0]/(16*60*60*24)),axis=0)
print _mich.shape
#exit()
_mich = TimeSeries(_mich,dt=3600*24*u.s,t0=mich.t0)
print _mich
#exit()
plot = seis.plot(
    figsize=(15,5),
    color='black',
    ylim=(0,3e-6),
    #xlim=(seis.t0.value, seis.t0.value+60*60*24*7*8),
    xlim=(tconvert('Apr 28 2018 09:00:00 JST'),tconvert('May 6 2018 09:00:00 JST')+78),
    #xlim=(tconvert('Apr 8 2018 00:00:00 UTC'),tconvert('Jun 1 2018 00:00:00 UTC')+78),
    epoch=tconvert('Apr 28 2018 09:00:00 JST'),
    #epoch=tconvert('Apr 8 2018 09:00:00 UTC'),
    ylabel='Velocity [m/s]',
    title='RMS of horizontal ground velocity at the site',
    )

_n = seis.value.shape
_dt = 1/seis.dt
_t0 = seis.t0
_bit = seis.times > int(tconvert('Apr 28 2018 9:0:0 JST'))*u.s
bit = _bit * (seis.times < int(tconvert('May 8 2018 9:0:0 JST'))*u.s )
phase1 = StateTimeSeries(bit,sample_rate=_dt, epoch=_t0).to_dqflag(round=True)
#_n = mich.value.shape
#_dt = 1/mich.dt
#_t0 = mich.t0
bit = mich >= 100
mich = bit.to_dqflag(round=True)


ax = plot.gca()
#ax.plot(_mich*3e-6,marker='o')
ax.legend([seis.name.replace('_','\_')])
plot.add_segments_bar(mich,label='Mich locked')
plot.savefig('bKAGRA_rms_ground_velocity_hor_phase1.png')
#plot.savefig('bKAGRA_rms_ground_velocity_hor.png')
