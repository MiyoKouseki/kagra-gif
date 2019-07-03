import subprocess
import os
import numpy as np
import traceback

from gwpy.segments import Segment,SegmentList
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.frequencyseries import FrequencySeries
from gwpy.spectrogram import Spectrogram

from lib.channel import get_seis_chname
from lib.io import fname_gwf,fname_png_ts,fname_png_asd,fname_hdf5_sg
import lib.logger
log = lib.logger.Logger(__name__)

    

def _save_longterm_spectrogram(axis,idnum,fname,**kwargs):
    '''
    '''
    prefix = kwargs.pop('prefix','./data')
    specgrams = Spectrogram.read(fname[0],format='hdf5')
    for fname in fname[1:]:
        try:
            specgrams.append(Spectrogram.read(fname,format='hdf5'),gap='ignore')        
        except:
            log.debug(traceback.format_exc())
            raise ValueError('AAAA')
    fname_hdf5 = prefix + '/SG_LongTerm_{0}_{1}.hdf5'.format(axis,idnum)
    log.debug('{0} Combined'.format(fname_hdf5))
    specgrams.write(fname_hdf5,format='hdf5',overwrite=True)
    log.debug('{0} Saved'.format(fname_hdf5))
    

def save_longterm_spectrogram(axis,available,prefix='./data',**kwargs):
    fname = [prefix+'/{0}_{1}_{2}.hdf5'.format(axis,start,end) for start,end in available]
    divnum = 4
    try:
        bins = int(len(fname)/divnum)
        fnamelist = [fname[bins*i:bins*(i+1)] for i in range(0,divnum)]
        fnamelist.append(fname[bins*divnum:])
        n = len(fname)
        if n-(divnum*bins)!=len(fnamelist[-1]):
            log.debug('{0}-{1}*{2} != {3}'.format(n,divnum,bins,len(fnamelist[-1])))
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!!!!')
    for idnum,fname in enumerate(fnamelist):
        log.debug('{0}/({1}) {2}-axis'.format(idnum+1,len(fnamelist),axis))
        _save_longterm_spectrogram(axis,idnum,fname)

def _check_skip(segmentlist,fnames):
    exists = [os.path.exists(fname) for fname in fnames]
    saved = [segmentlist[i] for i,exist in enumerate(exists) if exist]
    log.debug('{0}(/{1}) are existed.'.format(len(saved),len(segmentlist)))
    if len(saved)==len(segmentlist):
        log.debug('So, Do nothing.')
        return []
    not_checked = [segmentlist[i] for i,exist in enumerate(exists) if not exist]
    return not_checked

def _save_spectrogram(sg,fname_hdf5):
    sg.write(fname_hdf5,format='hdf5',overwrite=True)
    log.debug(fname_hdf5,'Saved')


def fname_hdf5(segment,prefix):
    start,end = segment
    fname_hdf5_fmt = fname_hdf5_sg(start,end,prefix,axis='{axis}')
    fnamelist = [fname_hdf5_fmt.format(axis=axis) for axis in ['X','Y','Z']]
    return fnamelist

def _calc_spectrogram(data,segment,**kwargs):
    write  = kwargs.pop('write',False)
    write = False
    prefix = kwargs.pop('prefix','./data')
    sglist = [d.spectrogram2(**kwargs)**(1/2.) for d in data.values()]
    if write:
        fnamelist = fname_hdf5(segment,prefix)
        #[_save_spectrogram(sg,fname) for fname,sg in zip(fnamelist,sglist)]
        #[_save_averaged_asd(sg,fname) for fname,sg in zip(fnamelist,sglist)]
    return sglist

def save_spectrogram(segmentlist,fftlength=2**10,overlap=2**9,**kwargs):
    '''
    
    '''    
    log.debug('Save spectrograms')
    lackofdata = SegmentList()
    prefix = kwargs.pop('prefix','./data')
    write = kwargs.pop('write',True)
    skip = kwargs.pop('skip',False)

    fnames = [fname_png_asd(start,end,prefix) for start,end in segmentlist]
    not_checked = _check_skip(segmentlist,fnames)

    log.debug('{0}(/{1}) are not checked'.format(len(not_checked),len(segmentlist)))
    log.debug('Save spectrograms..')
    for i,segment in enumerate(not_checked):
        try:
            fname = fname_gwf(start,end,prefix)
            chname = get_seis_chname(segment[0],segment[1])
            data = TimeSeriesDict.read(fname,chname,**kwargs)
            data = data.crop(segment[0],segment[1])
        except:
            log.debug(traceback.format_exc())
            raise ValueError('No such data {0}'.format(fname))
        # plot
        kwargs['fftlength'] = fftlength
        kwargs['overlap'] = overlap
        sglist = _calc_spectrogram(data,segment,**kwargs)
        asdlist = [sg.percentile(50) for sg in sglist]
        fname = fname_png_asd(segment[0],segment[1],prefix)
        plot_asd(asdlist,fname,**kwargs)
        log.debug('{0:03d}/{1:03d} {2} '.format(i,len(segmentlist),fname)+'Plot')




def save_asd(axis,available,percentile=50,**kwargs):
    prefix = kwargs.pop('prefix','./data')
    write = kwargs.pop('write',None)
    write_gwf = kwargs.pop('write_gwf',None)
    skip = kwargs.pop('skip',None)

    asd_fmt = '{0}/{1}_{2:02d}_LongTerm.hdf5'.format(prefix,axis,percentile)
    if os.path.exists(asd_fmt):
        #log.debug(asd_fmt+' Read')
        return FrequencySeries.read(asd_fmt,format='hdf5')

    log.debug(asd_fmt+' Saving {0:02d} percentile'.format(percentile))
    fnamelist = [prefix+'/{0}_{1}_{2}.hdf5'.format(axis,start,end) for start,end in available]  
    specgrams = Spectrogram.read(fnamelist[0],format='hdf5')
    [specgrams.append(Spectrogram.read(fname,format='hdf5'),gap='ignore') \
     for fname in fnamelist]
    asd = specgrams.percentile(percentile)
    asd.write(asd_fmt,format='hdf5',overwrite=True)
    return asd
