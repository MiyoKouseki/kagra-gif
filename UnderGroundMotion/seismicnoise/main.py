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
from lib.iofunc import fname_hdf5_longasd,fname_gwf,fname_hdf5_asd


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

    # check existance of the spectrogram data
    fname_hdf5 = fname_hdf5_asd(start,end,prefix,axis)
    if os.path.exists(fname_hdf5):
        specgram = Spectrogram.read(fname_hdf5)
        if bandpass:
            timeseries = specgram.crop_frequencies(bandpass[0],bandpass[1]).sum(axis=1)
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
    specgram = data.spectrogram2(fftlength=2**8,overlap=2**7,nproc=nproc)
    specgram.write(fname_hdf5,format='hdf5',overwrite=True)
    return specgram
    
            
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--start',type=int,default=1211817600)
    parser.add_argument('--end',type=int,default=1245372032)
    parser.add_argument('--nproc',type=int,default=8)
    parser.add_argument('--percentile', action='store_false')
    parser.add_argument('--alldata', action='store_false')
    args = parser.parse_args()
    nproc = args.nproc
    run_percentile = args.percentile
    alldata = args.alldata
    if args.start!=1211817600 or args.end!=1245372032:
        alldata = True 

    log.info('# ----------------------------------------')
    log.info('# Start SeismicNoise            ')
    log.info('# ----------------------------------------')

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

    # Plot segmentlist
    if False:
        from lib.plot import plot_segmentlist
        start, end = total[0][0],total[-1][1]
        from gwpy.segments import DataQualityAlldata
        available = DataQualityAlldata(name='Available',active=available,
                                    known=[(start,end)])
        lackoffile = DataQualityAlldata(name='No Frame Files',active=lackoffile,
                                     known=[(start,end)])
        lackofdata = DataQualityAlldata(name='Lack of Data',active=lackofdata,
                                     known=[(start,end)])
        glitch = DataQualityAlldata(name='Glitche',active=glitch,known=[(start,end)])
        total = DataQualityAlldata(name='Total',active=total,known=[(start,end)])
        plot_segmentlist(available,lackoffile,lackofdata,glitch,total,
                         fname='./segment.png')
        exit()


    # Main
    blrms = False
    #kwargs = {'nproc':nproc,'bandpass':(0.0,0.1)}
    kwargs = {'nproc':nproc}
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
        if not blrms:
            x_array2ds.append(array2d_x,gap='ignore')
            y_array2ds.append(array2d_y,gap='ignore')
            z_array2ds.append(array2d_z,gap='ignore')
        elif blrms:
            x_array2ds.append(array2d_x,gap='pad',pad=0.0)
            y_array2ds.append(array2d_y,gap='pad',pad=0.0)
            z_array2ds.append(array2d_z,gap='pad',pad=0.0)

    # Main : Percentile
    run_percentile = True
    suffix = '_{start}_{end}'.format(start=args.start,end=args.end)
    if run_percentile:
        for pctl in [10,50,90]:
            percentile(x_array2ds,pctl,'X',suffix=suffix)
            percentile(y_array2ds,pctl,'Y',suffix=suffix)
            percentile(z_array2ds,pctl,'Z',suffix=suffix)

    # Main : BLRMS
    if False:
        import astropy.units as u
        x_array2ds *= 1./256*u.Hz*1.5 # enbw with hanning
        x_array2ds = x_array2ds**0.5
        x_array2ds.write('./data/LongTerm_X_BLRMS_0_100mHz.gwf')
        y_array2ds *= 1./256*u.Hz*1.5 # enbw with hanning
        y_array2ds = y_array2ds**0.5
        y_array2ds.write('./data/LongTerm_Y_BLRMS_0_100mHz.gwf')
        z_array2ds *= 1./256*u.Hz*1.5 # enbw with hanning
        z_array2ds = z_array2ds**0.5
        z_array2ds.write('./data/LongTerm_Z_BLRMS_0_100mHz.gwf')
        
    # Finish!
    log.debug('Finish!')
