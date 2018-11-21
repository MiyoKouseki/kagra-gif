
import numpy
from miyopy.gif import GifData
from gwpy.timeseries import TimeSeries

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__=='__main__':
    start = 'Nov 20 2018 15:00:00' # UTC
    end = 'Nov 20 2018 23:00:00' # UTC
    #chname = 'CALC_STRAIN'
    chname = 'X1500_15'
    segments = GifData.findfiles(start,end,chname,
                                 prefix='/Users/miyo/Dropbox/KagraData/gif/')
    source = [path for files in segments for path in files]

    x500_baro = TimeSeries.read(source=source,
                                name=chname,
                                format='gif',
                                pad=numpy.nan,
                                nproc=2)
    print x500_baro
    plot = x500_baro.plot()
    plot.savefig('hoge.png')
