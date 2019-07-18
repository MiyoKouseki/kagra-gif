import lib.logger
log = lib.logger.Logger(__name__)

import traceback
import numpy as np
from gwpy.segments import Segment,SegmentList


from lib.channel import get_seis_chname
from lib.plot import plot_asd,plot_timeseries # kesu!
from lib import iofunc
from check import check_nodata,check_baddata

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


def random_segments(start,end,bins=4096,nseg=10,seed=3434,**kwargs):
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
    bins : `int`, optional
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
    ini = range(start,end,bins)
    _start = np.array([ ini[randint(0,len(ini))] for i in range(0,nseg)])
    _end = _start + bins
    segmentlist = SegmentList(map(Segment,zip(_start,_end)))

    if write:
        segmentlist.write('./segmentlist/random.txt')

    return segmentlist


def divide_segmentlist(start,end,bins=4096,write=True,**kwargs):
    ''' Divide given period to segmenlist
    
    Parameters
    ----------
    start : `int`
        GPS start time of given period
    end : `int`
        GPS end time of given period
    bins : `int`, optional
        The number of bins. Unit is second. Default value is 4096 =(2**12).

    Returns
    -------
    segmentlist : `gwpy.segment.SegmentList`
        Divided segmentlist
    '''
    if ((end-start) % bins) != 0:
        raise ValueError('Not divisible!')

    _start = range(start     ,end     ,bins)
    _end   = range(start+bins,end+bins,bins)
    segmentlist = SegmentList([Segment(s,e) for s,e in zip(_start,_end)])
    log.debug(segmentlist[0])
    log.debug(segmentlist[-1])
    if write:
        segmentlist.write('./segmentlist/total.txt')
    return segmentlist






def read_segmentlist(total,skip=True,**kwargs):
    '''
    '''
    if skip:
        log.debug('Skip chekking segment')
        total  = SegmentList.read('./segmentlist/total.txt')
        none   = SegmentList.read('./segmentlist/nodata.txt')
        good   = SegmentList.read('./segmentlist/available.txt')
        lack   = SegmentList.read('./segmentlist/lackofdata.txt')
        glitch = SegmentList.read('./segmentlist/glitch.txt')
    else:
        good,none        = check_nodata(total,skip=True,**kwargs)
        good,lack,glitch = check_baddata(good,**kwargs)
        log.debug('Checking done. Close.')
        exit()
    if not (len(total)-len(none)-len(lack)-len(glitch)==len(good)):
        log.debug('SegmentListError!')
        raise ValueError('Missmatch SegmentLists!')
    return good,none,lack,glitch

