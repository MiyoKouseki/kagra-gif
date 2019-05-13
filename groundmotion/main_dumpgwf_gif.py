
import numpy
from miyopy.gif import findfiles
from gwpy.timeseries import TimeSeries
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert
from gwpy.plot import Plot

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


start = tconvert('Dec 10 2018 00:00:00 UTC')
end   = tconvert('Dec 14 2018 00:00:00 UTC')

chname = 'CALC_STRAIN'
segments = findfiles(start,end,chname,prefix='/Users/miyo/Dropbox/KagraData/gif')
source = [path for files in segments for path in files]    
strain = TimeSeries.read(source=source,
                       name=chname,
                       format='gif',
                       pad=numpy.nan,
                       nproc=1)
#strain =  strain.crop(strain.t0.value,strain.t0.value+0.04)
strain = TimeSeries(strain.value,times=strain.times.value,name=chname)
print strain.value.shape[0]/200,'sec'
strain = strain.resample(8.0)
#strain.write('Dec10_3hours_strain.gwf',format='gwf.lalframe')
#strain.write('Dec10_24hours_strain.gwf',format='gwf.lalframe')
strain.write('Dec10_4days_strain.gwf',format='gwf.lalframe')
print strain.value.shape[0]/8,'sec'
