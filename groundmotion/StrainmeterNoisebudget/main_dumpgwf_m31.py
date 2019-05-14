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
    'K1:PEM-SEIS_IXV_GND_X_OUT_DQ',
    'K1:PEM-SEIS_EXV_GND_X_OUT_DQ',
    'K1:GIF-X_STRAIN_OUT16',
]
start = tconvert('May 03 2019 00:00:00 JST')
end   = tconvert('May 03 2019 06:00:00 JST')
nproc = 10

# Read Data
cache = True
dump = False
if cache and not dump:
    print('Read using cache')
    from glue import lal
    from pylal import frutils
    cachefname = './full_2018_May01-May14.cache'
    source = lal.Cache.fromfile(open(cachefname))
    data = TimeSeriesDict.read(source,chname,start=start,end=end,format='gwf.lalframe',nproc=nproc)
elif dump:
    print('Read using dumped gwf file')
    source = 'dump.gwf'
    data = TimeSeriesDict.read(source,chname,start=start,end=end,format='gwf.lalframe')
else:
    print('Read using single gwf full file')
    #source = 'K-K1_C-1231133824-32.gwf'
    source = '/data/full/12284/K-K1_C-1228435200-32.gwf'
    source = '/data/full/12407/K-K1_C-1240758016-32.gwf'
    data = TimeSeries.read(source,chname[0],format='gwf.lalframe')
    print tconvert(tconvert(data.t0))
    
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
