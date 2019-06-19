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
from miyopy.utils.trillium import Trillium
from gwpy.frequencyseries import FrequencySeries
from astropy import units as u
from lalframe.utils import frtools

amp = 10**(30/20.)
_v2vel = 1/1202.5*u.m/u.s/u.V
tr120q = Trillium('120QA')
v2vel = tr120q.v2vel


# --------------------
#   Utils
# --------------------
def asd(ts, fftlength=2**10,percentile=50):
    sg = ts.spectrogram2(fftlength=fftlength,overlap=fftlength/2.0) ** (1/2.)
    return sg.percentile(percentile)

def csd(ts1, ts2, fftlength=2**10):
    csd = ts1.csd(ts2,fftlength=fftlength)
    return csd

def save(data,fname='tmp.hdf5',overwrite=True):
    data.write(fname,format='hdf5',overwrite=True)



# --------------------
#   Parse Argument
# --------------------    
import argparse 
parser = argparse.ArgumentParser(description='description')
parser.add_argument('dataname',nargs='*', help='data name which you want to calculate')
parser.add_argument('--Plot')
args = parser.parse_args()
dataname = args.dataname[0]


# ------------------------
#   Read timeseries data
# ------------------------
c2v = (10.0/2**15)*u.V/u.ct
gwf_fname = './{dataname}/X.gwf'.format(dataname=dataname)
chnames = frtools.get_channels(gwf_fname)
datadict = TimeSeriesDict.read(gwf_fname,chnames,format='gwf.lalframe',nproc=2,verbose=True)

for data in datadict.values():
    data.override_unit('ct')
    data = data*c2v
    
if 'chname3' in dataname:
    exv_x = datadict['K1:PEM-EXV_GND_TR120Q_X_IN1_DQ']
    ixv1_x = datadict['K1:PEM-IXV_GND_TR120Q_X_IN1_DQ']
    ixv2_x = datadict['K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ']
elif 'chname4' in datadictname:
    exv_x = datadict['K1:PEM-SEIS_EXV_GND_EW_IN1_DQ']
    ixv1_x = datadict['K1:PEM-SEIS_IXV_GND_EW_IN1_DQ']
    eyv_x = datadict['K1:PEM-SEIS_EYV_GND_EW_IN1_DQ']
else:
    raise ValueError('Invalid data name')

if 'chname3' in dataname:
    diff12 = ixv1_x - ixv2_x
    comm12 = ixv1_x + ixv2_x
    diff13 = ixv1_x - exv_x
    comm13 = ixv1_x + exv_x
    print('Read timeseries data.')
else:
    raise ValueError('Invalid data name')

# -------------------
# Calc ASD
# -------------------
md_0 = asd(exv_x,fftlength=2**8,percentile=50)
md_1 = asd(ixv1_x,fftlength=2**8,percentile=50)
md_1 = asd(ixv2_x,fftlength=2**8,percentile=50)
md_d12 = asd(diff12,fftlength=2**8,percentile=50)
md_c12 = asd(comm12,fftlength=2**8,percentile=50)
md_d13 = asd(diff13,fftlength=2**8,percentile=50)
md_c13 = asd(comm13,fftlength=2**8,percentile=50)
# Calibrate to velocity.
from miyopy.utils.trillium import tr120
freq = md_0.frequencies.value
v2vel = tr120.tf(freq)
md_0 = v2vel*md_0/amp
md_1 = v2vel*md_1/amp
md_2 = v2vel*md_2/amp
md_d12 = v2vel*md_d12/amp
md_c12 = v2vel*md_c12/amp
md_d13 = v2vel*md_d13/amp
md_c13 = v2vel*md_c13/amp

    
if False:
    print('save')
    hdf5_fmt = './{dataname}/Xaxis_{sensor}_{pct}.hdf5'.replace("{dataname}",dataname)
    
    exv_fmt = hdf5_fmt.replace('{sensor}','exv')
    md_0.name = 'exv_x_50pct'
    low_0.name = 'exv_x_5pct'
    high_0.name = 'exv_x_95pct'    
    save(md_0, fname=exv_fmt.format(pct='50pct'),overwrite=True)
    save(low_0, fname=exv_fmt.format(pct='5pct'),overwrite=True)
    save(high_0, fname=exv_fmt.format(pct='95pct'),overwrite=True)
    
    ixv1_fmt = hdf5_fmt.replace('{sensor}','ixv1')    
    md_1.name = 'ixv1_x_50pct'
    low_1.name = 'ixv1_x_5pct'
    high_1.name = 'ixv1_x_95pct'
    save(md_1, fname=ixv1_fmt.format(pct='50pct'),overwrite=True)
    save(low_1, fname=ixv1_fmt.format(pct='5pct'),overwrite=True)
    save(high_1, fname=ixv1_fmt.format(pct='95pct'),overwrite=True)

    ixv2_fmt = hdf5_fmt.replace('{sensor}','ixv2')    
    md_2.name = 'ixv2_x_50pct'
    low_2.name = 'ixv2_x_5pct'
    high_2.name = 'ixv2_x_95pct'
    save(md_2, fname=ixv2_fmt.format(pct='50pct'),overwrite=True)
    save(low_2, fname=ixv2_fmt.format(pct='5pct'),overwrite=True)
    save(high_2, fname=ixv2_fmt.format(pct='95pct'),overwrite=True)    
    
    diff12_fmt = hdf5_fmt.replace('{sensor}','diff12')    
    md_d12.name = 'diff12_x_50pct'
    low_d12.name = 'diff12_x_5pct'
    high_d12.name = 'diff12_x_95pct'
    save(md_d12, fname=diff12_fmt.format(pct='50pct'),overwrite=True)
    save(low_d12, fname=diff12_fmt.format(pct='5pct'),overwrite=True)
    save(high_d12, fname=diff12_fmt.format(pct='95pct'),overwrite=True)    

    comm12_fmt = hdf5_fmt.replace('{sensor}','comm12')    
    md_c12.name = 'comm12_x_50pct'
    low_c12.name = 'comm12_x_5pct'
    high_c12.name = 'comm12_x_95pct'
    save(md_c12, fname=comm12_fmt.format(pct='50pct'),overwrite=True)
    save(low_c12, fname=comm12_fmt.format(pct='5pct'),overwrite=True)
    save(high_c12, fname=comm12_fmt.format(pct='95pct'),overwrite=True)    

    diff13_fmt = hdf5_fmt.replace('{sensor}','diff13')    
    md_d13.name = 'diff13_x_50pct'
    low_d13.name = 'diff13_x_5pct'
    high_d13.name = 'diff13_x_95pct'
    save(md_d13, fname=diff13_fmt.format(pct='50pct'),overwrite=True)
    save(low_d13, fname=diff13_fmt.format(pct='5pct'),overwrite=True)
    save(high_d13, fname=diff13_fmt.format(pct='95pct'),overwrite=True)    

    comm13_fmt = hdf5_fmt.replace('{sensor}','comm13')    
    md_c13.name = 'comm13_x_50pct'
    low_c13.name = 'comm13_x_5pct'
    high_c13.name = 'comm13_x_95pct'
    save(md_c13, fname=comm13_fmt.format(pct='50pct'),overwrite=True)
    save(low_c13, fname=comm13_fmt.format(pct='5pct'),overwrite=True)
    save(high_c13, fname=comm13_fmt.format(pct='95pct'),overwrite=True)
