#
#! coding:utf-8
__author__ = 'Koseki Miyo'
import traceback
from tqdm import tqdm
import os
import astropy.units as u

from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.spectrogram import Spectrogram

import Kozapy.utils.filelist as existedfilelist

from lib.plot import plot_segmentlist
import lib.logger
log = lib.logger.Logger('main')

from lib.channel import get_seis_chname
from lib.check import check
from lib.iofunc import fname_hdf5_percentile, fname_specgram
from dataquality.dataquality import remake


''' Seismic Noise
'''

START_GPS = 1211817600 # UTC: 2018-05-31 15:59:42
END_GPS   = 1245372032 # UTC: 2019-06-24 00:40:14 (end=start+2**25)

# ------------------------------------------------------------------------------

def save_percentile(specgrams,percentile=50,axis='X',**kwargs):
    ''' Calculate and save a percentile with spectrogram.

    This function calculates a amplitude spectrum density of 
    percentile and saves in local working space.
    
    Parameters
    ----------
    specgrams : `gwpy.spectrogram`
        spectrogram.
    percentile : `int`
        percentile. default is 50.
    axis : `str`
        axis of seismometer

    Returns
    -------
    asd : `gwpy.frequencyseries.FrequencySeries`
        amplitude spectrum density.
    '''
    asd = specgrams.percentile(percentile)
    prefix = kwargs.pop('prefix','')
    fname = fname_hdf5_percentile(axis,percentile,prefix=prefix)
    if not os.path.exists('./data2/'+prefix):
        os.mkdir('./data2/'+prefix)
    log.debug('Save ASD as '+fname)
    asd.write(fname,format='hdf5',overwrite=True)
    return asd


def save_mean(specgrams,axis,**kwargs):
    ''' Calculate a percentile with given spectrogram of seismometer
        in specified axis.    

    Parameters
    ----------
    specgrams : `gwpy.spectrogram`
        spectrogram.
    axis : `str`
        axis of seismometer

    Returns
    -------
    asd : `gwpy.frequencyseries.FrequencySeries`
        amplitude spectrum density.
    '''    
    asd = specgrams.mean(axis=0)
    prefix = kwargs.pop('prefix','')
    fname = fname_hdf5_percentile(axis,'mean',prefix=prefix)
    log.debug('Save ASD as '+fname)
    asd.write(fname,format='hdf5',overwrite=True)
    return asd


def get_spectrogram(start,end,axis='X',seis='EXV',**kwargs):
    ''' Get Spectrogram    

    Parameters
    ----------
    start : `int`
        start GPS time.
    end : `int`
       end GPS time.

    Returns
    -------
    specgram : `gwpy.spectrogram.Spectrogram`
        spectrogram.
    '''
    nproc = kwargs.pop('nproc',3)
    bandpass = kwargs.pop('bandpass',None)
    fftlen = kwargs.pop('fftlen',2**8)
    diff = kwargs.pop('diff',False)
    fs = kwargs.pop('fs',256)
    fname_hdf5 = fname_specgram(start,end,prefix=seis,axis=axis)

    # Load specgram from hdf5 file
    if os.path.exists(fname_hdf5):
        specgram = Spectrogram.read(fname_hdf5,format='hdf5')
        return specgram

    # If no file, make specgram from timeseries data
    try:
        chname = get_seis_chname(start,end,axis=axis,seis=seis)[0]
        fnamelist = existedfilelist(start,end)
        data = TimeSeries.read(fnamelist,chname,nproc=nproc)
        data = data.resample(fs)
        data = data.crop(start,end)
    except:
        log.debug(traceback.format_exc())        
        raise ValueError('!!! {0} {1}'.format(start,end))
    
    # calculate specgram
    specgram = data.spectrogram2(fftlength=fftlen,overlap=fftlen/2,nproc=nproc)
    try:
        fname_dir = '/'.join(fname_hdf5.split('/')[:4])
        if not os.path.exists(fname_dir):
            os.makedirs(fname_dir)
        specgram.write(fname_hdf5,format='hdf5',overwrite=True)
        log.debug('Make {0}'.format(fname_hdf5))
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!!')
    return specgram


def append_data(segment,**kwargs):
    '''
    '''
    blrms = kwargs.pop('blrms',False)
    n = len(segment)
    kwargs['n'] = len(segment)
    # i = 0
    start,end = segment[0]
    x = [get_spectrogram(start,end,axis='X',**kwargs).mean(axis=0)]
    y = [get_spectrogram(start,end,axis='Y',**kwargs).mean(axis=0)]
    z = [get_spectrogram(start,end,axis='Z',**kwargs).mean(axis=0)]
    # i > 1
    for i,(start,end) in enumerate(segment[1:]):
        x += [get_spectrogram(start,end,axis='X',**kwargs).mean(axis=0)]
        y += [get_spectrogram(start,end,axis='Y',**kwargs).mean(axis=0)]
        z += [get_spectrogram(start,end,axis='Z',**kwargs).mean(axis=0)]
        log.debug('{0:04d}/{1:04d} : Append {2} '.format(i+2,n,start))  

    # make spectrogram
    x = Spectrogram.from_spectra(*x)
    y = Spectrogram.from_spectra(*y)
    z = Spectrogram.from_spectra(*z)
    return x,y,z

def get_segment_seis(start,end,seis,nproc):
    from dataquality.dataquality import DataQuality, fmt_total,fmt_gauss
    with DataQuality('./dataquality/dqflag.db') as db:
        total = db.ask(fmt_total.format(start,end,'EXV_SEIS'))
        gauss = db.ask(fmt_gauss.format(start,end,'EXV_SEIS'))
    return total,gauss

