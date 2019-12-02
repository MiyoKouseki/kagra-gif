from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.spectrogram import Spectrogram
import matplotlib.pyplot as plt
import numpy as np
import Kozapy.utils.filelist as existedfilelist

from miyopy.gif.datatype import GifData
from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries

start = tconvert('Sep 16 2019 20:26:00 UTC')
end = tconvert('Sep 16 2019 21:00:00 UTC')
if False:
    chname = 'CALC_STRAIN'
    gif = GifData('CALC_STRAIN')
    files = gif.findfiles(start,end,chname,prefix = '/Users/miyo/Dropbox/KagraData/gif/')[0]
    #print(files)
    data = TimeSeries.read(files,name='CALC_STRAIN',format='gif')
    data = data.crop(start,end)
    data = data.resample(16)
    data.name = 'CALC_STRAIN'
    data.write('gif_Sep17.gwf')
else:
    gif = TimeSeries.read('gif_Sep17.gwf','CALC_STRAIN')
    fnamelist = existedfilelist(start,end,trend='full')
    xarm = TimeSeries.read(fnamelist,'K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16')

fig,ax = plt.subplots(2,1,figsize=(10,10))
ax[0].plot(gif)
ax[1].plot(xarm)
plt.savefig('gif.png')
plt.close()
