
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert

import sys
sys.path.insert(0,'../../miyopy')
from miyopy.types import SeismoMeter
from miyopy.utils.trillium import Trillium
from utils import read_gif, calc_asd, save

import numpy as np

import argparse 
parser = argparse.ArgumentParser(description='description')
parser.add_argument('dataname', help='help')
parser.add_argument('--Plot')
args = parser.parse_args()


dataname = args.dataname
if dataname == 'chname3_1':
    start = tconvert('Dec 02 2018 11:00:00')
    end = start + 2**16
elif dataname == 'chname3_2':
    start = tconvert('Jan 01 2019 04:00:00')
    end = start + 2**16
elif dataname == 'chname3_3':
    start = tconvert('Jan 02 2019 00:00:00')
    end = start + 2**16
else:
    raise ValueError('Invalid data name')



if __name__ == '__main__':
    # read from data
    gwf_fmt = './{dataname}/Xaxis_{sensor}.gwf'.replace("{dataname}",dataname)
    _gwf_fmt = './{dataname}/{sensor}.gwf'.replace("{dataname}",dataname)

    
    if True:
        x1500_ew = read_gif('X1500_TR240posEW',start,end,write=True)
        x1500_ns = read_gif('X1500_TR240posNS',start,end,write=True)
        x1500_ud = read_gif('X1500_TR240posUD',start,end,write=True)
        strain = read_gif('CALC_STRAIN',start,end,write=True)
        print('read')
        x1500_ew.write(_gwf_fmt.format(sensor='x1500_ew'),format='gwf.lalframe')
        x1500_ns.write(_gwf_fmt.format(sensor='x1500_ns'),format='gwf.lalframe')
        x1500_ud.write(_gwf_fmt.format(sensor='x1500_ud'),format='gwf.lalframe')
        strain.write(gwf_fmt.format(sensor='strain'),format='gwf.lalframe')        
        print('wrote')
        #exit()        
    else:
        x1500_ew = TimeSeries.read(_gwf_fmt.format(sensor='x1500_ew'),
                                   'X1500_TR240posEW',
                                    format='gwf.lalframe')
        x1500_ns = TimeSeries.read(_gwf_fmt.format(sensor='x1500_ns'),
                                   'X1500_TR240posNS',
                                    format='gwf.lalframe')
        x1500_ud = TimeSeries.read(_gwf_fmt.format(sensor='x1500_ud'),
                                   'X1500_TR240posUD',
                                    format='gwf.lalframe')
        strain = TimeSeries.read(gwf_fmt.format(sensor='strain'),
                                   'CALC_STRAIN',
                                    format='gwf.lalframe')
        
    if True:
        # rotate
        x1500 = SeismoMeter(x1500_ew, x1500_ns, x1500_ud)   
        x1500.rotate(-30)
        x1500_x = x1500.x        
        x1500_x.write(gwf_fmt.format(sensor='x1500'),format='gwf.lalframe')
        print('write')
    else:
        x1500_x = TimeSeries.read(gwf_fmt.format(sensor='x1500'),
                                   'X1500_TR240posEW',
                                    format='gwf.lalframe')
        strain = TimeSeries.read(gwf_fmt.format(sensor='strain'),
                                 'CALC_STRAIN',
                                  format='gwf.lalframe')
        print('read')
        
    # calc asd
    x1500_x.name = 'x1500'
    strain.name = 'strain'
    median_x1500, low_x1500, high_x1500 = calc_asd(x1500_x)
    median_strain, low_strain, high_strain = calc_asd(strain)
    print('calc asd')

    # calib
    tr240 = Trillium('240')
    median_x1500 = tr240.v2vel(median_x1500)/2.0
    low_x1500    = tr240.v2vel(low_x1500)/2.0
    high_x1500   = tr240.v2vel(high_x1500)/2.0    
    median_strain = median_strain
    low_strain = low_strain
    high_strain = high_strain
    
    # save as hdf5
    hdf5_fmt = './{dataname}/Xaxis_{sensor}_{pct}.hdf5'.replace("{dataname}",dataname)
    x1500_fmt = hdf5_fmt.replace("{sensor}",'x1500')
    save(median_x1500, fname=x1500_fmt.format(pct='50pct'))
    save(low_x1500, fname=x1500_fmt.format(pct='5pct'))
    save(high_x1500, fname=x1500_fmt.format(pct='95pct'))    
    strain_fmt = hdf5_fmt.replace("{sensor}",'strain')
    save(median_strain, fname=strain_fmt.format(pct='50pct'))
    save(low_strain, fname=strain_fmt.format(pct='5pct'))
    save(high_strain, fname=strain_fmt.format(pct='95pct'))   