def get_segment_2seis(start,end,seis1,seis2,nproc):
    from dataquality.dataquality import DataQuality, fmt_total,fmt_gauss, fmt_gauss_2seis
    with DataQuality('./dataquality/dqflag.db') as db:
        total = db.ask(fmt_total.format(start,end,'EXV_SEIS'))
        gauss = db.ask(fmt_gauss_2seis.format(start,end,seis1,seis2))
    return total,gauss

def get_segment_3seis(start,end,seis1,seis2,seis3,nproc):
    from dataquality.dataquality import DataQuality, fmt_total,fmt_gauss, fmt_gauss_3seis
    with DataQuality('./dataquality/dqflag.db') as db:
        total = db.ask(fmt_total.format(start,end,'EXV_SEIS'))
        gauss = db.ask(fmt_gauss_3seis.format(start,end,seis1,seis2,seis3))
    return total,gauss


def updatedb(segment,seis,nproc,plot=False):
    import random
    fname = './dataquality/result_{0}.txt'.format(seis)
    if not os.path.exists(fname.split("result")[0]):
        os.mkdir(fname.split("result")[0])
        
    with open(fname,'a') as f:
        for i,(start,end) in enumerate(segment):
            kwargs = {'nproc':nproc,'plot':plot,'seis':seis,
                      'axis':'all','tlen':4096,'sample_rate':16,'cl':0.05}
            ans = check(start,end,**kwargs)
            log.debug('{0:03d}/{1:03d} : {2} {3} {4}'.format(
                i+1,len(segment),start,end,ans))
            f.write('{0} {1} {2}\n'.format(start,end,ans))

def balsdb(fname,seis):
    remake(fname,seis)


def download_seis_data(segment,seis,axis,nproc=1,fs=256):
    '''
    '''
    start,end = segment
    _chname = get_seis_chname(start,end,axis=axis,seis=seis)[0]
    _fnamelist = existedfilelist(start,end)
    try:
        data = TimeSeries.read(_fnamelist,_chname,nproc=nproc,
                               format='gwf.framecpp')
        data = data.resample(fs)
        data = data.crop(start,end)
        data.override_unit('ct')
        fname = './tmp/{0}_{1}/{0}_{1}_{2}.gwf'.format(start,end,_chname)
        if not os.path.exists('./tmp/{0}_{1}'.format(start,end)):
            os.mkdir('./tmp/{0}_{1}'.format(start,end))
        if not os.path.exists(fname):        
            data.write(fname)
        log.debug(fname)
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!! {0} {1}'.format(start,end))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--start',type=int,default=START_GPS)
    parser.add_argument('--end',type=int,default=END_GPS)
    parser.add_argument('--nproc',type=int,default=8)
    parser.add_argument('--seis',type=str,default='EXV')
    parser.add_argument('--asd', action='store_true') # default False
    parser.add_argument('--remakedb', action='store_true')
    parser.add_argument('--updatedb', action='store_true')
    parser.add_argument('--balsdb', action='store_true')
    parser.add_argument('--bandpass', action='store_true')
    parser.add_argument('--savespecgram', action='store_true')
    parser.add_argument('--download_gwf', action='store_true')
    log.debug('!')
    args = parser.parse_args()
    start,end = args.start,args.end
    nproc = args.nproc
    remakedb = args.remakedb
    savespecgram = args.savespecgram
    seis = args.seis
    # -------------------------------------------------------------------------
    #  Choose Segment  
    # -------------------------------------------------------------------------
    total,gauss = get_segment_seis(start,end,seis,nproc)
    #total,gauss = get_segment_2seis(start,end,'EXV_SEIS','EYV_SEIS',nproc)
    #total,gauss = get_segment_2seis(start,end,'EXV_SEIS','IXV_SEIS',nproc)
    total,gauss = get_segment_3seis(1228662018,end,'EXV_SEIS','IXV_SEIS','EYV_SEIS',nproc) # use data after Dec 12 2018 
    
    # -------------------------------------------------------------------------
    #  Choose Calculation
    # -------------------------------------------------------------------------
    if args.download_gwf:
        import random
        random.seed(34)
        total = random.sample(gauss,100)
        [download_seis_data(segment,'EXV','X') for segment in total]
        [download_seis_data(segment,'EXV','Y') for segment in total]
        [download_seis_data(segment,'EXV','Z') for segment in total]
        [download_seis_data(segment,'IXV','X') for segment in total]
        [download_seis_data(segment,'IXV','Y') for segment in total]
        [download_seis_data(segment,'IXV','Z') for segment in total]
        [download_seis_data(segment,'EYV','X') for segment in total]
        [download_seis_data(segment,'EYV','Y') for segment in total]
        [download_seis_data(segment,'EYV','Z') for segment in total]
        exit()
        
    if args.updatedb:
        #total = total[20:21]
        updatedb(total,seis,nproc,plot=False)
        
    if args.balsdb: 
        bals('./dataquality/result_EXV.txt',seis)
        
    if args.savespecgram:        
        kwargs = {'seis':seis,'nproc':nproc}
        x,y,z = append_data(gauss,**kwargs)
        log.debug('Finish to save spectrogram.')
        exit()
    
    if args.asd: # calculate asd
        kwargs = {'seis':seis,'nproc':nproc}
        x,y,z = append_data(gauss,**kwargs)
        for pctl in [1,5,10,50,90,95,99]:
            save_percentile(x,pctl,'X',prefix=seis)
            save_percentile(y,pctl,'Y',prefix=seis)
            save_percentile(z,pctl,'Z',prefix=seis)
            
        save_mean(x,'X',prefix=seis)
        save_mean(y,'Y',prefix=seis)
        save_mean(z,'Z',prefix=seis)
    
    # Finish!
    log.debug('Finish!')
    
