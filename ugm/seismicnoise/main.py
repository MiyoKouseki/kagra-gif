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
from lib.iofunc import fname_hdf5_longasd,fname_gwf,fname_hdf5_asd

import matplotlib.pyplot as plt

''' Seismic Noise
'''

def percentile(specgrams,percentile,axis,**kwargs):
    ''' Calculate a percentile with given spectrogram of seismometer
        in specified axis.    
    '''
    asd = specgrams.percentile(percentile)
    write = kwargs.pop('write',True)
    suffix = kwargs.pop('suffix','')
    if write:
        fname = fname_hdf5_longasd(axis,percentile,suffix=suffix,prefix='./data2')
        log.debug(fname)
        asd.write(fname,format='hdf5',overwrite=True)
    return asd


def get_array2d(start,end,axis='X',prefix='./data',**kwargs):
    ''' Get Spectrogram    

    Parameters
    ----------
    start
    end

    Returns
    -------


    '''
    nproc = kwargs.pop('nproc',4)
    bandpass = kwargs.pop('bandpass',None)
    fftlen = kwargs.pop('fftlen',2**8)

    # Load specgram from hdf5 file
    fname_hdf5 = fname_hdf5_asd(start,end,prefix,axis)
    if os.path.exists(fname_hdf5):
        specgram = Spectrogram.read(fname_hdf5,format='hdf5')
        if bandpass:
            timeseries = specgram.crop_frequencies(bandpass[0],bandpass[1]).sum(axis=1)
            return timeseries
        else:            
            return specgram

    # If no file, make specgram from timeseries data
    try:
        chname = get_seis_chname(start,end,axis=axis)
        fnamelist = existedfilelist(start,end)
        data = TimeSeries.read(fnamelist,chname,nproc=nproc)
        data = data.resample(32)
        data = data.crop(start,end)
    except:
        log.debug(traceback.format_exc())        
        raise ValueError('!!! {0} {1}'.format(start,end))
    
    # calculate specgram
    specgram = data.spectrogram2(fftlength=fftlen,overlap=fftlen/2,nproc=nproc)
    try:
        specgram.write(fname_hdf5,format='hdf5',overwrite=True)
        log.debug('Make {0}'.format(fname_hdf5))
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!!')

    return specgram


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--start',type=int,default=1211817600)
    parser.add_argument('--end',type=int,default=1245372032)
    parser.add_argument('--nproc',type=int,default=8)
    parser.add_argument('--percentile', action='store_false') # default True
    #parser.add_argument('--remakedb', action='store_true') # default False
    parser.add_argument('--remakedb', action='store_false') 
    args = parser.parse_args()
    nproc = args.nproc
    run_percentile = args.percentile
    remakedb = args.remakedb
    # ------------------------------------------------------------
    # Get segments
    # ------------------------------------------------------------
    from dataquality.dataquality import DataQuality
    with DataQuality('./dataquality/dqflag.db') as db:
        total      = db.ask('select startgps,endgps from EXV_SEIS WHERE ' +
                            'startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))
        available  = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0 ' +
                            'and startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))
        glitch     = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=8 ' +
                            'and startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))
        big_glitch = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=16 ' +
                            'and startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))
        if remakedb:
            with open('./result.txt','a') as f:
                for i,(start,end) in enumerate(total):
                    ans = check(start,end,plot=True,nproc=nproc)
                    fmt = '{3:03d}/{4:03d} {0} {1} {2}'
                    txt = fmt.format(start,end,ans,i+1,len(total))
                    log.debug(txt)
                    _txt = '{0} {1} {2}'.format(start,end,ans)
                    f.write(_txt+'\n')
            exit()

    # ------------------------------------------------------------
    # Main
    # ------------------------------------------------------------
    use = available+glitch+big_glitch
    use = np.array(use)
    use = np.sort(use,axis=0)
    multmode = True
    if multmode:
        fname_mult = ''
        exit()
    blrms = True
    fftlen = 2**8
    if not blrms:
        kwargs = {'nproc':nproc}
    else:
        bandpass = 1.0 # 1/3 oct bandpass
        low = bandpass/(2**(1./6)) # 1/6 oct 
        high = bandpass*(2**(1./6)) # 1/6 oct
        kwargs = {'nproc':nproc,'bandpass':[low,high]}
    start,end = use[0]
    x_array2ds = get_array2d(start,end,axis='X',**kwargs)
    y_array2ds = get_array2d(start,end,axis='Y',**kwargs)
    z_array2ds = get_array2d(start,end,axis='Z',**kwargs)
    n = len(use)
    for i,(start,end) in enumerate(use[1:]):
        array2d_x = get_array2d(start,end,axis='X',**kwargs)
        array2d_y = get_array2d(start,end,axis='Y',**kwargs)
        array2d_z = get_array2d(start,end,axis='Z',**kwargs)
        log.debug('{0}/{1} : {2}'.format(i+2,n,start))
        if not blrms: # get Long Spectrogram
            x_array2ds.append(array2d_x,gap='ignore')
            y_array2ds.append(array2d_y,gap='ignore')
            z_array2ds.append(array2d_z,gap='ignore')
        elif blrms: # get Long BLRMS TimeSeries
            x_array2ds.append(array2d_x,gap='pad',pad=0.0)
            y_array2ds.append(array2d_y,gap='pad',pad=0.0)
            z_array2ds.append(array2d_z,gap='pad',pad=0.0)

    try:
        specgram.write(fname_hdf5,format='hdf5',overwrite=True)
        log.debug('Make {0}'.format(fname_hdf5))
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!!')

    
    
    # Main : Percentile
    if run_percentile and not blrms:
        suffix = '_{start}_{end}'.format(start=args.start,end=args.end)
        for pctl in [1,5,10,50,90,95,99]:
            percentile(x_array2ds,pctl,'X',suffix=suffix)
            percentile(y_array2ds,pctl,'Y',suffix=suffix)
            percentile(z_array2ds,pctl,'Z',suffix=suffix)

    # Main : BLRMS
    if blrms:
        import astropy.units as u
        x_array2ds *= 1./(fftlen)*u.Hz*1.5 # enbw with hanning
        x_array2ds = x_array2ds**0.5
        suffix = '_{start}_{end}'.format(start=args.start,end=args.end)
        #_fmt = './data2/LongTerm_{0}_BLRMS_{1}_{2}mHz{3}.gwf'
        fmt = './data2/LongTerm_{0}_BLRMS_{1}mHz{2}.gwf'
        low,high = kwargs['bandpass']
        #_fname = _fmt.format('X',str(int(low*1000)),str(int(high*1000)),suffix)
        fname = fmt.format('X',int(bandpass*1000),suffix)
        x_array2ds.write(fname)
        log.debug(fname)
        y_array2ds *= 1./256*u.Hz*1.5 # enbw with hanning
        y_array2ds = y_array2ds**0.5
        #_fname = _fmt.format('Y',str(int(low*1000)),str(int(high*1000)),suffix)
        #fname = fmt.format('Y',bandpass,suffix)
        fname = fmt.format('Y',int(bandpass*1000),suffix)
        y_array2ds.write(fname)
        log.debug(fname)
        z_array2ds *= 1./256*u.Hz*1.5 # enbw with hanning
        z_array2ds = z_array2ds**0.5
        #_fname = _fmt.format('Z',str(int(low*1000)),str(int(high*1000)),suffix)
        fname = fmt.format('Z',int(bandpass*1000),suffix)
        z_array2ds.write(fname)
        log.debug(fname)        

    # Finish!
    log.debug('Finish!')
