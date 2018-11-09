import sys
sys.path.insert(0,'/Users/miyo/Dropbox/Git/gwpy/')
sys.path.insert(0,'/Users/miyo/Dropbox/Git/miyopy/')
#print sys.path

import numpy
from astropy import units as u 
import matplotlib.pyplot as plt

from gwpy.timeseries import TimeSeries

from miyopy.gif import (GifData,KagraStrain)#,gps2datestr)
from gwpy.plot import Plot

start = 1223996418-3600*24*4
tlen = 3600*24*5
end = start + tlen
#
# -- kagra gif x -----------------------
segments = GifData.findfiles(start,tlen,'CALC_STRAIN',
                             prefix='/Users/miyo/Dropbox/KagraData/gif/')
allfiles = [path for files in segments for path in files]
strain = TimeSeries.read(source=allfiles,
                         name='CALC_STRAIN',
                         format='gif',
                         pad=numpy.nan,
                         nproc=2)
strain = strain.detrend('linear')
#
# -- gotic -------------
gifx = KagraStrain(start,end).x
gifx = gifx.detrend('linear')
gifx = gifx*0.9
#
# -- plot  -----------------------
print(gifx)
print(strain)
#plot = gifx.plot()
plot = Plot(gifx,strain,xscale='auto-gps')
#plot.auto_gps_label()
#plot.legend()
plot.subplots_adjust(right=.86)
plot.savefig('x_.png')
plot.close()
