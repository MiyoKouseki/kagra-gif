from miyopy.gif.datatype import GifData
from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries

start = tconvert('Sep 16 2019 20:26:00 UTC')
end = tconvert('Sep 16 2019 21:00:00 UTC')
chname = 'CALC_STRAIN'
gif = GifData('CALC_STRAIN')
files = gif.findfiles(start,end,chname,prefix = '/Users/miyo/Dropbox/KagraData/gif/')[0]
#print(files)
data = TimeSeries.read(files,name='CALC_STRAIN',format='gif')
data = data.crop(start,end)
data = data.resample(16)
data.name = 'CALC_STRAIN'
print(data)
data.write('gif_Sep17.gwf')
plot = data.plot()
plot.savefig('gif.png')
plot.close()
