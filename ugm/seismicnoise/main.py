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
    '''
    nproc = kwargs.pop('nproc',4)
    bandpass = kwargs.pop('bandpass',None)

    # Load specgram from hdf5 file
    fname_hdf5 = fname_hdf5_asd(start,end,prefix,axis)
    if os.path.exists(fname_hdf5):
        specgram = Spectrogram.read(fname_hdf5)
        if bandpass:
            timeseries = specgram.crop_frequencies(bandpass[0],bandpass[1]).sum(axis=1)
            return timeseries
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
        raise ValueError('!!!')

    # if timeseries data broken, raise Error.
    if data.value.shape[0] != 131072: 
        # (131072 = 2**17 = 2**12[sec] * 2**5[Hz] )
        log.debug(data.value.shape)
        log.debug('!!!!!!!! {0} {1}'.format(start,end))
        raise ValueError('data broken')
    
    # calculate specgram
    specgram = data.spectrogram2(fftlength=2**8,overlap=2**7,nproc=nproc)
    try:
        specgram.write(fname_hdf5,format='hdf5',overwrite=True)
    except IOError as e:
        log.debug(traceback.format_exc())
        raise ValueError('No File')
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!!')


    return specgram


def check(start,end,plot=False):
    try:
        chname = get_seis_chname(start,end,axis='X')
        fnamelist = existedfilelist(start,end)
        data = TimeSeries.read(fnamelist,chname,nproc=nproc)
        data = data.resample(32)
        data = data.crop(start,end)
    except ValueError as e:
        if 'Cannot append discontiguous TimeSeries' in e.args[0]:
            return 'NoData:_LackofData'
        elif 'Failed to read' in e.args[0]:
            return 'NoData_FailedtoRead'
        else:
            log.debug(traceback.format_exc())
            raise ValueError('!!!')
    except IndexError as e:
        if 'cannot read TimeSeries from empty source list' in e.args[0]:
            return 'NoData:_Empty'
        else:
            log.debug(traceback.format_exc())
            raise ValueError('!!!')
    except RuntimeError as e:
        if 'Failed to read' in e.args[0]:
            return 'NoData_FailedtoRead'
        else:
            log.debug(traceback.format_exc())
            raise ValueError('!!!')
    except TypeError  as e:
        if 'NoneType' in e.args[0]:
            return 'NoData_NoChannel'
        else:
            log.debug(traceback.format_exc())
            raise ValueError('!!!')
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!!')

    if data.shape[0] != 131072:
        return 'NoData_FewData'
    if data.std().value == 0:
        return 'NoData_AllZero'
    if any(data.value==0.0):
        return 'NoData_AnyZero'
    std = data.std().value
    mean = data.mean().value
    _max = data.max().value
    if np.abs(_max-mean)/std > 10:
        return 'Glitch_10sigma'
    elif  np.abs(_max-mean)/std > 5:
        return 'Glitch_5sigma'
    if plot:
        fig,ax=plt.subplots(1,1,figsize=(6,4),sharex=True)
        ax.plot(data,'k')
        ax.hlines(mean,start,end,'k')
        ax.hlines(mean+std*5,start,end,'k')
        ax.hlines(mean-std*5,start,end,'k')
        ax.set_xscale('auto-gps')
        ax.set_xlim(start,end)
        plt.savefig('./tmp/{0}_{1}.png'.format(start,end))
        plt.close()
    return 'Stationaly'

            
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

    mkdir = True

    log.info('# ----------------------------------------')
    log.info('# Start SeismicNoise                      ')
    log.info('# ----------------------------------------')

    # Get segments
    remake_db = False
    from dataquality.dataquality import DataQuality
    with DataQuality('./dataquality/dqflag.db') as db:
        total      = db.ask('select startgps,endgps from EXV_SEIS WHERE ' +
                            'startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))
        available  = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0 ' +
                            'and startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))
        lackoffile = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=2 ' +
                            'and startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))
        lackofdata = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=4 ' +
                            'and startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))
        glitch     = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=8 ' +
                            'and startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))
        glitch_big = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=16 ' +
                            'and startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))

        use        = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0 ' +
                            'and startgps>={0} and endgps<={1}'.format(args.start,
                                                                       args.end))
        bad = len(total)-len(available)-len(lackoffile)-len(lackofdata)-len(glitch)-len(glitch_big)

    if bad!=0:
        raise ValueError('SegmentList Error: Missmatch the number of segments.')

    if remake_db:        
        f = open('result.txt','a')
        for i,(start,end) in enumerate(total):
            ans = check(start,end,plot=False)
            txt = '{3:03d}/{4:03d} {0} {1} {2}'.format(start,end,ans,i,len(use))
            log.debug(txt)
            _txt = '{0} {1} {2}'.format(start,end,ans)
            f.write(_txt+'\n')
        f.close()


    # Main
    blrms = False
    kwargs = {'nproc':nproc}
    #kwargs = {'nproc':nproc,'bandpass':[0.2,0.3]}
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
        if not blrms: # get Long Spectrogram
            x_array2ds.append(array2d_x,gap='ignore')
            y_array2ds.append(array2d_y,gap='ignore')
            z_array2ds.append(array2d_z,gap='ignore')
        elif blrms: # get Long TimeSeries
            x_array2ds.append(array2d_x,gap='pad',pad=0.0)
            y_array2ds.append(array2d_y,gap='pad',pad=0.0)
            z_array2ds.append(array2d_z,gap='pad',pad=0.0)

    # Main : Percentile
    run_percentile = True
    suffix = '_{start}_{end}'.format(start=args.start,end=args.end)
    if run_percentile and not blrms:
        for pctl in [1,5,10,50,90,95,99]:
            percentile(x_array2ds,pctl,'X',suffix=suffix)
            percentile(y_array2ds,pctl,'Y',suffix=suffix)
            percentile(z_array2ds,pctl,'Z',suffix=suffix)

    # Main : BLRMS
    if blrms:
        import astropy.units as u
        x_array2ds *= 1./256*u.Hz*1.5 # enbw with hanning
        x_array2ds = x_array2ds**0.5
        suffix = '_{start}_{end}'.format(start=args.start,end=args.end)
        x_array2ds.write('./data2/LongTerm_X_BLRMS_100_300mHz{0}.gwf'.format(suffix))
        y_array2ds *= 1./256*u.Hz*1.5 # enbw with hanning
        y_array2ds = y_array2ds**0.5
        y_array2ds.write('./data2/LongTerm_Y_BLRMS_100_300mHz{0}.gwf'.format(suffix))
        z_array2ds *= 1./256*u.Hz*1.5 # enbw with hanning
        z_array2ds = z_array2ds**0.5
        z_array2ds.write('./data2/LongTerm_Z_BLRMS_100_300mHz{0}.gwf'.format(suffix))
        
    # Finish!
    log.debug('Finish!')
