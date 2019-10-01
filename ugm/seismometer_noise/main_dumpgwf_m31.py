'''Read timeseries from gwffile
'''

'''Read timeseriese from gwffile.
'''

__author__ = "Koseki Miyo"

import matplotlib
matplotlib.use('Agg')


from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert

chname = [
    'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ',
    'K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ',
    'K1:PEM-EXV_GND_TR120Q_X_OUT_DQ',
]
start = tconvert('Dec 10 2018 00:00:00')
end = tconvert('Dec 10 2018 03:00:00')

nproc = 10

# Read Data
cache = True
dump = False
if cache and not dump:
    print('Read using cache')
    from glue import lal
    from pylal import frutils
    cachefname = './full_2018_Dec10-Dec20.cache'
    source = lal.Cache.fromfile(open(cachefname))
    data = TimeSeriesDict.read(source,chname,start=start,end=end,format='gwf.lalframe',nproc=nproc)
elif dump:
    print('Read using dumped gwf file')
    source = 'dump.gwf'
    data = TimeSeriesDict.read(source,chname,start=start,end=end,format='gwf.lalframe')
else:
    print('Read using single gwf full file')
    source = 'K-K1_C-1231133824-32.gwf'
    source = '/data/full/12284/K-K1_C-1228435200-32.gwf'
    data = TimeSeries.read(source,chname,format='gwf.lalframe')    

# some treatment
#data.override_unit('um/s') # bugs when use lalframe reader


# plot
plot = True
if plot:
    plot = data.plot()
    plot.savefig('result_timeseries.png')
    plot.close()

# Write
write = True
if write == True:
    data.write('dump.gwf',format='gwf.lalframe')
    
