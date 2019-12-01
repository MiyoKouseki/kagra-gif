#
#! coding:utf-8
__author__ = 'Koseki Miyo'

from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.spectrogram import Spectrogram
import matplotlib.pyplot as plt
import numpy as np
import Kozapy.utils.filelist as existedfilelist


def nan_helper(y):
    #return np.isnan(y), lambda z: z.nonzero()[0]
    diff = np.diff(y)
    ans = diff > 1e-8
    ans = y==0.0
    return ans, lambda z: z.nonzero()[0]


start = tconvert('Nov 18 2019 00:00:00 JST')
end   = tconvert('Nov 21 2019 00:00:00 JST')
start = tconvert('Oct 01 2019 00:00:00 JST')
end   = tconvert('Nov 01 2019 00:00:00 JST')
chname = ['K1:GIF-X_STRAIN_OUT_DQ.mean']
fnamelist = existedfilelist(start,end,trend='second')
print(fnamelist)
#data = TimeSeriesDict.read(fnamelist,chname,nproc=8,pad=0.0)
data = TimeSeriesDict.read(fnamelist,chname,nproc=8,pad=np.nan)
#data = data.resample(32)
#data = data.crop(start,end)
gif = data['K1:GIF-X_STRAIN_OUT_DQ.mean']
# _x,_y = gif.times,gif.value
# nans, x = nan_helper(_y)
# print(True in nans)
# y = _y
# y[nans] = np.interp(x(nans), x(~nans), y[~nans])
# plt.plot(_x,y)
# #plt.plot(_x[nans],y[nans])
# plt.savefig('hoge.png')
# plt.close()
#exit()
plot = gif.plot(ylim=(-1e-7,1e-7))
plot.savefig('hoge.png')
plot.close()
asd = gif.asd(fftlength=2**17,overlap=2**16)
#asd = gif.asd(fftlength=2**10,overlap=2**9)
plot = asd.plot()
plot.savefig('huge_.png')
plot.close()
