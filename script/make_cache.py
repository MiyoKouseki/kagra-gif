#!/usr/bin/env python2
#! coding:utf-8
import os
import numpy as np
import re
import warnings

''' FullとTrendのキャッシュファイルをつくるスクリプト
'''

is_this_gomi = lambda _fname: (_fname[0] == '.' ) or (_fname[-3]!='gwf')

fullcache_fmt = 'K K1_C {gps} {dt} file://{basedir}/full/{gpsdir}/K-K1_C-{gps}-{dt}.gwf'
trendcache_fmt = 'K K1_M {gps} {dt} file://{basedir}/trend/minute/{gpsdir}/K-K1_M-{gps}-{dt}.gwf'
DT = 100000
dt = 32


def fullcache(gst,get,basedir='/data',check_existance=False):
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
    
    cachelist = []
    for gps in gps_list:
        gpsdir = int(gps/DT)
        txt = fullcache_fmt.format(gps=gps,dt=dt,basedir=basedir,gpsdir=gpsdir)
        path = txt.split('file://')[1]        
        if check_existance and os.path.exists(path):
            cachelist.append(txt)
        elif check_existance and not os.path.exists(path):
            raise IOError('"{0}" is not exist'.format(path))            
        else:
            warnings.warn("Existance is not checked!")
            cachelist.append(txt)            
                
    print 'Make full cache file'
    print ' - Start : ',cachelist[0].split('file://')[1]
    print ' - End   : ',cachelist[-1].split('file://')[1]
    return cachelist


def trendcache(gst,get,basedir='/trend',check_existance=False):
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
    
    cachelist = []    
    for gps in gps_list:
        gpsdir = int(gps/DT)
        txt = trendcache_fmt.format(gps=gps,dt=3600,basedir=basedir,gpsdir=gpsdir)
        path = txt.split('file://')[1]
        if check_existance and os.path.exists(path):
            cachelist.append(txt)
        elif check_existance and not os.path.exists(path):
            raise IOError('"{0}" is not exist'.format(path))
        else:
            warnings.warn("Existance is not checked!")            
            cachelist.append(txt)            

    print 'Make trend cache file'
    print ' - Start : ',cachelist[0].split('file://')[1]
    print ' - End   : ',cachelist[-1].split('file://')[1]            
    return cachelist


if __name__ == '__main__':
    import argparse
    from gwpy.time import tconvert
    parser = argparse.ArgumentParser(description='Make a cache file.')
    parser.add_argument('type', help='choose "full" or "trend"')
    parser.add_argument('start', help='start time')
    parser.add_argument('end', help='end time')
    parser.add_argument('-c', '-check_existance',help='check existance',action='store_true')
    args = parser.parse_args()
    start = tconvert(args.start)
    end = tconvert(args.end)
    kwargs = {}
    kwargs['check_existance'] = args.c
    kwargs['basedir'] = '/data'
    #
    if args.type == 'full':
        cachelist = fullcache(start,end,**kwargs)
        cachefile = './full.cache'                    
    elif args.type == 'trend':
        cachelist = trendcache(start,end,**kwargs)
        cachefile = './trend.cache'            
    else:
        raise ValueError('Invalid frame type; {0}'.fomrat(args.type))
    #
    print("Saved on {0}".format(cachefile))
    with open(cachefile,'w') as f:
        f.write('\n'.join(cachelist)+'\n')
