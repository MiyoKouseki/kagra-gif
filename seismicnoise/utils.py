import subprocess
import os
import numpy as np

import logger
log = logger.Logger(__name__)

import traceback


from gwpy.segments import Segment,SegmentList
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.frequencyseries import FrequencySeries
from gwpy.spectrogram import Spectrogram

from plot import plot_asd,plot_timeseries # kesu!

gwf_fmt = '{prefix}/{start}_{end}.gwf'
img_asd_fmt = '{prefix}/ASD_{start}_{end}.png'
img_ts_fmt = '{prefix}/TS_{start}_{end}.png'
sg_fmt = '{prefix}/{axis}_{start}_{end}.hdf5'


def get_seis_chname(start,end,place='EXV'):
    '''
    
    '''
    #K1:PEM-EX1_SEIS_WE_SENSINF_IN1_DQ : 1203897618 - 1216771218 , 2018-03-01T00:00:00 - 2018-07-28T00:00:00
    #K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ : 1216857618 - 1227139218 , 2018-07-29T00:00:00 - 2018-11-25T00:00:00 
    #K1:PEM-EXV_GND_TR120Q_X_IN1_DQ    : 1227571218 - 1232668818 , 2018-11-30T00:00:00 - 2019-01-28T00:00:00  
    #K1:PEM-SEIS_EXV_GND_X_IN1_DQ      : 1232668818 - <>         , 2019-01-28T00:00:00 - <>
    if start > 1232668818:
        chname = ['K1:PEM-SEIS_EXV_GND_EW_IN1_DQ',
                  'K1:PEM-SEIS_EXV_GND_NS_IN1_DQ',
                  'K1:PEM-SEIS_EXV_GND_UD_IN1_DQ']
    elif 1227571218 < start and start < 1232668818:
        chname = ['K1:PEM-EXV_GND_TR120Q_X_IN1_DQ',
                  'K1:PEM-EXV_GND_TR120Q_Y_IN1_DQ',
                  'K1:PEM-EXV_GND_TR120Q_Z_IN1_DQ']
    elif 1216857618 < start and start < 1227139218:
        chname = ['K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ',
                  'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ',
                  'K1:PEM-EXV_SEIS_Z_SENSINF_IN1_DQ']
    elif 1203897618 < start and start < 1227571218:
        chname = ['K1:PEM-EX1_SEIS_WE_SENSINF_IN1_DQ',
                  'K1:PEM-EX1_SEIS_NS_SENSINF_IN1_DQ',
                  'K1:PEM-EX1_SEIS_Z_SENSINF_IN1_DQ']
    else:
        chname = None
    return chname



def random_segments(start,end,tlen=2**12,nseg=10,seed=3434,**kwargs):
    ''' Return segment list randomly in term you designated
    
        
    Parameters
    ----------
    start : `float`
        Start time 
    end : `float`
        End time
    nseg : `int`, optional
        The number of segments
    seed : `int`, optional
        Seed. 3434 is a default value.
    tlen : `int`, optional
        Duration. default is 3600 seconds.    
    write : `Bool`, optional
        If True, segmentlist is written in local directory. Default is True.

    Returns
    -------
    segmentlist : `gwpy.segments.SegmentList`
        SegmentList.
    '''
    from numpy.random import randint

    write = kwargs['write']

    np.random.seed(seed=seed)
    ini = range(start,end,tlen)
    _start = np.array([ ini[randint(0,len(ini))] for i in range(0,nseg)])
    _end = _start + tlen
    segmentlist = SegmentList(map(Segment,zip(_start,_end)))

    if write:
        segmentlist.write('./segmentlist/random.txt')

    return segmentlist

def _check_nodata(sources,chname,start,end,sample_freq=32,**kwargs):
    '''

    Parameters
    ----------
    sources : list of str
        Path to sources. 
    chname :  list of str
        Channel names. It's passed to 
    start : int
    end : int
    sample_freq : int
    
    '''    
    write_gwf = kwargs.pop('write_gwf',False)
    prefix = kwargs.pop('prefix','./tmp')
    try:
        data = TimeSeriesDict.read(sources,chname,**kwargs)
        data = data.resample(sample_freq)
        data = data.crop(start,end)
        assert None not in [d.name for d in data.values()], 'not exit!'
    except ValueError as e:
        log.debug(traceback.format_exc())
        return 'No Data (Channel not found)'
    except RuntimeError as e:       
        log.debug(traceback.format_exc())
        return 'No Data (RunTimeError)'
    except IndexError as e:
        log.debug(traceback.format_exc())
        return 'No Data (Missing frame files)'
    except:
        log.debug(traceback.format_exc())
        raise ValueError('Unknown error. Please comfirm.')
    
    if write_gwf:
        fname = gwf_fname(start,end,prefix)
        data.write(fname,format='gwf.lalframe')
        return 'OK. Now Writting..'
    return 'OK. Exists.'

