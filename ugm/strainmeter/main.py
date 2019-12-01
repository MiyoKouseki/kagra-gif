#
#! coding:utf-8
__author__ = 'Koseki Miyo'

from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.spectrogram import Spectrogram

import Kozapy.utils.filelist as existedfilelist

start = tconvert('Nov 10 2019 00:00:00 JST')
end   = tconvert('Dec 01 2019 00:01:00 JST')
chname = ['K1:GIF-X_STRAIN_OUT_DQ.mean']
fnamelist = existedfilelist(start,end,trend='second')
print(fnamelist)
data = TimeSeriesDict.read(fnamelist,chname,nproc=8,pad=0.0)
#data = data.resample(32)
#data = data.crop(start,end)
plot = data.plot()
plot.savefig('hoge.png')
plot.close()
