pfx = '/Users/miyo/KagraData/gif/'
from miyopy.gif.datatype import GifData
from gwpy.timeseries import TimeSeriesDict,TimeSeries
import numpy as np

def read_gif(chname,start,end,write=False):    
    segments = GifData.findfiles(start,end,chname,prefix=pfx)
    allfiles = [path for files in segments for path in files]    
    data = TimeSeries.read(source=allfiles,
                            name=chname,
                            format='gif',
                            pad=np.nan,
                            nproc=2)
    data.name = chname
    return data
        
def calc_asd(ts, fftlength=2**10):
    sg = ts.spectrogram2(fftlength=fftlength,
                         overlap=fftlength/2.,
                             window='hanning') ** (1/2.)
    median_0,low_0,high_0 = sg.percentile(50), sg.percentile(5), sg.percentile(95)
    return median_0,low_0,high_0

def save(data,fname='tmp.hdf5'):
    data.write(fname,format='hdf5')
