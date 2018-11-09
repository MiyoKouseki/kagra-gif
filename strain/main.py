import sys
sys.path.insert(0,'/Users/miyo/Dropbox/Git/gwpy/')
sys.path.insert(0,'/Users/miyo/Dropbox/Git/miyopy/')
#print sys.path

import numpy
from astropy import units as u 
import matplotlib.pyplot as plt

from gwpy.timeseries import TimeSeries

from miyopy.gif import (GifData,KagraGoticStrain,gps2datestr)
from gwpy.plot import Plot

start = 1223996418-3600*24*4
start = 1223996418
tlen = 3600*24 - 60
end = start + tlen

# gif data
segments = GifData.findfiles(start,end,'CALC_STRAIN',prefix='/Users/miyo/Dropbox/KagraData/gif/') # segment is not support in gwpy.timeseries.read
allfiles = [path for files in segments for path in files] 
strain = TimeSeries.read(source=allfiles,
                         name='CALC_STRAIN',
                         format='gif',
                         pad=numpy.nan,
                         nproc=2)
strain = strain.detrend('linear')


# gotic data
gifx = KagraGoticStrain(start,end).x
gifx = gifx.detrend('linear')
gifx = gifx*0.9 


#plot = gifx.plot()
plot = Plot(gifx,strain,xscale='auto-gps')
plot.legend()
plot.subplots_adjust(right=.86)
plot.savefig('x_.png')
plot.close()
