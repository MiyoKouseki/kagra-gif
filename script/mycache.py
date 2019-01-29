#
#!/usr/bin/env python2
import os
import numpy as np
import re

is_this_gomi = lambda _fname: (_fname[0] == '.' ) or (_fname[-3]!='gwf')


fullcache_fmt = 'K K1_C {gps} {dt} file://{basedir}/full/{gpsdir}/K-K1_C-{gps}-{dt}.gwf'
trendcache_fmt = 'K K1_M {gps} {dt} file://{basedir}/trend/minute/{gpsdir}/K-K1_M-{gps}-{dt}.gwf'
DT = 100000
dt = 32


def fullcache(gst,get,basedir='/data',cachelist=[]):
    ''' get cache 
    
    Parameter
    ---------
    gst : int
        gps start time.
    get : int
        gps end time.
    basedir : str
        place where full locate.

    Return
    ------
    cachelist : list of str
        cache list.
    
    '''
    gps_from = gst - (gst%32)
    gps_to = get - (get%32)
    gps_list = np.arange(gps_from,gps_to+1,32)

    for gps in gps_list:
        gpsdir = int(gps/DT)
        txt = fullcache_fmt.format(gps=gps,dt=dt,basedir=basedir,gpsdir=gpsdir)
        cachelist.append(txt)

    return cachelist


def trendcache(gst,get,basedir='/trend',cachelist=[]):
    ''' get cache 
    
    Parameter
    ---------
    gst : int
        gps start time.
    get : int
        gps end time.
    basedir : str
        place where full locate.

    Return
    ------
    cachelist : list of str
        cache list.
    
    '''
    gps_from = gst - (gst%3600)
    gps_to = get - (get%3600)
    gps_list = np.arange(gps_from,gps_to+1,3600)
    
    for gps in gps_list:
        gpsdir = int(gps/DT)
        txt = trendcache_fmt.format(gps=gps,dt=3600,basedir=basedir,gpsdir=gpsdir)
        path = txt[28:]        
        path = txt.split(' ')[4].replace('file://','')
        if os.path.exists(path):
            cachelist.append(txt)

    return cachelist


if __name__ == '__main__':
    #gst = 1222354818 # UTC 2018-09-30T15:00:00
    #gst = 1219762818 # UTC 2018-08-31T15:00:00
    #gst = 1219795218 # Sep01
    gst = 1209168018 # May01
    #get = 1224082818 # UTC 2018-10-20T15:00:00
    #get = 1225065618 # Nov01
    get = 1231977618 # Jan20
    cachefile = './xarmcomms.cache'
    #cachelist = fullcache(gst,get,basedir='/data/')
    cachelist = trendcache(gst,get,basedir='/data/')
    # 12220
    # 
    with open(cachefile,'w') as f:
        f.write('\n'.join(cachelist)+'\n')