def gwf_fname(start,end,prefix):
    return gwf_fmt.format(prefix=prefix,start=start,end=end)

def img_ts_fname(start,end,prefix):
    return img_ts_fmt.format(prefix=prefix,start=start,end=end)

def img_asd_fname(start,end,prefix):
    return img_asd_fmt.format(prefix=prefix,start=start,end=end)

def diff(seglist,nodata):
    new = SegmentList()
    for segment in seglist:
        flag = 0
        for _nodata in nodata:
            if segment != _nodata:
                flag += 1
            else:
                break
        if flag==len(nodata):
            new.append(segment)
    return new


def check_nodata(segmentlist,**kwargs):
    ''' 
    
    '''
    log.debug('Save timeseriesdict..')
    from Kozapy.utils import filelist
    skip = kwargs.pop('skip',False)
    check = kwargs.pop('check',True)
    write = kwargs.pop('write',True)
    prefix = kwargs.pop('prefix','./data')
    fnames = [gwf_fname(start,end,prefix) for start,end in segmentlist]
    exists = [os.path.exists(fname) for fname in fnames]

    # 
    checked = [segmentlist[i] for i,exist in enumerate(exists) if exist]
    log.debug('{0}(/{1}) segments are existed.'.format(len(checked),len(segmentlist)))
    if len(checked)==len(segmentlist):
        log.debug('Then, all segments are existed.')
        return segmentlist,nodata
    #
    not_checked = [segmentlist[i] for i,exist in enumerate(exists) if not exist]
    log.debug('{0}(/{1}) are not checked'.format(len(not_checked),len(segmentlist)))
    n = len(not_checked)
    nodata = SegmentList()
    for i,segment in enumerate(not_checked):
        chname = get_seis_chname(segment[0],segment[1])
        sources = filelist(segment[0],segment[1])        
        if check:
            ans = _check_nodata(sources,chname,segment[0],segment[1],**kwargs)
        else:
            ans = 'Skiped. No Data.'
        log.debug('{0:03d}/{1:03d} {2} '.format(i+1,n,fname) + ans)
        if 'No Data' in ans:
            nodata.append(segment)

    exist = diff(segmentlist,nodata)
    if len(exist)==0:
        log.debug('No data are existed...')
        raise ValueError('No data Error.')
    if write:
        exist.write('./segmentlist/exist.txt')
        nodata.write('./segmentlist/nodata.txt')

    log.debug('{0} segments are existed'.format(len(exist)))
    return exist,nodata
    

def _check_badsegment(segment,data=None,**kwargs):
    ''' Check whether given segment is good or not.
    
    1. Read timeseriese data from frame file saved in local place. 
       If data could not be read, return "No Data" flag.
    2. Check lack of data. 
    

    1 bit : no data
    2 bit : lack of data
    3 bit : missed caliblation 
    4 bit : big earthquake
    '''    
    start,end = segment
    fname = gwf_fmt.format(prefix=prefix,start=start,end=end)
    chname = get_seis_chname(start,end)
    try:
        data = TimeSeriesDict.read(fname,chname,nproc=nproc,verbose=False)
        lack_of_data = any([0.0 in d.value for d in data.values()] )*4
        miss_calib = any([ 1000.0 < d.mean() for d in data.values()])*8
        bigeq = any([any((d.std()*6)<(d-d.mean()).abs().value) for d in data.values()])*16
        return data, (lack_of_data + miss_calib + bigeq)
    except IOError as e:
        nodata = (True)*2
        return None, nodata
    except ValueError as e:
        if 'Cannot append discontiguous TimeSeries' in e.args[0]:
            log.debug(e)
            nodata = (True)*2
            return None, nodata
        else:
            log.debug(traceback.format_exc())
            raise ValueError('!!')
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!!')


