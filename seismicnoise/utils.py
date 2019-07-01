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
img_fmt = '{prefix}/ASD_{start}_{end}.png'
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
        segmentlist.write('./segmentlist/base.txt')

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

    checked = [segmentlist[i] for i,exist in enumerate(exists) if exist]
    log.debug('{0}(/{1}) segments are existed.'.format(len(checked),len(segmentlist)))
    if len(checked)==len(segmentlist):
        log.debug('Then, all segments are existed.')
        return segmentlist,nodata

    not_checked = [segmentlist[i] for i,exist in enumerate(exists) if not exist]
    log.debug('{0}(/{1}) segments are not checked before'.format(len(not_checked),len(segmentlist)))
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
    

def _check_badsegment(segment,trend='full',stype='',prefix='./data',nproc=2,**kwargs):
    '''
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
        new.write('./segmentlist/good.txt')    
        bad.write('./segmentlist/bad.txt')    
        eq.write('./segmentlist/eq.txt')
    return new,bad,eq


def read_segmentlist(prefix='./segmentlist'):
    base = SegmentList.read('./segmentlist/base.txt')
    nodata = SegmentList.read('./segmentlist/nodata.txt')
    good = SegmentList.read('./segmentlist/good.txt')
    bad = SegmentList.read('./segmentlist/bad.txt')
    eq = SegmentList.read('./segmentlist/eq.txt')
    fmt = '{0} \t - {1}\t - {2}\t - {3} \t= {4}'
    log.debug(fmt.format('All','None','Lack','EQ','Good'))
    log.debug(fmt.format(len(base),len(nodata),len(bad),len(eq),len(good)))
    if not (len(base)-len(nodata)-len(bad)-len(eq)==len(good)):
        log.debug('SegmentListError!')
        raise ValueError('!')
    return good,nodata,bad,eq


def save_longterm_spectrogram(axis,good,prefix='./data',**kwargs):
    fname = [prefix+'/{0}_{1}_{2}.hdf5'.format(axis,start,end) for start,end in good]
    specgrams = Spectrogram.read(fname[0],format='hdf5')    
    for fname in fname[1:]:
        try:
            specgrams.append(Spectrogram.read(fname,format='hdf5'),gap='ignore')        
        except:
            log.debug(traceback.format_exc())
            raise ValueError('AAAA')
    fname_hdf5 = prefix + '/SG_LongTerm_{0}.hdf5'.format(axis)
    specgrams.write(fname_hdf5,format='hdf5',overwrite=True)
    log.debug('Saved {0}'.format(fname_hdf5))


def save_spectrogram(seglist,plot=True,nproc=2,write=True,nodata=False,trend='full',stype='',prefix='./data',**kwargs):
    '''
    
    '''    
    log.debug('Save spectrograms ')
    bad = SegmentList()
    for i,segment in enumerate(seglist):
        start,end = segment        
        fname = gwf_fmt.format(prefix=prefix,start=start,end=end)
        chname = get_seis_chname(start,end)
        try:
            data = TimeSeriesDict.read(fname,chname,nproc=nproc,verbose=False)
            data = data.crop(start,end)
        except:
            log.debug(traceback.format_exc())
            nodata = True
            raise ValueError('No such data {0}'.format(fname))

        label = [d.replace('_','\_') for d in data]
        fname_img = img_fmt.format(prefix=prefix,start=start,end=end)
        if os.path.exists(fname_img):
            log.debug('{0:03d}/{1:03d} {2} '.format(i,len(seglist),fname_img)+'Exist')
        elif not nodata and plot:
            kwargs={'nproc':nproc}
            fname_hdf5 = sg_fmt.format(prefix=prefix,axis='{axis}',start=start,end=end)
            plot_asd(segment,data,fname_img,fname_hdf5,**kwargs)
            log.debug('{0:03d}/{1:03d} {2} '.format(i,len(seglist),fname_img)+'Plot')
        elif nodata:
            log.debug('{0:03d}/{1:03d} {2} '.format(i,len(seglist),fname_img)+'No Data')
        else:
            raise ValueError('!')




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
        seglist.write('./segmentlist/base.txt')
    
    return seglist


def fw_segments(fw_name='fw0',scp=False):
    ''' Return the segment list when the frame writer could write data.

    Information about when the fw0 write data is given by a text file 
    named "fw0-latest.txt". This text file is generated by a script 
    written by T. Yamamoto. Then we can make a segment list by 
    translating this file.

    MEMO:"fw0-latest.txt" is saved on /users/DGS/Frame.

    Parameters
    ----------
    fw_name : `str`, optional
        Name of the frame writer. KAGRA have a fw0 and fw1. Default is fw0.
    scp : `str`, optional
        If download from control machine, please choose True. In default, False.

    Returns
    -------
    ok : `gwpy.segments.SegmentList`
        SegmentList whihch only contain segments when fw has write data on main strage.
    '''
    if scp:
        cmd = 'scp controls@k1ctr7:/users/DGS/Frame/{0}-latest.txt ./ '.format(fw_name)
        download = subprocess.call(cmd, shell=True)

    cmd = "less ./{0}-latest.txt".format(fw_name) 
    cmd += " | awk '{if ($4>86400) print $1 , $2}' > tmp_{0}.txt".format(fw_name)
    make_tmp_txt = subprocess.call(cmd,shell=True)
    ok = SegmentList.read('tmp_{0}.txt'.format(fw_name))
    remove_tmp_txt = subprocess.call("rm tmp_{0}.txt".format(fw_name), shell=True)
    return ok
