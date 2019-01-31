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

# gif data
pfx = '/Users/miyo/KagraData/gif/'
from miyopy.gif.datatype import GifData
start = tconvert('Dec 02 2018 11:00:00')
end = tconvert('Dec 03 2018 07:00:00')
#end = 'Dec 02 2018 11:01:00'

segments = GifData.findfiles(start,end,'X1500_TR240posEW',prefix=pfx)
allfiles = [path for files in segments for path in files]

strain = TimeSeries.read(source=allfiles,
                         name='X1500_TR240posEW',
                         format='gif',
                         pad=np.nan,
                         nproc=2)
strain = strain/1196.5
plot = strain.plot()
plot.savefig('hoge_ts.png')

print(strain)

#exit()

def calc_asd(ts, fftlength=2**10):
    sg = ts.spectrogram2(fftlength=fftlength, overlap=fftlength/2., window='hanning') ** (1/2.)
    median_0,low_0,high_0 = sg.percentile(50), sg.percentile(5), sg.percentile(95)
    return median_0,low_0,high_0

median_d12,low_d12,high_d12 = calc_asd(strain)

def save(data,fname='tmp.hdf5'):
    data.write(fname,format='hdf5')

median_d12.name = 'X1500_TR240posEW'
print median_d12
#save(median_d12, fname='./chname3_1_X_x1500.hdf5')


from gwpy.plot import Plot
plot = Plot()
ax = plot.gca(xscale='log', xlim=(1e-3, 100), xlabel='Frequency [Hz]',
              yscale='log', #ylim=(1e-11, 1e-5),
              ylabel=r'Velocity [m/sec/\rtHz]')
ax.loglog(median_d12,label='IXV1-IXV2')

ax.legend()    
ax.set_title('Seismometer',fontsize=16)
plot.savefig('hoge.png')

exit()







def read(fname):
    return FrequencySeries.read(fname,format='hdf5')        
median_0 = read('chname3_1_X_exv_50pct.hdf5')
median_1 = read('chname3_1_X_ixv1_50pct.hdf5')
median_2 = read('chname3_1_X_ixv2_50pct.hdf5')
median_d12 = read('chname3_1_X_diff12_50pct.hdf5')
median_c12 = read('chname3_1_X_comm12_50pct.hdf5')




# Get several noise
amp = 10**(30/20.)
v2vel = Trillium120q.v2vel
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
