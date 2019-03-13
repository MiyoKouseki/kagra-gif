
import numpy
from miyopy.gif import findfiles
from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__=='__main__':
    start = tconvert('Feb 25 2019 15:00:00') # UTC
    end = tconvert('Feb 25 2019 15:02:00') # UTC
    chname = 'PD_PWAVE_PXI01_50k'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/KagraData/gif')
    source = [path for files in segments for path in files]

    x500_baro = TimeSeries.read(source=source,
                                name=chname,
                                format='gif',
                                pad=numpy.nan,
                                nproc=1)
    print x500_baro
    plot = x500_baro.plot()
    plot.savefig('hoge.png')
    
