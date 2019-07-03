import traceback
#from tqdm import tqdm
import lib.logger
log = lib.logger.Logger(__name__)
from lib import io
import Kozapy.utils as koza
from channel import get_seis_chname
from gwpy.timeseries import TimeSeriesDict

def write(data,fname,**kwargs):
    '''
    '''
    if io.existance(fname):
        return 'Exist'

    try:
        data.write(fname,format='gwf.lalframe')
        return 'Wrote'
    except:
        log.debug(traceback.format_exc())            
        raise RuntimeError('AAAAAA')

    
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
    fname = io.fname_gwf(start,end,prefix)
    chname = get_seis_chname(start,end)
    sources = koza.filelist(start,end)
    try:
        data = TimeSeriesDict.read(sources,chname,**kwargs)
        data = data.resample(sample_freq)
        data = data.crop(start,end)
        [d.override_unit('ct') for d in data.values()]
        assert None not in [d.name for d in data.values()], 'not exit!'
        _ans = write(data,fname)
        ans = 'OK. {0}'.format(_ans)
    except ValueError as e:
        data = None
        if 'units do not match:' in e.args[0]:
            ans = 'NoData[ValueError1]'
        elif 'Cannot append discontiguous TimeSeries' in e.args[0]:
            ans = 'NoData[ValueError2]'
        else:
            log.debug(traceback.format_exc())
            ans = 'NoData[ValueError0]'
    except IndexError as e:
        data = None
        if 'list index out of range' in e.args[0]:
            ans = 'NoData[IndexError1]'
        elif 'Creation of unknown checksum type' in e.args[0]:
            ans = 'NoData[IndexError2]'
        elif 'Missing FrEndOfFile structure' in e.args[0]:
            ans = 'NoData[IndexError3]'
        else:
            log.debug(traceback.format_exc())
            ans = 'NoData[IndexError0]'
    except:
        log.debug(traceback.format_exc())
        raise ValueError('Unknown error. Please comfirm.')

    ans = '{0} {1} {2}'.format(headder,fname,ans)
    log.debug(ans)
    return data,ans


def check_nodata(segmentlist,prefix='./data',write=True,**kwargs):
    ''' 
    
    '''
    log.debug('Save timeseriesdict..')
    exists = io.existance(segmentlist,ftype='gwf')

    # already checked
    checked = [segmentlist[i] for i,exist in enumerate(exists) if exist]
    log.debug('{0}(/{1}) segments are existed.'.format(len(checked),len(segmentlist)))
    if len(checked)==len(segmentlist):
        log.debug('Then, all segments are existed.')
        return segmentlist,nodata

    # not checked
    not_checked = [segmentlist[i] for i,exist in enumerate(exists) if not exist]
    log.debug('{0}(/{1}) are not checked'.format(len(not_checked),len(segmentlist)))
    n = len(not_checked)
    #ans = [_check_nodata(segment,**kwargs)[1] for segment in not_checked]
    ans = [_check_nodata(segment,headder='{0:04d}(/{1:04d})'.format(i,n),**kwargs)[1] for i,segment in enumerate(not_checked)]
    log.debug(ans)

    # nodata segments
    from gwpy.segments import SegmentList
    nodata = SegmentList([not_checked[i] for i,_ans in enumerate(ans) if 'NoData' in _ans])
    # exist segments
    exist = diff(segmentlist,nodata)
    if len(exist)==0:
        log.debug('No data are existed...')
        raise ValueError('No data Error.')

    if write:
        exist.write('./segmentlist/exist.txt')
        nodata.write('./segmentlist/nodata.txt')

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
    fname = io.fname_gwf(start,end,prefix)
    chname = get_seis_chname(start,end)    
    try:
        data = TimeSeriesDict.read(fname,chname,verbose=False,**kwargs)
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


def check_baddata(seglist,prefix='./data',write=True,**kwargs):
    '''

    '''
    log.debug('Checking bad segments')
            
    exists = io.existance(segmentlist,ftype='png_ts')
    checked = [seglist[i] for i,exist in enumerate(exists) if exist]
    not_checked = [seglist[i] for i,exist in enumerate(exists) if not exist]
    
    bad = SegmentList()
    eq = SegmentList()
    for i,segment in enumerate(seglist):
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
        fname_img = io.fname_png_ts(start,end,prefix)
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
