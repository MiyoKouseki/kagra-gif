'''Read timeseries from gwffile
'''

'''Read timeseriese from gwffile.
'''

__author__ = "Koseki Miyo"

import matplotlib
matplotlib.use('Agg')


from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.time import tconvert

chname = [
    #'K1:GIF-X_STRAIN_IN1_DQ.mean',
    'K1:PEM-WEATHER_IXV_FIELD_PRES_OUT16.mean'
]

start = tconvert('May 03 2019 00:00:00 JST')
end   = tconvert('May 03 2019 01:00:00 JST')
nproc = 1 

# Read Data
cache = True
dump = False
if cache and not dump:
    print('Read using cache')
    from glue import lal
    from pylal import frutils
    cachefname = './trend_2019_May01-May14.cache'
    source = lal.Cache.fromfile(open(cachefname))
    print('Read ')
    data = TimeSeriesDict.read(source,chname,start=start,end=end,format='gwf.lalframe',nproc=nproc)
    print data
elif dump:
    print('Read using dumped gwf file')
    source = 'dump.gwf'
    data = TimeSeriesDict.read(source,chname,start=start,end=end,format='gwf.lalframe')
else:
    print('Read using single gwf full file')
    #source = 'K-K1_C-1231133824-32.gwf'
    #source = '/data/full/12284/K-K1_C-1228435200-32.gwf'
    #source = '/data/full/12407/K-K1_C-1240758016-32.gwf'
    source = '/data/trend/minute/12407/K-K1_M-1240758000-3600.gwf'
    data = TimeSeriesDict.read(source,chname,format='gwf.lalframe')
    print data
    
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

