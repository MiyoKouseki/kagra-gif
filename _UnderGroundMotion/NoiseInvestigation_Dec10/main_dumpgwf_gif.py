
import numpy
from miyopy.gif import findfiles
from gwpy.timeseries import TimeSeries
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert
from gwpy.plot import Plot

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


start = tconvert('Dec 10 2018 00:00:00 UTC')
end   = tconvert('Dec 10 2018 03:00:00 UTC')

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
    strain.write('Dec10_3hours_strain.gwf',format='gwf.lalframe')

# -----------
# Pressure
# -----------
if True:
    chname = 'X500_BARO'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/Dropbox/KagraData/gif')
    source = [path for files in segments for path in files]    
    strain = TimeSeries.read(source=source,
                             name=chname,
                             format='gif',
                             pad=numpy.nan,
                             nproc=1)
    x500_baro = TimeSeries(x500_baro.value,times=x500_baro.times.value,name=chname)
    x500_baro = x500_baro.resample(8.0)
    x500_baro.write('Dec10_3hours_x500_baro.gwf',format='gwf.lalframe')
    
