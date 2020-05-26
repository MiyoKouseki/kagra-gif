#
#! coding:utf-8
__author__ = 'Koseki Miyo'
import traceback
import os
import numpy as np

from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.spectrogram import Spectrogram

import Kozapy.utils.filelist as existedfilelist

from lib.plot import plot_segmentlist
import lib.logger
log = lib.logger.Logger('main')
from lib.channel import get_seis_chname
from lib.check import check
from lib.iofunc import fname_hdf5_percentile,fname_gwf,fname_hdf5_asd,fname_hdf5_diffasd

from lib.iofunc import fname_specgram

import matplotlib.pyplot as plt
from dataquality.dataquality import remake

''' Seismic Noise
'''

#--------------------------------------------------------------------------------
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
    fname_hdf5 = fname_specgram(start,end,prefix=seis,axis=axis)

    # Load specgram from hdf5 file
    if os.path.exists(fname_hdf5):
        specgram = Spectrogram.read(fname_hdf5,format='hdf5')
        return specgram

    # If no file, make specgram from timeseries data
    if '-' in seis:
        seis,seis2 = seis.split('-')
        diff = True
    try:
        chname = get_seis_chname(start,end,axis=axis,seis=seis)[0]
        fnamelist = existedfilelist(start,end)
        data = TimeSeries.read(fnamelist,chname,nproc=nproc)
        data = data.resample(32)
        data = data.crop(start,end)
        if diff:
            chname2 = get_seis_chname(start,end,axis=axis,seis=seis2)[0]
            data2 = TimeSeries.read(fnamelist,chname2,nproc=nproc)
            data2 = data2.resample(32)
            data2 = data2.crop(start,end)
            data = data - data2
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