def check_badsegment(seglist,plot=True,nproc=2,stype='',trend='full',prefix='./data',**kwargs):
    '''

    '''
    log.debug('Checking bad segments')
    
        
    status = {2:'no_data',
              4:'lack_of_data',
              8:'miss_calib',
              16:'big_eq'}

    write = kwargs.pop('write',True)

    prefix = kwargs.pop('prefix','./data')
    fnames = [img_ts_fname(start,end,prefix) for start,end in seglist]
    exists = [os.path.exists(fname) for fname in fnames]
    checked = [seglist[i] for i,exist in enumerate(exists) if exist]
    not_checked = [seglist[i] for i,exist in enumerate(exists) if not exist]
    
    bad = SegmentList()
    eq = SegmentList()
    for i,segment in enumerate(seglist):
        data,bad_status = _check_badsegment(segment,trend='full',stype='',nproc=2,**kwargs)
        if bad_status-16>=0:
            eq.append(segment)
        elif bad_status and not (bad_status-16>=0):
            bad.append(segment)
        elif not bad_status:            
            pass
        else:
            log.debug(bad_status)
            log.debug('!')
            raise ValueError('!')
        start,end = segment
        fname_img = img_ts_fmt.format(prefix=prefix,start=start,end=end)
        log.debug('{0:03d}/{1:03d} {2} {3}'.format(i,len(seglist),fname_img,bad_status))
        chname = get_seis_chname(start,end)
        if plot and not os.path.exists(fname_img):
            plot_timeseries(data,start,end,bad_status,fname_img)
    # 
    new = SegmentList()    
    for segment in seglist:
        flag = 0
        for _bad in bad:
            if segment != _bad:
                flag += 1
            else:
                break
        if flag==len(bad):
            new.append(segment)
    seglist = new
    new = SegmentList()    
    for segment in seglist:
        flag = 0
        for _eq in eq:
            if segment != _eq:
                flag += 1
            else:
                break
        if flag==len(eq):
            new.append(segment)
    if write:
        new.write('./segmentlist/available.txt')    
        bad.write('./segmentlist/lackofdata.txt')
        eq.write('./segmentlist/glitch.txt')
    return new,bad,eq


def read_segmentlist(prefix='./segmentlist'):
    total = SegmentList.read('./segmentlist/total.txt')
    nodata = SegmentList.read('./segmentlist/nodata.txt')
    available = SegmentList.read('./segmentlist/available.txt')
    lackofdata = SegmentList.read('./segmentlist/lackofdata.txt')
    eq = SegmentList.read('./segmentlist/glitch.txt')
    fmt = '{0} \t - {1}\t - {2}\t - {3} \t= {4}'
    log.debug(fmt.format('All','None','Lack','Glitch','Available'))
    log.debug(fmt.format(len(total),len(nodata),len(lackofdata),len(eq),len(available)))
    if not (len(total)-len(nodata)-len(lackofdata)-len(eq)==len(available)):
        log.debug('SegmentListError!')
        raise ValueError('!')
    return available,nodata,lackofdata,eq

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
    fname_hdf5_fmt = sg_fmt.format(prefix=prefix,axis='{axis}',start=start,end=end)
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

def save_spectrogram(segmentlist,fftlength=100,overlap=50,**kwargs):
    '''
    
    '''    
    log.debug('Save spectrograms')
    lackofdata = SegmentList()
    prefix = kwargs.pop('prefix','./data')
    write = kwargs.pop('write',True)
    skip = kwargs.pop('skip',False)

    fnames = [img_asd_fname(start,end,prefix) for start,end in segmentlist]
    not_checked = _check_skip(segmentlist,fnames)

    log.debug('{0}(/{1}) are not checked'.format(len(not_checked),len(segmentlist)))
    log.debug('Save spectrograms..')
    for i,segment in enumerate(not_checked):
        try:
            fname = gwf_fmt.format(prefix=prefix,start=segment[0],end=segment[1])
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
        fname = img_asd_fname(segment[0],segment[1],prefix)
        plot_asd(asdlist,fname,**kwargs)
        log.debug('{0:03d}/{1:03d} {2} '.format(i,len(segmentlist),fname)+'Plot')


def allsegmentlist(start,end,tlen=2**12,**kwargs):
    '''
    
    Parameters
    ----------
    start : `int`
        GPS start time of designated 
    end : `int`
    
    '''
    write = kwargs['write']
    seglist = SegmentList()
    i = 0
    while True:
        if start+(i+1)*tlen >= end:
            break
        else:
            seglist.append(Segment(start+i*tlen,start+(i+1)*tlen))
            i += 1
    if write:
        seglist.write('./segmentlist/total.txt')
    
    return seglist



def save_asd(axis,available,percentile=50,**kwargs):
    prefix = kwargs.pop('prefix','./data')
    write = kwargs.pop('write',None)
    write_gwf = kwargs.pop('write_gwf',None)
    skip = kwargs.pop('skip',None)

    asd_fmt = '{0}/{1}_{2:02d}_LongTerm.hdf5'.format(prefix,axis,percentile)
    if os.path.exists(asd_fmt):
        log.debug(asd_fmt+' Read')
        return FrequencySeries.read(asd_fmt,format='hdf5')

    log.debug(asd_fmt+' Saving {0:02d} percentile'.format(percentile))
    fnamelist = [prefix+'/{0}_{1}_{2}.hdf5'.format(axis,start,end) for start,end in available]  
    specgrams = Spectrogram.read(fnamelist[0],format='hdf5')
    [specgrams.append(Spectrogram.read(fname,format='hdf5'),gap='ignore') \
     for fname in fnamelist]
    asd = specgrams.percentile(percentile)
    asd.write(asd_fmt,format='hdf5',overwrite=True)
    return asd
