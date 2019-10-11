import numpy as np
import traceback
#from tqdm import tqdm
import lib.logger
log = lib.logger.Logger(__name__)
from lib import iofunc
import Kozapy.utils.filelist as existedfilelist
from channel import get_seis_chname
from gwpy.timeseries import TimeSeriesDict
import os
from plot import plot_timeseries

def diff(segmentlist,nodata):
    '''
    '''
    from gwpy.segments import SegmentList
    new = SegmentList()    
    for segment in segmentlist:
        flag = 0
        for _nodata in nodata:
            if segment != _nodata:
                flag += 1
            else:
                break
        if flag==len(nodata):
            new.append(segment)
    return new


def write(data,fname,**kwargs):
    '''
    '''
    if iofunc.existance(fname):
        return 'Exist'

    try:
        data.write(fname,format='gwf.lalframe')
        return 'Wrote'
    except:
        log.debug(traceback.format_exc())      
        raise RuntimeError('AAAAAA')


def lack_gwf(start,end):
    gwflist = existedfilelist(start,end)
    if not gwflist:
        return True
    else:
        diffs = np.diff([int(gwf.split('-')[2]) for gwf in  gwflist])
        lackofgwf = False in [32==diff for diff in diffs]
        return lackofgwf

def broken_gwf(start,end):
    return False

def _check_nodata(segment,sample_freq=32,headder='',prefix='./data',**kwargs):
    '''

    Parameters
    ----------
    sources : list of str
        Path to sources. 
    chname :  list of str
        Channel names. It's passed to 
    sample_freq : int
    
    '''    
    start,end = segment
    fname = iofunc.fname_gwf(start,end,prefix)

    if lack_gwf(start,end):
        data,ans = None,'Nodata [noGWF]'
        ans = '{0} {1} {2}'.format(headder,fname,ans)
        log.debug(ans)
        return data,ans
    
    if broken_gwf(start,end):
        data,ans = None, 'Nodata [Broken]'
        return data,ans

    chname = get_seis_chname(start,end)
    sources = existedfilelist(start,end)
    try:
        data = TimeSeriesDict.read(sources,chname,format='gwf.lalframe',**kwargs)
        data = data.resample(sample_freq)
        data = data.crop(start,end)
        [d.override_unit('ct') for d in data.values()]
        assert None not in [d.name for d in data.values()], 'not exit!'
        _ans = write(data,fname)
        ans = 'OK. {0}'.format(_ans)
    except ValueError as e:
        data = None
        if 'need more than 0 values to unpack' in e.args[0]:
            ans = 'NoData [ValueError1]'
            log.debug('{0}, {1}'.format(start,end))
            log.debug(traceback.format_exc())
            exit()
        else:
            log.debug(traceback.format_exc())
            ans = 'NoData [ValueError]'
            raise ValueError('Unknown error. Please confirm.')
    except RuntimeError as e:
        data = None
        if 'Internal function call failed: I/O error' in e.args[0]:
            ans = 'NoData [Broken]'
            ''' Could not read because of broken file!!!!
            $ FrChannels /data/full/12132/K-K1_C-1213232928-32.gwf
            *** Error reading frame from file /data/full/12132/K-K1_C-1213232928-32.gwf
            *** FrError: in FrVectRead : Record length error: nBytes=3136930 nBytesR=2989154 length=147813           
            *** FrError: in FrameRead  missing dictionary
            *** FrError: in FrameRead Read Error
            '''
        elif 'Wrong name' in e.args[0]:
            ans = 'NoData [noChannel?]'
        else:
            log.debug(traceback.format_exc())
            ans = 'NoData [RuntimeError]'
            raise RuntimeError('Unknown error. Please confirm.')
    except TypeError as e:
        data = None
        if "'NoneType' object is not iterable" in e.args[0]:
            ans = 'NoData [noChannel]'
        else:
            log.debug(traceback.format_exc())
            ans = 'NoData [TypeError]'
            raise TypeError('Unknown error. Please confirm.')
    except:
        log.debug(traceback.format_exc())
        raise RuntimeError('Unknown error. Please confirm.')

    ans = '{0} {1} {2}'.format(headder,fname,ans)
    log.debug(ans)
    return data,ans


def check_nodata(segmentlist,prefix='./data',write=True,skip=False,**kwargs):
    ''' 
    
    '''
    from gwpy.segments import SegmentList
    if not skip:
        log.debug('Find segments')
        # find unchecked segments
        exists = iofunc.existance(segmentlist,ftype='gwf')
        not_checked = [segmentlist[i] for i,exist in enumerate(exists) if not exist]
        log.debug('{0}(/{1}) are not checked'.format(len(not_checked),len(segmentlist)))
        n = len(not_checked)
        #ans = [_check_nodata(segment,**kwargs)[1] for segment in not_checked]
        ans = [_check_nodata(segment,headder='{0:04d}(/{1:04d})'.format(i,n),**kwargs)[1] for i,segment in enumerate(not_checked)]        
        # nodata segments
        nodata = SegmentList([not_checked[i] for i,_ans in enumerate(ans) if 'NoData' in _ans])
    else:
        nodata   = SegmentList.read('./segmentlist/nodata.txt')

    # exist segments
    exist = diff(segmentlist,nodata)

    if len(exist)==0:
        log.debug('No data are existed...')
        raise ValueError('No data Error.')

    if write:
        exist.write('./segmentlist/exist.txt')
        nodata.write('./segmentlist/nodata.txt')
        log.debug('./segmentlist/exist.txt Saved')
        log.debug('./segmentlist/nodata.txt Saved')

    log.debug('{0} segments are existed'.format(len(exist)))
    return exist,nodata


def _check_baddata(segment,data=None,prefix='./data',**kwargs):
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
    fname = iofunc.fname_gwf(start,end,prefix)
    fname = existedfilelist(start,end)
    chname = get_seis_chname(start,end)    
    try:
        data = TimeSeriesDict.read(fname,chname,verbose=False,**kwargs)
        lack_of_data = any([0.0 in d.value for d in data.values()] )*4
        miss_calib = any([ 1000.0 < d.mean().value for d in data.values()])*8
        bigeq = any([any((d.std()*6).value < (d-d.mean()).abs().value) for d in data.values()])*16
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


def check_baddata(segmentlist,prefix='./data',write=True,plot=True,**kwargs):
    '''

    '''
    log.debug('Checking bad segments')
            
    exists = iofunc.existance(segmentlist,ftype='png_ts')
    checked = [segmentlist[i] for i,exist in enumerate(exists) if exist]
    not_checked = [segmentlist[i] for i,exist in enumerate(exists) if not exist]
    
    from gwpy.segments import SegmentList
    bad = SegmentList()
    eq = SegmentList()
    for i,segment in enumerate(segmentlist):
        data,bad_status = _check_baddata(segment,**kwargs)
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
        fname_img = iofunc.fname_png_ts(start,end,prefix)
        log.debug('{0:03d}/{1:03d} {2} {3}'.format(i,len(segmentlist),fname_img,bad_status))
        chname = get_seis_chname(start,end)
        #if plot and not os.path.exists(fname_img):
        #    plot_timeseries(data,start,end,bad_status,fname_img)
    # 
    new = SegmentList()    
    for segment in segmentlist:
        flag = 0
        for _bad in bad:
            if segment != _bad:
                flag += 1
            else:
                break
        if flag==len(bad):
            new.append(segment)
    segmentlist = new
    new = SegmentList()    
    for segment in segmentlist:
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

    
