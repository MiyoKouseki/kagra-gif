import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

from gwpy.plot import Plot
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert
from glue import lal
import sys
sys.path.insert(0,'../../miyopy')
from gwpy.frequencyseries import FrequencySeries
from astropy import units as u
from miyopy.types import SeismoMeter

'''
chname3_1.gwf data contains these bellow channels in JST Dec02 11:00 - Dec03 07.
chname3 list;
'K1:PEM-IXV_GND_TR120Q_X_IN1_DQ',
'K1:PEM-IXV_GND_TR120Q_Y_IN1_DQ',
'K1:PEM-IXV_GND_TR120Q_Z_IN1_DQ',
'K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ',
'K1:PEM-IXV_GND_TR120QTEST_Y_IN1_DQ',
'K1:PEM-IXV_GND_TR120QTEST_Z_IN1_DQ',
'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ',
'K1:PEM-EXV_GND_TR120Q_Y_IN1_DQ',
'K1:PEM-EXV_GND_TR120Q_Z_IN1_DQ',
'K1:PEM-EYV_GND_TR120Q_X_IN1_DQ',
'K1:PEM-EYV_GND_TR120Q_Y_IN1_DQ',
'K1:PEM-EYV_GND_TR120Q_Z_IN1_DQ'

chname3_1_X.gwf data contains only X axis.

'''


# -------------------------------

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

# ---------------------------------



pfx = '/Users/miyo/KagraData/gif/'
from miyopy.gif.datatype import GifData
start = tconvert('Dec 02 2018 11:00:00')
end = tconvert('Dec 03 2018 07:00:00')
end = start + 2**16
#end = 'Dec 02 2018 11:01:00'




if __name__ == '__main__':
    # read from data
    if False:
        x1500_ew = read_gif('X1500_TR240posEW',start,end,write=True)
        x1500_ns = read_gif('X1500_TR240posNS',start,end,write=True)
        x1500_ud = read_gif('X1500_TR240posUD',start,end,write=True)
        strain = read_gif('CALC_STRAIN',start,end,write=True)
        x1500_ew.write('./chname3_1_X_x1500_ew.gwf',format='gwf.lalframe')
        x1500_ns.write('./chname3_1_X_x1500_ns.gwf',format='gwf.lalframe')
        x1500_ud.write('./chname3_1_X_x1500_ud.gwf',format='gwf.lalframe')
        strain.write('./chname3_1_X_strain.gwf',format='gwf.lalframe')
        print('wrote')
        #exit()
    
    if True:
        x1500_ew = TimeSeries.read('chname3_1_X_x1500_ew.gwf',
                                   'X1500_TR240posEW',
                                    format='gwf.lalframe')
        x1500_ns = TimeSeries.read('chname3_1_X_x1500_ns.gwf',
                                   'X1500_TR240posNS',
                                    format='gwf.lalframe')
        x1500_ud = TimeSeries.read('chname3_1_X_x1500_ud.gwf',
                                   'X1500_TR240posUD',
                                    format='gwf.lalframe')
        strain = TimeSeries.read('chname3_1_X_strain.gwf',
                                   'CALC_STRAIN',
                                    format='gwf.lalframe')        
        #print(strain)
    # rotate
    x1500 = SeismoMeter(x1500_ew, x1500_ns, x1500_ud)   
    x1500.rotate(-30)
    x1500_x = x1500.x

    # write
    if True:
        x1500_x.write('./chname3_1_X_x1500.gwf',format='gwf.lalframe')
        strain.write('./chname3_1_X_strain.gwf',format='gwf.lalframe')
    
    if True:
        x1500_x = TimeSeries.read('chname3_1_X_x1500.gwf',
                                   'X1500_TR240posEW',
                                    format='gwf.lalframe')
        strain = TimeSeries.read('chname3_1_X_strain.gwf',
                                 'CALC_STRAIN',
                                     format='gwf.lalframe')
        
    # calc asd
    median_x1500, low_x1500, high_x1500 = calc_asd(x1500_x)
    median_strain, low_strain, high_strain = calc_asd(strain)

    
    # save as hdf5
    save(median_x1500, fname='./chname3_1_X_x1500_50pct.hdf5')
    save(low_x1500, fname='./chname3_1_X_x1500_5pct.hdf5')
    save(high_x1500, fname='./chname3_1_X_x1500_95pct.hdf5')    

    save(median_strain, fname='./chname3_1_X_strain_50pct.hdf5')
    save(low_strain, fname='./chname3_1_X_strain_5pct.hdf5')
    save(high_strain, fname='./chname3_1_X_strain_95pct.hdf5')    