def append_data(segment,blrms=False,ave=False,**kwargs):
    '''
    '''
    n = len(segment)
    # i = 0
    start,end = segment[0]
    x = get_spectrogram(start,end,axis='X',**kwargs)
    y = get_spectrogram(start,end,axis='Y',**kwargs)
    z = get_spectrogram(start,end,axis='Z',**kwargs)
    if ave :
        x = [x.mean(axis=0)]
        y = [y.mean(axis=0)]
        z = [z.mean(axis=0)]
        # x = x.mean(axis=0)
        # y = y.mean(axis=0)
        # z = z.mean(axis=0)
    # i > 1
    for i,(start,end) in enumerate(segment[1:]):
        _x = get_spectrogram(start,end,axis='X',**kwargs)
        _y = get_spectrogram(start,end,axis='Y',**kwargs)
        _z = get_spectrogram(start,end,axis='Z',**kwargs)
        log.debug('{0:04d}/{1:04d} : Append {2} '.format(i+2,n,start))    
        if (not blrms): # get Long Spectrogram
            if ave :
                _x = _x.mean(axis=0)
                _y = _y.mean(axis=0)
                _z = _z.mean(axis=0)
                x += [_x] 
                y += [_y] 
                z += [_z] 
                # x.append(_x,gap='ignore')
                # y.append(_y,gap='ignore')
                # z.append(_z,gap='ignore')            
            else:
                x.append(_x,gap='ignore')
                y.append(_y,gap='ignore')
                z.append(_z,gap='ignore')            
        elif blrms: # get Long BLRMS TimeSeries        
            low,high = kwargs.pop('bandpass',None)
            _x = _x.crop_frequencies(low,high).sum(axis=1)
            _y = _y.crop_frequencies(low,high).sum(axis=1)
            _z = _z.crop_frequencies(low,high).sum(axis=1)
            x.append(_x,gap='pad',pad=0.0)
            y.append(_y,gap='pad',pad=0.0)
            z.append(_z,gap='pad',pad=0.0)
    if ave:
        x = Spectrogram.from_spectra(*x)
        y = Spectrogram.from_spectra(*y)
        z = Spectrogram.from_spectra(*z)
    return x,y,z


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--start',type=int,default=1211817600)
    parser.add_argument('--end',type=int,default=1245372032)
    parser.add_argument('--nproc',type=int,default=8)
    parser.add_argument('--seis',type=str,default='EXV')
    parser.add_argument('--term',type=str,default='')
    parser.add_argument('--percentile', action='store_true') # default False
    parser.add_argument('--remakedb', action='store_true') # default False
    parser.add_argument('--savespecgram', action='store_true') # default False
    args = parser.parse_args()
    start,end = args.start,args.end
    nproc = args.nproc
    run_percentile = args.percentile
    remakedb = args.remakedb
    savespecgram = args.savespecgram
    seis = args.seis
    term = args.term

    # ------------------------------------------------------------
    #  Choose Segment  
    # ------------------------------------------------------------
    from dataquality.dataquality import DataQuality, fmt_total,fmt_gauss
    with DataQuality('./dataquality/dqflag.db') as db:
        total = db.ask(fmt_total.format(start,end,'EXV_SEIS'))
        gauss = db.ask(fmt_gauss.format(start,end,'EXV_SEIS'))

    if remakedb:
        import random
        fname = './dataquality/result_{0}.txt'.format(seis)
        if not os.path.exists(fname.split("result")[0]):
            os.mkdir(fname.split("result")[0])
        with open(fname,'a') as f:
            for i,(start,end) in enumerate(total):
            #for i,(start,end) in enumerate(random.sample(total,1)):
                ans = check(start,end,plot=False,nproc=nproc,
                            seis=seis,axis='X',
                            tlen=4096,sample_rate=16,cl=0.05)
                log.debug('{0:03d}/{1:03d} : {2} {3} {4}'.format(
                    i+1,len(total),start,end,ans))
                f.write('{0} {1} {2}\n'.format(start,end,ans))
    else:
        log.debug('Not remake.')

    segment = gauss

    # ------------------------------------------------------------
    # Percentile
    # ------------------------------------------------------------
    if run_percentile:
        x,y,z = append_data(segment,blrms=False,seis=seis,nproc=nproc,ave=True)
        if savespecgram:
            log.debug('Finish to save spectrogram.')
            exit()
        if term=='all':
            prefix = '{0}'.format(seis)
        else:
            prefix = '{0}{1}'.format(seis,term)
        for pctl in [1,5,10,50,90,95,99]:
            save_percentile(x,pctl,'X',prefix=prefix)
            save_percentile(y,pctl,'Y',prefix=prefix)
            save_percentile(z,pctl,'Z',prefix=prefix)
        save_mean(x,'X',prefix=prefix)
        save_mean(y,'Y',prefix=prefix)
        save_mean(z,'Z',prefix=prefix)


    # ------------------------------------------------------------
    # Band Limited RMS
    # ------------------------------------------------------------
    if False:
        bandpass = 0.2 # 1/3 oct bandpass
        low  = bandpass/(2**(1./6)) # 1/6 oct 
        high = bandpass*(2**(1./6)) # 1/6 oct
        kwargs = {'nproc':nproc,'bandpass':[low,high]}
        x,y,z = append_data(segment,blrms=False,seis=seis,
                            bandpass=[low,high],
                            nproc=nproc)
        import astropy.units as u
        x *= 1./(fftlen)*u.Hz*1.5 # enbw with hanning
        x = x**0.5
        fmt = './data2/LongTerm_{0}_BLRMS_{1}mHz.gwf'
        low,high = kwargs['bandpass']
        fname = fmt.format('X',int(bandpass*1000))
        x.write(fname)
        log.debug(fname)
        y *= 1./256*u.Hz*1.5 # enbw with hanning
        y = y**0.5
        fname = fmt.format('Y',int(bandpass*1000))
        y.write(fname)
        log.debug(fname)
        z *= 1./256*u.Hz*1.5 # enbw with hanning
        z = z**0.5
        fname = fmt.format('Z',int(bandpass*1000))
        z.write(fname)
        log.debug(fname)        

    # Finish!
    log.debug('Finish!')
