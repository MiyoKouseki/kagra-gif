
from miyopy.gif.datatype import GifData
from gwpy.time import tconvert

start = tconvert('Sep 16 2019 20:26:00 UTC')
end = tconvert('Sep 16 2019 21:00:00 UTC')
chname = 'CALC_STRAIN'
gif = GifData('CALC_STRAIN')
files = gif.findfiles(start,end,chname)
print(files)
