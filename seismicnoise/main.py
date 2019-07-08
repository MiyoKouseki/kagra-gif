#
#! coding:utf-8
__author__ = 'Koseki Miyo'

import warnings
warnings.filterwarnings('ignore')

from gwpy.segments import SegmentList
from gwpy.time import tconvert
from lib.plot import plot_timeseries,plot_segmentlist,plot_averaged_asd
from lib.segment import divide_segmentlist,random_segments,read_segmentlist
from lib.utils import save_spectrogram, save_longterm_spectrogram, save_asd

import lib.logger
log = lib.logger.Logger('main')

from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.frequencyseries import FrequencySeries
from gwpy.spectrogram import Spectrogram
import Kozapy.utils.filelist as existedfilelist    
from lib.channel import get_seis_chname
from lib.iofunc import fname_hdf5_longasd,fname_gwf,fname_hdf5_asd
import os

''' Seismic Noise
'''

def hoge(start,end,nproc=4,axis='X',prefix='./data',skip=True):
    '''
    '''
    fname_hdf5 = fname_hdf5_asd(start,end,prefix,axis)
    #log.debug(fname_hdf5)
    if os.path.exists(fname_hdf5):
        specgram = Spectrogram.read(fname_hdf5)
        return specgram
    try:
        chname = get_seis_chname(start,end,axis=axis)
        fname = fname_gwf(start,end,prefix='./data')
        data = TimeSeries.read(fname,chname,nproc=nproc)
        data.override_unit('ct')
    except:
        raise ValueError('!!!')

    if data.value.shape[0] != 131072: # (131072 = 2**17 = 2**12[sec] * 2**5[Hz] )
        log.debug('!!!!!!!! {0} {1}'.format(start,end))
        return None

    specgram = data.spectrogram2(fftlength=2**8,overlap=2**7,nproc=nproc)
    specgram.write(fname_hdf5,format='hdf5',overwrite=True)
    return specgram
    

            
if __name__ == "__main__":
    nproc = 8
    log.info('# ----------------------------------------')
    log.info('# Start SeismicNoise            ')
    from dataquality import DataQuality
    with DataQuality() as db:
        total = db.ask('select startgps,endgps from EXV_SEIS')
        available = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0')
        lackoffile = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=2')
        lackofdata = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=4')
        glitch = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=8')

    bad = len(total)-len(available)-len(lackoffile)-len(lackofdata)-len(glitch)
    if bad!=0:
        raise ValueError('!')

    if False:
        from lib.plot import plot_segmentlist
        start, end = total[0][0],total[-1][1]
        from gwpy.segments import DataQualityFlag
        available = DataQualityFlag(name='Available',active=available,known=[(start,end)])
        lackoffile = DataQualityFlag(name='No Frame Files',active=lackoffile,known=[(start,end)])
        lackofdata = DataQualityFlag(name='Lack of Data',active=lackofdata,known=[(start,end)])
        glitch = DataQualityFlag(name='Glitche',active=glitch,known=[(start,end)])
        total = DataQualityFlag(name='Total',active=total,known=[(start,end)])
        log.debug(total)
        plot_segmentlist(available,lackoffile,lackofdata,glitch,total,fname='./segment.png')

    
    x_specgrams = hoge(available[0][0],available[0][1],skip=False)
    y_specgrams = hoge(available[0][0],available[0][1],skip=False)
    z_specgrams = hoge(available[0][0],available[0][1],skip=False)
    n = len(available)
    import numpy as np
    for i,(start,end) in enumerate(available[1:]):
        log.debug('{0}/{1} : {2}'.format(i,n,start))
        x_specgrams.append(hoge(start,end,nproc=nproc,axis='X'),gap='ignore')
        y_specgrams.append(hoge(start,end,nproc=nproc,axis='Y'),gap='ignore')
        z_specgrams.append(hoge(start,end,nproc=nproc,axis='Z'),gap='ignore')

    # x
    percentile = 50
    asd = x_specgrams.percentile(percentile)
    fname = fname_hdf5_longasd(prefix='./data',axis='X',percentile=percentile)
    log.debug(fname)
    asd.write(fname,format='hdf5',overwrite=True)        
    percentile = 10
    asd = x_specgrams.percentile(percentile)
    fname = fname_hdf5_longasd(prefix='./data',axis='X',percentile=percentile)
    log.debug(fname)
    asd.write(fname,format='hdf5',overwrite=True)        
    percentile = 90
    asd = x_specgrams.percentile(percentile)
    fname = fname_hdf5_longasd(prefix='./data',axis='X',percentile=percentile)
    log.debug(fname)
    asd.write(fname,format='hdf5',overwrite=True)
    # Y
    percentile = 50
    asd = y_specgrams.percentile(percentile)
    fname = fname_hdf5_longasd(prefix='./data',axis='Y',percentile=percentile)
    log.debug(fname)
    asd.write(fname,format='hdf5',overwrite=True)        
    percentile = 10
    asd = y_specgrams.percentile(percentile)
    fname = fname_hdf5_longasd(prefix='./data',axis='Y',percentile=percentile)
    log.debug(fname)
    asd.write(fname,format='hdf5',overwrite=True)        
    percentile = 90
    asd = y_specgrams.percentile(percentile)
    fname = fname_hdf5_longasd(prefix='./data',axis='Y',percentile=percentile)
    log.debug(fname)
    asd.write(fname,format='hdf5',overwrite=True)        
    # Z
    percentile = 50
    asd = z_specgrams.percentile(percentile)
    fname = fname_hdf5_longasd(prefix='./data',axis='Z',percentile=percentile)
    log.debug(fname)
    asd.write(fname,format='hdf5',overwrite=True)        
    percentile = 10
    asd = z_specgrams.percentile(percentile)
    fname = fname_hdf5_longasd(prefix='./data',axis='Z',percentile=percentile)
    log.debug(fname)
    asd.write(fname,format='hdf5',overwrite=True)        
    percentile = 90
    asd = z_specgrams.percentile(percentile)
    fname = fname_hdf5_longasd(prefix='./data',axis='Z',percentile=percentile)
    log.debug(fname)
    asd.write(fname,format='hdf5',overwrite=True)        
    
    

    

    
    log.debug('Finish!')
