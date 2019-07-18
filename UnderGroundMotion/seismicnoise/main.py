#
#! coding:utf-8
__author__ = 'Koseki Miyo'
import traceback
import os
import numpy as np

import astropy.units as u
from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.spectrogram import Spectrogram

import Kozapy.utils.filelist as existedfilelist

from lib.plot import plot_segmentlist
import lib.logger
log = lib.logger.Logger('main')
from lib.channel import get_seis_chname
from lib.iofunc import fname_hdf5_longasd,fname_gwf,fname_hdf5_asd,fname_gwf_longblrms


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
        fname = fname_hdf5_longasd(axis,percentile,suffix=suffix)
        log.debug(fname)
        asd.write(fname,format='hdf5',overwrite=True)
    return asd


def get_array2d(start,end,axis='X',prefix='./data',**kwargs):
    '''
    '''
    nproc = kwargs.pop('nproc',4)
    bandpass = kwargs.pop('bandpass',None)
    blrms = kwargs.pop('blrms',None)
    fftlen = kwargs.pop('fftlen',2**8)
    overlap = fftlen/2

    # check existance of the spectrogram data
    fname_hdf5 = fname_hdf5_asd(start,end,prefix,axis)
    if os.path.exists(fname_hdf5):
        specgram = Spectrogram.read(fname_hdf5)
        if blrms:
            timeseries = specgram.crop_frequencies(blrms[0],blrms[1]).sum(axis=1)
            return timeseries
        return specgram
    
    # If spectrogram dose not exist, calculate it from timeseries data.
    try:
        fname = fname_gwf(start,end,prefix='./data')
        chname = get_seis_chname(start,end,axis=axis)
        # check existance of the timeseries data
        if os.path.exists(fname):
            data = TimeSeries.read(fname,chname,nproc=nproc)
        else:
            # when timeseries data dose not exist
            fnamelist = existedfilelist(start,end)
            chname = get_seis_chname(start,end)
            datadict = TimeSeriesDict.read(fnamelist,chname,nproc=nproc)
            datadict = datadict.resample(32)
            datadict = datadict.crop(start,end)
            chname = get_seis_chname(start,end,axis=axis)
            datadict.write(fname,format='gwf.lalframe')
            data = TimeSeries.read(fname,chname,nproc=nproc)
            # If data broken, raise Error.
            if data.value.shape[0] != 131072:
                log.debug(data.value.shape)
                log.debug('####### {0} {1}'.format(start,end))
                raise ValueError('data broken')
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!!')

    # if data broken, raise Error.
    if data.value.shape[0] != 131072: # (131072 = 2**17 = 2**12[sec] * 2**5[Hz] )
        log.debug(data.value.shape)
        log.debug('!!!!!!!! {0} {1}'.format(start,end))
        raise ValueError('data broken')

    # calculate from timeseries data
    specgram = data.spectrogram2(fftlength=fftlen,overlap=overlap,nproc=nproc)
    specgram.write(fname_hdf5,format='hdf5',overwrite=True)
    return specgram
    
            
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--start',type=int,default=1211817600)
    parser.add_argument('--end',type=int,default=1245372032)
    parser.add_argument('--nproc',type=int,default=8)
    args = parser.parse_args()
    nproc = args.nproc

    # Get segments
    from dataquality.dataquality import DataQuality
    with DataQuality('./dataquality/dqflag.db') as db:
        total      = db.ask('select startgps,endgps from EXV_SEIS')
        available  = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0')
        lackoffile = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=2')
        lackofdata = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=4')
        glitch     = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=8')
        use        = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0 ' +
                        'and startgps>={0} and endgps<={1}'.format(args.start,args.end))
    bad = len(total)-len(available)-len(lackoffile)-len(lackofdata)-len(glitch)
    if bad!=0:
        raise ValueError('SegmentList Error: Missmatch the number of segments.')


    log.info('# ----------------------------------------')
    log.info('# Start SeismicNoise                      ')
    log.info('# ----------------------------------------')

    # Setup
    bandlimited = True
    rms = True
    if bandlimited and rms:
        kwargs = {'nproc':nproc,'blrms':(0.2,0.3)}
        default = {'gap':'pad','pad':0.0}
    else:
        kwargs = {'nproc':nproc,'bandpass':False}
        default = {'gap':'ignore'}    
    fftlen = 2**8
    enbw = (1./fftlen)*u.Hz*1.5


    # Main
    start,end = use[0]
    x_array2ds = get_array2d(start,end,axis='X',**kwargs)
    y_array2ds = get_array2d(start,end,axis='Y',**kwargs)
    z_array2ds = get_array2d(start,end,axis='Z',**kwargs)
    n = len(use)
    for i,(start,end) in enumerate(use[1:]):
        log.debug('{0}/{1} : {2}'.format(i+2,n,start))
        array2d_x = get_array2d(start,end,axis='X',**kwargs)
        array2d_y = get_array2d(start,end,axis='Y',**kwargs)
        array2d_z = get_array2d(start,end,axis='Z',**kwargs)
        x_array2ds.append(array2d_x,**default)
        y_array2ds.append(array2d_y,**default)
        z_array2ds.append(array2d_z,**default)
            
    # Main : `n`th Percentile
    suffix = '_{start}_{end}'.format(start=args.start,end=args.end)
    run_percentile = True
    if run_percentile and not bandlimited:
        for pctl in [10,50,90]:
            percentile(x_array2ds,pctl,'X',suffix=suffix)
            percentile(y_array2ds,pctl,'Y',suffix=suffix)
            percentile(z_array2ds,pctl,'Z',suffix=suffix)


    # Main : Band Limited Root Mean Square
    blrms = True
    if blrms and bandlimited:
        log.debug(enbw)
        x_blrms = (x_array2ds*enbw)**0.5 # ct
        y_blrms = (y_array2ds*enbw)**0.5 # ct
        z_blrms = (z_array2ds*enbw)**0.5 # ct
        log.debug(x_blrms)
        low = int(kwargs['blrms'][0]*1000)
        high = int(kwargs['blrms'][1]*1000)
        suffix = '_{start}_{end}'.format(start=args.start,end=args.end)        
        x_fname = fname_gwf_longblrms('X',low,high,suffix=suffix)
        y_fname = fname_gwf_longblrms('Y',low,high,suffix=suffix)
        z_fname = fname_gwf_longblrms('Z',low,high,suffix=suffix)
        log.debug(x_fname)
        x_blrms.write(x_fname)
        log.debug(y_fname)
        y_blrms.write(y_fname)
        log.debug(z_fname)
        z_blrms.write(z_fname)

        
    # Main : plot Segment List
    if False:
        from lib.plot import plot_segmentlist
        start, end = total[0][0], total[-1][1]
        from gwpy.segments import DataQualityFlag
        available = DataQualityFlag(name='Available',active=available,
                                    known=[(start,end)])
        lackoffile = DataQualityFlag(name='No Frame Files',active=lackoffile,
                                     known=[(start,end)])
        lackofdata = DataQualityFlag(name='Lack of Data',active=lackofdata,
                                     known=[(start,end)])
        glitch = DataQualityFlag(name='Glitche',active=glitch,known=[(start,end)])
        total = DataQualityFlag(name='Total',active=total,known=[(start,end)])
        plot_segmentlist(available,lackoffile,lackofdata,glitch,total,
                         fname='./result/segment.png')
    
        
    # Finish!
    log.debug('Finish!')
