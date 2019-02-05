from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
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



xaxis = True
make_gwf = True
if make_gwf and xaxis:
    smallgwf_fname = './{dataname}/X.gwf'.format(dataname=dataname)
    
    chname3_x = [
        'K1:PEM-IXV_GND_TR120Q_X_IN1_DQ',
        'K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ',
        'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ',
        'K1:PEM-EYV_GND_TR120Q_X_IN1_DQ',
        ]
    data = TimeSeriesDict.read('./m31/{dataname}.gwf'.format(dataname=dataname),
                               chname3_x,
                               verbose=True,
                               format='gwf.lalframe',
                               start=start,
                               end=end,
                               pad=np.pad,
                               )
    data.write(smallgwf_fname)
    print('Wrote {0}'.format(smallgwf_fname))
