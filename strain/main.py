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

import warnings
warnings.filterwarnings("ignore")
# because scipy/signal/signaltools.py omit warning .


def main_compare_gif_gotic2():
    start = 'Oct 15 2018 00:00:00'
    end = 'Oct 21 2018 00:00:00'

    # gif data
    pfx = '/Users/miyo/Dropbox/KagraData/gif/'
    segments = GifData.findfiles(start,end,'CALC_STRAIN',prefix=pfx)
    allfiles = [path for files in segments for path in files]
    strain = TimeSeries.read(source=allfiles,
                             name='CALC_STRAIN',
                             format='gif',
                             pad=numpy.nan,
                             nproc=2)
    strain = strain.detrend('linear')


    
    # gotic data
    source = '201805010000_201811010000.gotic'
    gifx = KagraGoticStrain.read(source,start=start,end=end).x
    gifx = gifx.detrend('linear')
    gifx = gifx*0.9 

    
    # plot 
    plot = Plot(gifx,strain,xscale='auto-gps')
    plot.legend()
    plot.subplots_adjust(right=.86)
    plot.savefig('result.png')
    plot.close()


if __name__ == '__main__':
    main_compare_gif_gotic2()
