#!/usr/bin/env python
# coding:utf-8
from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert

from kagraread import read


if __name__ == '__main__':
    start = tconvert('Oct 20 00:00:00').gpsSeconds
    end = tconvert('Oct 20 00:10:00').gpsSeconds
    ch = 'K1:PEM-EXV_SEIS_NS_SENSINF_INMON'
    
    data = read('K-K1_C-1224029408-32.gwf',start,end,ch)
    data.write('K-K1_C-1224029408-32_forTest.gwf',format='gwf.lalframe')
    print data
    print type(data)
    
