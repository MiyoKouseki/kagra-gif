#
#! coding:utf-8
__author__ = 'Koseki Miyo'

from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.spectrogram import Spectrogram

import Kozapy.utils.filelist as existedfilelist

start = tconvert('Nov 13 2019 00:00:00 JST')
start = tconvert('Nov 16 2019 00:00:00 JST')
end   = tconvert('Nov 20 2019 00:00:00 JST')
end   = tconvert('Nov 16 2019 03:00:00 JST')
chname = ['K1:GIF-X_STRAIN_OUT_DQ.mean']
fnamelist = existedfilelist(start,end,trend='minute')
print(fnamelist)
data = TimeSeriesDict.read(fnamelist,chname,nproc=8,pad=0.0)
#data = data.resample(32)
#data = data.crop(start,end)
plot = data.plot()
plot.savefig('hoge.png')
plot.close()
gif = data['K1:GIF-X_STRAIN_OUT_DQ.mean']
asd = gif.asd(fftlength=2**14,overlap=2**13)
plot = asd.plot()
plot.savefig('huge.png')
plot.close()
