import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from gwpy.plot import Plot
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert
from glue import lal

#start = tconvert('Dec 25 2018 00:00:54 JST')
start = tconvert('Sep 06 2018 00:00:00 JST')
#end = tconvert('Sep 10 2018 01:00:00 JST')
#end = tconvert('Oct 06 2018 01:00:00 JST')
start = tconvert('Oct 06 2018 00:00:00 JST')
start = tconvert('Nov 06 2018 01:00:00 JST')
start = tconvert('Dec 02 2018 11:00:00 JST')
end = tconvert('Dec 03 2018 07:00:00 JST')
#end = start + 1000
kwargs = {}
kwargs['verbose'] = True
kwargs['format'] = 'gwf.lalframe'
kwargs['start'] = start
kwargs['end'] = end
kwargs['pad'] = np.nan
kwargs['nproc'] = 10

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
chname_3 = ['K1:PEM-IXV_GND_TR120Q_X_IN1_DQ.rms',
            'K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ.rms',
            'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ.rms',
            'K1:PEM-EYV_GND_TR120Q_X_IN1_DQ.rms',
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

source = '../script/mtrend_phase1_xarm.cache'    
source = '../script/full_phase1_xarm.cache'
source = lal.Cache.fromfile(open(source))
#source = '/data/trend/minute/12303/K-K1_M-1230303600-3600.gwf'
chname = chname_3
data = TimeSeriesDict.read(source,chname,**kwargs)

# ----------
data.write('chname3_1.gwf',format='gwf.lalframe')
exit()
data = TimeSeriesDict.read('chname3_1.gwf',chname,**kwargs)
# ----------

labels = [ch.replace('_',' ')for ch in chname]
plot = data.plot(ylim=(-100,100),epoch=start)
ax = plot.gca()
#plot = data.plot()
plot.legend(labels)
plot.savefig('hoge.png')
