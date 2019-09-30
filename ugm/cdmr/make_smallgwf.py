from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np

chname3_x = [
    'K1:PEM-IXV_GND_TR120Q_X_IN1_DQ',
    'K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ',
    'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ',
    'K1:PEM-EYV_GND_TR120Q_X_IN1_DQ',
    ]
chname4_x = [
    'K1:PEM-SEIS_IXV_GND_X_OUT_DQ',
    'K1:PEM-SEIS_EXV_GND_X_OUT_DQ',
    'K1:PEM-SEIS_EYV_GND_X_OUT_DQ',
    ]
chname4_x = [
    'K1:PEM-SEIS_IXV_GND_EW_IN1_DQ',
    'K1:PEM-SEIS_EXV_GND_EW_IN1_DQ',
    'K1:PEM-SEIS_EYV_GND_EW_IN1_DQ',
    ]


import argparse 
parser = argparse.ArgumentParser(description='description')
parser.add_argument('dataname', help='help')
parser.add_argument('--Plot')
args = parser.parse_args()

dataname = args.dataname
if dataname == 'chname3_1':
    start = tconvert('Dec 02 2018 11:00:00')
    end = start + 2**16
    chname = chname3_x
elif dataname == 'chname3_2':
    start = tconvert('Jan 01 2019 04:00:00')
    end = start + 2**16
    chname = chname3_x    
elif dataname == 'chname3_3':
    start = tconvert('Jan 02 2019 00:00:00')
    end = start + 2**16
    chname = chname3_x    
elif dataname == 'chname4_1':
    start = tconvert('May 31 2019 00:00:00')
    end = start + 2**16
    chname = chname4_x
elif dataname == 'chname4_2':
    start = tconvert('Jun 2 2019 00:00:00')
    end = start + 2**16
    chname = chname4_x
elif dataname == 'chname4_3':
    start = tconvert('Jun 4 2019 00:00:00')
    end = start + 2**16
    chname = chname4_x            
else:
    raise ValueError('Invalid data name')



xaxis = True
make_gwf = True
nds = True
if make_gwf and xaxis:
    smallgwf_fname = './{dataname}/X.gwf'.format(dataname=dataname)
    if nds:
        data = TimeSeriesDict.fetch(chname,start,end,
                                   host='10.68.10.121',port=8088,verbose=True)
    else:
        data = TimeSeriesDict.read('./m31/{dataname}.gwf'.format(dataname=dataname),
                                chname,
                                verbose=True,
                                format='gwf.lalframe',
                                start=start,
                                end=end,
                                pad=np.pad,
                                )
    for d in data.values():
        d.override_unit('ct')
    
    data.write(smallgwf_fname)
    print('Wrote {0}'.format(smallgwf_fname))
