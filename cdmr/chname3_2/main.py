import sys
sys.path.insert(0,'../../miyopy')

import numpy as np
import matplotlib
matplotlib.use('Agg')

from astropy import units as u

from gwpy.plot import Plot
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert

from miyopy.utils.trillium import Trillium



'''
chname3_2.gwf data contains these bellow channels in JST Dec02 11:00 - Dec03 07.
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

chname3_2_X.gwf data contains only X axis.

'''

# gif data
pfx = '/Users/miyo/KagraData/gif/'
from miyopy.gif.datatype import GifData
start = tconvert('Dec 02 2018 11:00:00')
end = tconvert('Dec 03 2018 07:00:00')
end = start + 2**16
#end = 'Dec 02 2018 11:01:00'

def read_gif(chname,start,end,write=False):    
    segments = GifData.findfiles(start,end,chname,prefix=pfx)
    allfiles = [path for files in segments for path in files]    
    strain = TimeSeries.read(source=allfiles,
                            name=chname,
                            format='gif',
                            pad=np.nan,
                            nproc=2)
    strain.name = chname
    if write:
        strain.write('./chname3_2_tr240ew.gwf',format='gwf.lalframe')
        
def calc_asd(ts, fftlength=2**10):
    sg = ts.spectrogram2(fftlength=fftlength,
                         overlap=fftlength/2.,
                             window='hanning') ** (1/2.)
    median_0,low_0,high_0 = sg.percentile(50), sg.percentile(5), sg.percentile(95)
    return median_0,low_0,high_0
        

def read(fname):
    return FrequencySeries.read(fname,format='hdf5')


median_0 = read('chname3_2_X_exv_50pct.hdf5')
median_1 = read('chname3_2_X_ixv1_50pct.hdf5')
median_2 = read('chname3_2_X_ixv2_50pct.hdf5')
median_d12 = read('chname3_2_X_diff12_50pct.hdf5')
median_c12 = read('chname3_2_X_comm12_50pct.hdf5')
median_x1500 = read('./chname3_2_X_x1500_50pct.hdf5')
median_strain = read('./chname3_2_X_strain_50pct.hdf5')


# Get several noise
amp = 10**(30/20.)
tr120q = Trillium('120QA')
tr240 = Trillium('240')
v2vel = tr120q.v2vel
_adcnoise = 2e-6*u.V # Equivalent Input Noise [V/rtHz]. [1]
_adcnoise2 = np.sqrt((10/2**15)**2/12/(214/2))*u.V # Equivalent Input Noise [V/rtHz]. [1]
_ampnoise = 6e-7*u.V # Output Noise [V/rtHz]. [2]
_aanoise = 7e-8*u.V # Equivalent Input Noise [V/rtHz]. 
# [1] JGW-S1402729 (for IY1 not found IX1..)
# [2] JGW-S1605058 (for IX1 rack). When use 30db(24+6db),
#     24db noise affect of 4e-7 [Vrms/rtHz]. As transferomation
#     from Vrms to V is given by Vrms = V / sqrt(2),
#     then 4e-7*1.4 = 6e-7 [V/rtHz]
selfnoise_120q = tr120q.selfnoise()
selfnoise_240 = tr240.selfnoise()
_adcnoise = FrequencySeries(_adcnoise*np.ones(len(median_0)),frequencies=median_0.frequencies)
_adcnoise2 = FrequencySeries(_adcnoise2*np.ones(len(median_0)),frequencies=median_0.frequencies)
_ampnoise = FrequencySeries(_ampnoise*np.ones(len(median_0)),frequencies=median_0.frequencies)
_aanoise = FrequencySeries(_aanoise*np.ones(len(median_0)),frequencies=median_0.frequencies)
adcnoise = v2vel(_adcnoise)/amp
ampnoise = v2vel(_ampnoise)/amp # 
aanoise = v2vel(_aanoise)/amp

v2vel = tr240.v2vel
median_x1500 = v2vel(median_x1500)/2.0#/amp

#median_strain = median_strain*550.0/median_strain.frequencies.value
# ??????????????????????????????????????????????????????????????
median_strain = median_strain*3000 # ???????????????????????????
# ??????????????????????????????????????????????????????????????

# Plot
from gwpy.plot import Plot
plot = Plot()
ax = plot.gca(xscale='log', xlim=(1e-3, 10), xlabel='Frequency [Hz]',
              yscale='log', ylim=(1e-12, 1e-4),
              ylabel=r'Velocity [m/sec/\rtHz]')


if True:
    ax.loglog(median_x1500,label='x1500 (ref. GIF data)')    
    ax.loglog(selfnoise_120q,'k--',label='Self Noise 120Q',linewidth=1,alpha=0.7)
    ax.loglog(selfnoise_240,'m--',label='Self Noise 240',linewidth=1,alpha=0.7)
    ax.loglog(adcnoise,'r--',label='ADC Noise',linewidth=1,alpha=0.7)
    ax.loglog(ampnoise,'g--',label='Amp Noise',linewidth=1,alpha=0.7)
    ax.loglog(aanoise,'b--',label='AA Noise',linewidth=1,alpha=0.7)        
    ax.loglog(median_0,'k-',label='EXV')    
    ax.loglog(median_1,label='IXV1')
    ax.loglog(median_2,label='IXV2')
    ax.loglog(median_d12,label='IXV1-IXV2')
    ax.loglog(median_strain,label='StrainMeter')

    
ax.legend(fontsize=8,loc='lower left')    
ax.set_title('Seismometer',fontsize=16)
plot.savefig('ASD_chname3_2_X.png')
