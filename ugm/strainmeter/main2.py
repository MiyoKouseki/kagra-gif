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
    gif = TimeSeries.read('gif_Sep17.gwf','CALC_STRAIN')*3000*1e-6
    fnamelist = existedfilelist(start,end,trend='full')
    c = 299792458 # m/sec
    lam = 1064e-9 # m
    xarm = TimeSeries.read(fnamelist,'K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16')*3000.0/(c/lam)*1e6 # [um]

fig,ax = plt.subplots(2,1,figsize=(10,10))
ax[0].plot(gif)
ax[0].set_ylim(-10,10)
ax[0].set_xscale('auto-gps')
ax[1].plot(xarm)
ax[1].set_xscale('auto-gps')
ax[1].set_ylim(-24,-14)
plt.savefig('gif.png')
plt.close()
