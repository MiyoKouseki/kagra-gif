#!/usr/bin/env python
# coding:utf-8
from gwpy.timeseries import TimeSeries
import nds2

def from_nds2_buffer(start,end,ch,**kwargs):
    '''
    
    Parameters
    ----------
    start : float
    end : float


    Returns
    -------
    data : `gwpy.timeseries.timeseries.TimeSeries`
        TimeSeries
    
    '''
    
    conn = nds2.connection('k1nds1', 8088)
    _buffer = conn.fetch(start, end, [ch])[0]   
    return TimeSeries.from_nds2_buffer(_buffer)


def fetch(start,end,ch,**kwargs):
    '''
    
    Parameters
    ----------
    start : float
    end : float


    Returns
    -------
    data : `gwpy.timeseries.timeseries.TimeSeries`
        TimeSeries
    
    '''    
    return TimeSeries.fetch(ch, start, end, host="k1nds0", port=8088)


def read(source,start,end,ch,**kwargs):
    '''
    
    Parameters
    ----------
    source : str
        source file

    start : float
        start gps time

    end : float
        end gps time


    Returns
    -------
    data : `gwpy.timeseries.timeseries.TimeSeries`
        TimeSeries
    
    '''        
    return TimeSeries.read(source, ch, start, end, nproc=2, **kwargs)
