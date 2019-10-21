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

import matplotlib.pyplot as plt
from dataquality.dataquality import remake

''' Seismic Noise
'''

#------------------------------------------------------------
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

    Returns
    -------
    asd : `gwpy.frequencyseries.FrequencySeries`
        amplitude spectrum density.

    '''
    asd = specgrams.percentile(percentile)
    suffix = kwargs.pop('suffix','')
    prefix = kwargs.pop('prefix','')
    fname = fname_hdf5_percentile(axis,percentile,suffix=suffix,prefix=prefix)
    log.debug(fname)
    asd.write(fname,format='hdf5',overwrite=True)
    return asd


def mean(specgrams,axis,**kwargs):
    ''' Calculate a percentile with given spectrogram of seismometer
        in specified axis.    
    '''
    asd = specgrams.mean(axis=0)
    write = kwargs.pop('write',True)
    suffix = kwargs.pop('suffix','')
    prefix = kwargs.pop('prefix','')
    if write:
        fname = fname_hdf5_percentile(axis,'mean',suffix=suffix,prefix=prefix)
        log.debug(fname)
        asd.write(fname,format='hdf5',overwrite=True)
    return asd


def get_array2d(start,end,axis='X',place='EXV',**kwargs):
    ''' Get Spectrogram    

    Parameters
    ----------
    start
    end

    Returns
    -------


    '''
    nproc = kwargs.pop('nproc',3)
    bandpass = kwargs.pop('bandpass',None)
    fftlen = kwargs.pop('fftlen',2**8)

    if isinstance(place,str):
        fname_hdf5 = fname_hdf5_asd(start,end,prefix='./data/'+place,axis=axis)
        diffasd = False
    elif isinstance(place,list):
        fname_hdf5 = fname_hdf5_diffasd(start,end,prefix='./data/'+'_'.join(place),axis=axis)
        place,place2 = place
        diffasd = True

    # Load specgram from hdf5 file
    if os.path.exists(fname_hdf5):
        specgram = Spectrogram.read(fname_hdf5,format='hdf5')
        if bandpass:
            timeseries = specgram.crop_frequencies(bandpass[0],bandpass[1]).sum(axis=1)
            return timeseries
        else:
            return specgram

    # If no file, make specgram from timeseries data
    try:        
        chname = get_seis_chname(start,end,axis=axis,place=place)[0]
        fnamelist = existedfilelist(start,end)
        data = TimeSeries.read(fnamelist,chname,nproc=nproc)
        data = data.resample(32)
        data = data.crop(start,end)
        if diffasd:
            chname2 = get_seis_chname(start,end,axis=axis,place=place2)[0]
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
        specgram.write(fname_hdf5,format='hdf5',overwrite=True)
        log.debug('Make {0}'.format(fname_hdf5))
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!!')

    return specgram


def get_arrays(use,blrms=False,**kwargs):
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
    return x_array2ds,y_array2ds,z_array2ds




if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--start',type=int,default=1211817600)
    parser.add_argument('--end',type=int,default=1245372032)
    parser.add_argument('--nproc',type=int,default=8)
    parser.add_argument('--percentile', action='store_false') # default True
    parser.add_argument('--remakedb', action='store_true') # default False
    args = parser.parse_args()
    nproc = args.nproc
    run_percentile = args.percentile
    remakedb = args.remakedb
    # ------------------------------------------------------------
    # Get segments
    # ------------------------------------------------------------
    from dataquality.dataquality import DataQuality
    fmt_total = 'select startgps,endgps from {2} WHERE ' +\
                '(startgps>={0} and endgps<={1})'
    fmt_gauss = 'select startgps,endgps from {2} WHERE flag=0 and ' +\
                '(startgps>={0} and endgps<={1})'
    fmt_gauss_day   = 'select startgps,endgps from {2} WHERE flag=0 and ' +\
                      '(startgps>={0} and endgps<={1}) and ' +\
                      '(((startgps-18)%86400)>=0) and (((startgps-18)%86400)<43200)'
    fmt_gauss_night = 'select startgps,endgps from {2} WHERE flag=0 and ' +\
                      '(startgps>={0} and endgps<={1}) and ' +\
                      '(((startgps-18)%86400)>=43200) and (((startgps-18)%86400)<86400)'
    fmt_gauss_summer = 'select startgps,endgps from {2} ' +\
                       'WHERE flag=0 ' +\
                       'and ((startgps>=1211814018 and endgps<=1219676418) ' +\
                       'or (startgps>=1243350018 and endgps<=1251212418)) '   #2019
    fmt_gauss_autumn = 'select startgps,endgps from {2} ' +\
                       'WHERE flag=0 ' +\
                       'and ((startgps>=1219762818 and endgps<=1227538818) ' +\
                       'or (startgps>=1251298818 and endgps<=1259074818)) '   #2019
    fmt_gauss_winter = 'select startgps,endgps from {2} ' +\
                       'WHERE flag=0' +\
                       ' and ((startgps>=1227625218 and endgps<=1235314818)' +\
                       ' or (startgps>=1259161218 and endgps<=1266850818))'   #2019
    fmt_gauss_spring = 'select startgps,endgps from {2} ' +\
                       'WHERE flag=0 ' +\
                       ' and ((startgps>=1203865218 and endgps<=1211727618)' +\
                       ' or (startgps>=1235401218 and endgps<=1243263618))'   #2019
    fmt_gauss_mult = 'select {2}.startgps,{2}.endgps from {2} '+\
                     'INNER JOIN {3} ON ({2}.startgps ={3}.startgps) '+\
                     'WHERE ({2}.flag=0 and {3}.flag=0 ) and '+\
                     '({2}.startgps>={0} and {2}.endgps<={1})'

    with DataQuality('./dataquality/dqflag.db') as db:
        total = db.ask(fmt_total.format(args.start,args.end,'EXV_SEIS'))
        gauss = db.ask(fmt_gauss.format(args.start,args.end,'EXV_SEIS'))
        gauss_day   = db.ask(fmt_gauss_day.format(args.start,args.end,'EXV_SEIS'))
        gauss_night = db.ask(fmt_gauss_night.format(args.start,args.end,'EXV_SEIS'))    
        gauss_winter = db.ask(fmt_gauss_winter.format(args.start,args.end,'EXV_SEIS'))
        gauss_spring = db.ask(fmt_gauss_spring.format(args.start,args.end,'EXV_SEIS'))
        gauss_autumn = db.ask(fmt_gauss_autumn.format(args.start,args.end,'EXV_SEIS'))
        gauss_summer = db.ask(fmt_gauss_summer.format(args.start,args.end,'EXV_SEIS'))
        gauss = db.ask(fmt_gauss.format(args.start,args.end,'IXVTEST_SEIS'))
        gauss = db.ask(fmt_gauss.format(args.start,args.end,'IXV_SEIS'))
        gauss = db.ask(fmt_gauss_mult.format(args.start,args.end,'IXV_SEIS','IXVTEST_SEIS'))
    if remakedb:
        #if True:
        with open('./result.txt','a') as f:
            for i,(start,end) in enumerate(total):
                ans = check(start,end,plot=False,place='EYV',axis='X',
                            nproc=nproc,tlen=4096,cl=0.05,sample_rate=16)
                fmt = '{3:03d}/{4:03d} {0} {1} {2}'
                txt = fmt.format(start,end,ans,i+1,len(total))
                log.debug(txt)
                _txt = '{0} {1} {2}'.format(start,end,ans)
                f.write(_txt+'\n')
        exit()

    # ------------------------------------------------------------
    # Main
    # ------------------------------------------------------------
    use = gauss
    blrms = False
    fftlen = 2**8
    sample_rate = 16
    if not blrms:
        kwargs = {'nproc':nproc}
    else:
        bandpass = 0.2 # 1/3 oct bandpass
        low  = bandpass/(2**(1./6)) # 1/6 oct 
        high = bandpass*(2**(1./6)) # 1/6 oct
        kwargs = {'nproc':nproc,'bandpass':[low,high]}
    # 
    place = 'EXV'
    place = 'IXV'
    place = 'IXVTEST'
    place = ['IXV','IXVTEST']
    place = ['EXV','IXV']
    x_array2ds,y_array2ds,z_array2ds = get_arrays(use,blrms=blrms,place=place)
    #exit()

    # Main : Percentile
    if isinstance(place,list):
        place = place[0]+'DIFF'
    if run_percentile and not blrms:
        suffix = '_{start}_{end}'.format(start=args.start,end=args.end)
        for pctl in [1,5,10,50,90,95,99]:
            save_percentile(x_array2ds,pctl,'X',suffix=suffix,prefix='{0}/'.format(place))
            save_percentile(y_array2ds,pctl,'Y',suffix=suffix,prefix='{0}/'.format(place))
            save_percentile(z_array2ds,pctl,'Z',suffix=suffix,prefix='{0}/'.format(place))
        mean(x_array2ds,'X',suffix=suffix,prefix='{0}/'.format(place))
        mean(y_array2ds,'Y',suffix=suffix,prefix='{0}/'.format(place))
        mean(z_array2ds,'Z',suffix=suffix,prefix='{0}/'.format(place))

    # Main : BLRMS
    if blrms:
        import astropy.units as u
        x_array2ds *= 1./(fftlen)*u.Hz*1.5 # enbw with hanning
        x_array2ds = x_array2ds**0.5
        suffix = '_{start}_{end}'.format(start=args.start,end=args.end)
        fmt = './data2/LongTerm_{0}_BLRMS_{1}mHz{2}.gwf'
        low,high = kwargs['bandpass']
        fname = fmt.format('X',int(bandpass*1000),suffix)
        x_array2ds.write(fname)
        log.debug(fname)
        y_array2ds *= 1./256*u.Hz*1.5 # enbw with hanning
        y_array2ds = y_array2ds**0.5
        fname = fmt.format('Y',int(bandpass*1000),suffix)
        y_array2ds.write(fname)
        log.debug(fname)
        z_array2ds *= 1./256*u.Hz*1.5 # enbw with hanning
        z_array2ds = z_array2ds**0.5
        fname = fmt.format('Z',int(bandpass*1000),suffix)
        z_array2ds.write(fname)
        log.debug(fname)        

    # Finish!
    log.debug('Finish!')
