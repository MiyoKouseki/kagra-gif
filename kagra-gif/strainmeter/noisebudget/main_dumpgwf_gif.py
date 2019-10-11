
import numpy
from miyopy.gif import findfiles
from gwpy.timeseries import TimeSeries
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert
from gwpy.plot import Plot

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


start = tconvert('May 03 2019 00:00:00 JST')
end   = tconvert('May 03 2019 06:00:00 JST')

# -----------
# Strain
# -----------
if False:
    chname = 'CALC_STRAIN'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/Dropbox/KagraData/gif')
    source = [path for files in segments for path in files]    
    strain = TimeSeries.read(source=source,
                        name=chname,
                        format='gif',
                        pad=numpy.nan,
                        nproc=1)
    strain = TimeSeries(strain.value,times=strain.times.value,name=chname)
    strain = strain.resample(8.0)
    #strain.write('Dec10_3hours_strain.gwf',format='gwf.lalframe')

# -----------
# Pressure
# -----------
if True:
    chname = 'X500_BARO'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/Dropbox/KagraData/gif')
    source = [path for files in segments for path in files]    
    x500_baro = TimeSeries.read(source=source,
                             name=chname,
                             format='gif',
                             pad=numpy.nan,
                             nproc=1)
    x500_baro = TimeSeries(x500_baro.value,times=x500_baro.times.value,name=chname)
    print x500_baro.name
    x500_baro = x500_baro.resample(8.0)
    x500_baro.write('2019May03_6hours_x500_press.gwf',format='gwf.lalframe')    
    #
    chname = 'X2000_BARO'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/Dropbox/KagraData/gif')
    source = [path for files in segments for path in files]    
    x2000_baro = TimeSeries.read(source=source,
                             name=chname,
                             format='gif',
                             pad=numpy.nan,
                             nproc=1)
    x2000_baro = TimeSeries(x2000_baro.value,times=x2000_baro.times.value,name=chname)
    print x2000_baro.name
    x2000_baro = x2000_baro.resample(8.0)
    x2000_baro.write('2019May03_6hours_x2000_press.gwf',format='gwf.lalframe')    
    
