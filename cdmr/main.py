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

def read(fname):
    
    try:     
        data = FrequencySeries.read(fname,format='hdf5')
    except IOError as ioe:
        print(ioe)
        exit()
    else:
        pass
    
    return data

'''
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
'''

import argparse 
parser = argparse.ArgumentParser(description='description')
parser.add_argument('dataname', help='help')
parser.add_argument('--Plot')
args = parser.parse_args()
dataname = args.dataname

hdf5_fmt = './{dataname}/Xaxis_{sensor}_50pct.hdf5'.replace("{dataname}",dataname)


# Load FrequencySeries from saved hdf5 files.
if True:
    exv0 = read(hdf5_fmt.format(sensor='exv'))
    ixv1 = read(hdf5_fmt.format(sensor='ixv1'))
    ixv2 = read(hdf5_fmt.format(sensor='ixv2'))
    d12 = read(hdf5_fmt.format(sensor='diff12'))
    c12 = read(hdf5_fmt.format(sensor='comm12'))
    x1500 = read(hdf5_fmt.format(sensor='x1500'))
    strain = read(hdf5_fmt.format(sensor='strain'))
    #strain = strain*550.0/strain.frequencies.value
    # ??????????????????????????????????????????????????????????????
    strain = strain#*3000 # ???????????????????????????
    # ??????????????????????????????????????????????????????????????
    



# Calcrate several noises
if True:
    ref = exv0
        
    _adcnoise = 2e-6*u.V*np.ones(len(ref)) # [V/rtHz]
    _adcnoise2 = np.sqrt((10/2**15)**2/12/(214/2))*u.V*np.ones(len(ref)) # [V/rtHz]
    _ampnoise = 6e-7*u.V*np.ones(len(ref)) # [V/rtHz]
    _aanoise = 7e-8*u.V*np.ones(len(ref)) # [V/rtHz]
        
    _adcnoise = FrequencySeries(_adcnoise, frequencies=ref.frequencies)
    _adcnoise2 = FrequencySeries(_adcnoise2, frequencies=ref.frequencies)
    _ampnoise = FrequencySeries(_ampnoise, frequencies=ref.frequencies)
    _aanoise = FrequencySeries(_aanoise, frequencies=ref.frequencies)

    amp = 10**(30/20.)
    tr120q = Trillium('120QA')
    tr240 = Trillium('240')
    v2vel = tr120q.v2vel
    v2vel = tr240.v2vel
    
    adcnoise = v2vel(_adcnoise)/amp
    ampnoise = v2vel(_ampnoise)/amp # 
    aanoise = v2vel(_aanoise)/amp   
    selfnoise_120q = tr120q.selfnoise()
    selfnoise_240 = tr240.selfnoise()


# Plot
if True:
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 10), xlabel='Frequency [Hz]',
                  yscale='log', ylim=(1e-12, 1e-4),
                  ylabel=r'Velocity [m/sec/\rtHz]'
                  )    
    ax.loglog(x1500,label='x1500 (ref. GIF data)')    
    ax.loglog(selfnoise_120q,'k--',label='Self Noise 120Q',linewidth=1,alpha=0.7)
    ax.loglog(selfnoise_240,'m--',label='Self Noise 240',linewidth=1,alpha=0.7)
    ax.loglog(adcnoise,'r--',label='ADC Noise',linewidth=1,alpha=0.7)
    ax.loglog(ampnoise,'g--',label='Amp Noise',linewidth=1,alpha=0.7)
    ax.loglog(aanoise,'b--',label='AA Noise',linewidth=1,alpha=0.7)        
    ax.loglog(exv0,'k-',label='EXV')    
    ax.loglog(ixv1,label='IXV1')
    ax.loglog(ixv2,label='IXV2')
    ax.loglog(d12,label='IXV1-IXV2')
    ax.loglog(strain,label='StrainMeter')
    #
    ax.legend(fontsize=8,loc='lower left')    
    ax.set_title('Seismometer, {dname}'.format(dname=dataname.replace('_','')),fontsize=16)
    plot.savefig('./{dname}/ASD_{dname}_X.png'.format(dname=dataname))
    print('save ./{dname}/ASD_{dname}_X.png'.format(dname=dataname))
