import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from gwpy.plot import Plot
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert
from glue import lal

if False:
    start = tconvert('Jan 01 2019 04:00:00 JST')
    end   = tconvert('Jan 02 2019 00:01:00 JST')
    fname = 'MEAN_Jan0104hJan0200h.png'
else:
    start = tconvert('Jan 02 2019 00:01:00 JST')
    end   = tconvert('Jan 02 2019 20:01:00 JST')
    fname = 'MEAN_Jan0200hJan0220h.png'

kwargs = {}
kwargs['verbose'] = True
kwargs['format'] = 'gwf.lalframe'
kwargs['start'] = start
kwargs['end'] = end
kwargs['pad'] = np.nan
kwargs['nproc'] = 28

# Old Name (XarmComiss)
chname_0 = ['K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ.rms',
            'K1:PEM-EYV_SEIS_WE_SENSINF_IN1_DQ.rms',
            'K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ.rms'
]

chname_1 = ['K1:PEM-EXV_SEIS_Z_SENSINF_IN1_DQ.rms',
            'K1:PEM-EYV_SEIS_Z_SENSINF_IN1_DQ.rms',
            'K1:PEM-IXV_SEIS_Z_SENSINF_IN1_DQ.rms',
            'K1:PEM-IXV_SEIS_TEST_Z_SENSINF_IN1_DQ.rms',
]

chname_2 = ['K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ.rms',
            'K1:PEM-EYV_SEIS_WE_SENSINF_IN1_DQ.rms',
            'K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ.rms',
            'K1:PEM-IXV_SEIS_TEST_WE_SENSINF_IN1_DQ.rms',
]

# Old Name (bKAGRAph1)
chname_3 = ['K1:PEM-IXV_GND_TR120Q_X_IN1_DQ.mean',
            'K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ.mean',
            'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ.mean',
            'K1:PEM-EYV_GND_TR120Q_X_IN1_DQ.mean',
            #'K1:PEM-IMC_GND_TR120C_MCE_X_IN1_DQ.rms',
            #'K1:PEM-IMC_GND_TR120C_MCI_X_IN1_DQ.rms'
            ]


chname_3 = ['K1:PEM-IXV_GND_TR120Q_X_IN1_DQ',
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
            'K1:PEM-EYV_GND_TR120Q_Z_IN1_DQ',
            #'K1:PEM-IMC_GND_TR120C_MCE_X_IN1_DQ.rms',
            #'K1:PEM-IMC_GND_TR120C_MCI_X_IN1_DQ.rms'
            ]



#source = '../../script/mtrend_phase1_xarm.cache'    
source = '../../script/full_phase1_xarm.cache'
source = lal.Cache.fromfile(open(source))
chname = chname_3
data = TimeSeriesDict.read(source,chname,**kwargs)
print('read data.')

if True:
    data.write('chname3_3.gwf',format='gwf.lalframe')
    exit()
    #data = TimeSeriesDict.read('chname3_1.gwf',chname,**kwargs)


labels = [ch.replace('_',' ')for ch in chname]
plot = data.plot(ylim=(-100,100),epoch=start)
ax = plot.gca()
#plot = data.plot()
plot.legend(labels)
plot.savefig(fname)
