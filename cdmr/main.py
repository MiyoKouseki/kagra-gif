import matplotlib
matplotlib.use('Agg')
import numpy as np
from gwpy.plot import Plot
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert
from glue import lal

#start = tconvert('Dec 25 2018 00:00:54 JST')
start = tconvert('Dec 05 2018 00:00:00 JST')
end = tconvert('Jan 20 2018 00:00:00 JST')
#end = tconvert('Jan 10 2019 01:00:00 JST')

kwargs = {}
kwargs['verbose'] = True
#kwargs['format'] = 'gwf.lalframe'
kwargs['start'] = start
kwargs['end'] = end
kwargs['pad'] = np.nan
kwargs['nproc'] = 100
# Old Name (XarmComiss)
#channels = ['K1:PEM-IXV_SEIS_WE_SENSINF_OUT_DQ.rms',
#            'K1:PEM-IXV_SEIS_WE_SENSINF_OUT_DQ.rms',
#            'K1:PEM-EXV_SEIS_WE_SENSINF_OUT_DQ.rms',
#            ]
# Old Name (bKAGRAph1)
chname_2 = ['K1:PEM-IXV_GND_TR120Q_X_IN1_DQ.rms',
            'K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ.rms',
            'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ.rms',
            'K1:PEM-IMC_GND_TR120C_MCE_X_IN1_DQ.rms'
            'K1:PEM-IMC_GND_TR120C_MCI_X_IN1_DQ.rms'
            ]

source = '../script/hogetr.cache'    
source = lal.Cache.fromfile(open(source))
#source = '/data/trend/minute/12303/K-K1_M-1230303600-3600.gwf'
print chname_2
data = TimeSeriesDict.read(source,chname_2,**kwargs)
print data
#plot = data.plot(ylim=(0,3))
plot = data.plot(ylim=(0,200))
plot.savefig('hoge.png')
