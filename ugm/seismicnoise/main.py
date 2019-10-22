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


def append_data(segment,blrms=False,**kwargs):
    '''
    '''
    n = len(segment)
    # i = 0
    start,end = segment[0]
    x = get_spectrogram(start,end,axis='X',**kwargs)
    y = get_spectrogram(start,end,axis='Y',**kwargs)
    z = get_spectrogram(start,end,axis='Z',**kwargs)
    # i > 1
    for i,(start,end) in enumerate(segment[1:]):
        _x = get_spectrogram(start,end,axis='X',**kwargs)
        _y = get_spectrogram(start,end,axis='Y',**kwargs)
        _z = get_spectrogram(start,end,axis='Z',**kwargs)
        log.debug('{0:04d}/{1:04d} : Append {2} '.format(i+2,n,start))
        if not blrms: # get Long Spectrogram
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
    from dataquality.dataquality import DataQuality
    fmt_total = 'select startgps,endgps from {2} '+\
                'WHERE (startgps>={0} and endgps<={1})'
    fmt_gauss = 'select startgps,endgps from {2} '+\
                'WHERE flag=0'+\
                ' and (startgps>={0} and endgps<={1})'
    fmt_gauss_night = 'select startgps,endgps from {2} '+\
                      'WHERE flag=0' +\
                      ' and (startgps>={0} and endgps<={1})'+\
                      ' and ((startgps-18)%86400)>=43200'+\
                      ' and ((startgps-18)%86400)<86400'
    fmt_gauss_day   = 'select startgps,endgps from {2} '+\
                      'WHERE flag=0' +\
                      ' and (startgps>={0} and endgps<={1})' +\
                      ' and ((startgps-18)%86400)>=0' +\
                      ' and ((startgps-18)%86400)<43200'
    fmt_gauss_summer = 'select startgps,endgps from {2} ' +\
                       'WHERE flag=0' +\
                       ' and ('+\
                       '(startgps>=1211814018 and endgps<=1219676418) or '+\
                       '(startgps>=1243350018 and endgps<=1251212418)'+\
                       ')'
    fmt_gauss_autumn = 'select startgps,endgps from {2} '+\
                       'WHERE flag=0'+\
                       ' and ('+\
                       '(startgps>=1219762818 and endgps<=1227538818) or '+\
                       '(startgps>=1251298818 and endgps<=1259074818)'+\
                       ')'
    fmt_gauss_winter = 'select startgps,endgps from {2} '+\
                       'WHERE flag=0'+\
                       ' and ('+\
                       '(startgps>=1227625218 and endgps<=1235314818) or '+\
                       '(startgps>=1259161218 and endgps<=1266850818)'+\
                       ')'
    fmt_gauss_spring = 'select startgps,endgps from {2} '+\
                       'WHERE flag=0'+\
                       ' and ('+\
                       '(startgps>=1203865218 and endgps<=1211727618) or ' +\
                       '(startgps>=1235401218 and endgps<=1243263618)'+\
                       ')'
    fmt_gauss_2seis = 'select {2}.startgps,{2}.endgps '+\
                      'from {2} INNER JOIN {3} '+\
                      'ON ({2}.startgps ={3}.startgps) '+\
                      'WHERE ({2}.flag=0 and {3}.flag=0 )'+\
                      ' and ({2}.startgps>={0} and {2}.endgps<={1})'
    with DataQuality('./dataquality/dqflag.db') as db:
        total = db.ask(fmt_total.format(start,end,'EXV_SEIS'))
        day = db.ask(fmt_gauss_day.format(start,end,'EXV_SEIS'))
        night = db.ask(fmt_gauss_night.format(start,end,'EXV_SEIS'))
        winter = db.ask(fmt_gauss_winter.format(start,end,'EXV_SEIS'))
        spring = db.ask(fmt_gauss_spring.format(start,end,'EXV_SEIS'))
        autumn = db.ask(fmt_gauss_autumn.format(start,end,'EXV_SEIS'))
        summer = db.ask(fmt_gauss_summer.format(start,end,'EXV_SEIS'))
        allday_exv = db.ask(fmt_gauss.format(start,end,'EXV_SEIS'))
        allday_ixvtest = db.ask(fmt_gauss.format(start,end,'IXVTEST_SEIS'))
        allday_ixv = db.ask(fmt_gauss.format(start,end,'IXV_SEIS'))
        allday_mce = db.ask(fmt_gauss.format(start,end,'MCE_SEIS'))
        allday_mcf = db.ask(fmt_gauss.format(start,end,'MCF_SEIS'))
        allday_bs = db.ask(fmt_gauss.format(start,end,'BS_SEIS'))
        allday_ixv_ixvtest = db.ask(fmt_gauss_2seis.format(start,end,
                                    'IXV_SEIS','IXVTEST_SEIS'))
        allday_mce_mcf = db.ask(fmt_gauss_2seis.format(start,end,
                                'MCE_SEIS','MCF_SEIS'))
        allday_exv_ixv = db.ask(fmt_gauss_2seis.format(start,end,
                                'EXV_SEIS','IXV_SEIS'))


    if remakedb:
        fname = './dataquality/result_{0}.txt'.format(seis)
        if not os.path.exists(fname.split("result")[0]):
            os.mkdir(fname.split("result")[0])
        with open(fname,'a') as f:
            for i,(start,end) in enumerate(total):
                ans = check(start,end,plot=True,nproc=nproc,
                            seis=seis,axis='X',
                            tlen=4096,sample_rate=16,cl=0.05)
                log.debug('{0:03d}/{1:03d} : {2} {3} {4}'.format(
                    i+1,len(total),start,end,ans))
                f.write('{0} {1} {2}\n'.format(start,end,ans))
    #
    if seis=='EXV':
        segment = allday_exv
    elif seis=='IXV':
        segment = allday_ixv
    elif seis=='IXVTEST':
        segment = allday_ixvtest
    elif seis=='MCE':
        segment = allday_mce
    elif seis=='MCF':
        segment = allday_mcf
    elif seis=='BS':
        segment = allday_bs
    elif seis=='MCE-MCF':
        segment = allday_mce_mcf
    elif seis=='EXV-IXV':
        segment = allday_exv_ixv
    else:
        raise ValueError('Invalid seis name.')

    # ------------------------------------------------------------
    # Percentile
    # ------------------------------------------------------------
    if run_percentile:
        x,y,z = append_data(segment,blrms=False,seis=seis,nproc=nproc)
        if savespecgram:
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
