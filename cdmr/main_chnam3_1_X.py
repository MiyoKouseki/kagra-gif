import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from gwpy.plot import Plot
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert
from glue import lal
import sys
sys.path.insert(0,'../../miyopy')
from miyopy.utils.trillium import Trillium120q
from gwpy.frequencyseries import FrequencySeries
from astropy import units as u

'''
chname3_1.gwf data contains these bellow channels in JST Dec02 11:00 - Dec03 07.
chname3 list;
'K1:PEM-IXV_GND_TR120Q_X_IN1_DQ',
'K1:PEM-IXV_GND_TR120Q_Y_IN1_DQ',
'K1:PEM-IXV_GND_TR120Q_Z_IN1_DQ',
'K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ',
'K1:PEM-IXV_GND_TR120QTEST_Y_IN1_DQ',
'K1:PEM-IXV_GND_TR120QTEST_Z_IN1_DQ',
'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ',
'K1:PEM-EXV_GND_TR120Q_Y_IN1_DQ',
'K1:PEM-EXV_GND_TR120Q_Z_IN1_DQ',
'K1:PEM-EYV_GND_TR120Q_X_IN1_DQ',
'K1:PEM-EYV_GND_TR120Q_Y_IN1_DQ',
'K1:PEM-EYV_GND_TR120Q_Z_IN1_DQ'

chname3_1_X.gwf data contains only X axis.

'''

def calc_asd(ts, fftlength=2**10):
    sg = ts.spectrogram2(fftlength=fftlength, overlap=fftlength/2., window='hanning') ** (1/2.)
    median_0,low_0,high_0 = sg.percentile(50), sg.percentile(5), sg.percentile(95)
    return median_0,low_0,high_0

# Data taking
start0 = tconvert('Dec 02 2018 11:00:00 JST')
end0 = tconvert('Dec 03 2018 07:00:00 JST')
end0 = start0 + 2**16
start,end = start0,end0
chname = ['K1:PEM-IXV_GND_TR120Q_X_IN1_DQ',
          'K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ',
          'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ',
]
kwargs = {}
kwargs['verbose'] = True
kwargs['format'] = 'gwf.lalframe'
kwargs['start'] = start
kwargs['end'] = end
kwargs['pad'] = np.nan
kwargs['nproc'] = 5
data = TimeSeriesDict.read('chname3_1_X.gwf',chname,**kwargs)


# Override unit of data from count to voltage.
c2v = (10/2**15)*u.V/u.ct # [1]
# [1] In the case of differential output.
exv_x = data['K1:PEM-EXV_GND_TR120Q_X_IN1_DQ']#.override_unit('ct')#*c2v
ixv1_x = data['K1:PEM-IXV_GND_TR120Q_X_IN1_DQ']#.override_unit('ct')#*c2v
ixv2_x = data['K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ']#.override_unit('ct')#*c2v
exv_x.override_unit('ct')#*c2v
ixv1_x.override_unit('ct')#*c2v
ixv2_x.override_unit('ct')#*c2v
exv_x = exv_x*c2v
ixv1_x = ixv1_x*c2v
ixv2_x = ixv2_x*c2v

# Calc differential and common components.
diff12 = ixv1_x - ixv2_x
diff02 = exv_x - ixv2_x
comm12 = ixv1_x - ixv2_x
comm02 = exv_x - ixv2_x

# Calc asd
median_0,low_0,high_0 = calc_asd(exv_x)
median_1,low_1,high_1 = calc_asd(ixv1_x)
median_2,low_2,high_2 = calc_asd(ixv2_x)
median_d12,low_d12,high_d12 = calc_asd(diff12)
median_d01,low_d01,high_d01 = calc_asd(diff02)

# Calibrate to velocity.    
amp = 10**(30/20.)
_v2vel = 1/1202.5*u.m/u.s/u.V
v2vel = Trillium120q.v2vel
median_0,low_0,high_0 = v2vel(median_0)/amp, v2vel(low_0)/amp, v2vel(high_0)/amp
median_1,low_1,high_1 = v2vel(median_1)/amp, v2vel(low_1)/amp, v2vel(high_1)/amp
median_2,low_2,high_2 = v2vel(median_2)/amp, v2vel(low_2)/amp, v2vel(high_2)/amp
median_d12,low_d12,high_d12 = v2vel(median_d12)/amp, v2vel(low_d12)/amp, v2vel(high_d12)/amp
median_d01,low_d01,high_d01 = v2vel(median_d01)/amp, v2vel(low_d01)/amp, v2vel(high_d01)/amp

# Get several noise
_adcnoise = 2e-6*u.V # Equivalent Input Noise [V/rtHz]. [1] 
_ampnoise = 6e-7*u.V # Output Noise [V/rtHz]. [2]
# [1] JGW-S1402729 (for IY1 not found IX1..)
# [2] JGW-S1605058 (for IX1 rack). When use 30db(24+6db),
#     24db noise affect of 4e-7 [Vrms/rtHz]. As transferomation
#     from Vrms to V is given by Vrms = V / sqrt(2),
#     then 4e-7*1.4 = 6e-7 [V/rtHz]
selfnoise = Trillium120q.selfnoise()
_adcnoise = FrequencySeries(_adcnoise*np.ones(len(median_0)),frequencies=median_0.frequencies)
_ampnoise = FrequencySeries(_ampnoise*np.ones(len(median_0)),frequencies=median_0.frequencies)
adcnoise = v2vel(_adcnoise)/amp
ampnoise = v2vel(_ampnoise)#/amp


# Plot
from gwpy.plot import Plot
plot = Plot()
ax = plot.gca(xscale='log', xlim=(1e-3, 100), xlabel='Frequency [Hz]',
              yscale='log', ylim=(1e-11, 1e-5),
              ylabel=r'Velocity [m/sec/\rtHz]')

if True:
    ax.loglog(selfnoise,label='Self Noise',linewidth=2,alpha=0.7,linestyle='--')
    ax.loglog(adcnoise,label='ADC EIN',linewidth=2,alpha=0.7,linestyle='--')
    ax.loglog(ampnoise,label='Amp EIN',linewidth=2,alpha=0.7,linestyle='--')
    ax.loglog(median_0,label='EXV',color='black')    
    ax.loglog(median_1,label='IXV1')
    ax.loglog(median_2,label='IXV2')
    ax.loglog(median_d12,label='IXV1-IXV2')
    #ax.loglog(median_d01,label='diff01')
    
ax.legend()    
ax.set_title('Seismometer',fontsize=16)
plot.savefig('ASD_chname3_1_ixv_x.png')
