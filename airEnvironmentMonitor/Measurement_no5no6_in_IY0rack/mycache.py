#
#!/usr/bin/env python2

from os import listdir
import numpy as np
import re
from gwpy.time import tconvert

is_this_gomi = lambda _fname: (_fname[0] == '.' ) or (_fname[-3]!='gwf')

cachefmt = 'K K1_C {0} {1} file://{2}/full/{3}/{4}'
DT = 100000
dt = 32

def get_cachelist(gst,get,basedir='/data',cachelist=[]):
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
    gpsdir = sorted([s for s in listdir(basedir+'full') if re.match('[0-9]{5}', s)])
    gpsdir = gpsdir[gpsdir.index(str(gst)[:5]):]
    for _dir in sorted(gpsdir):
        _start = int(_dir) * DT
        _stop  = _start + DT
        fnames = sorted(listdir(basedir+'full/'+_dir))
        fnames = filter(is_this_gomi,fnames)
        for fname in fnames:
            try:
                f_start = int(fname.split('-')[-2])
            except:
                print fname
                exit()
            if (f_start < _start) or (f_start > _stop):
                break
            else:
                cachelist.append(cachefmt.format(f_start,dt,basedir,_dir,fname))
    return cachelist


if __name__ == '__main__':
    # from
    gst = tconvert('Nov 27 12:00:00 2018 JST')
    get = tconvert('Nov 28 09:00:00 2018 JST')
    gst = tconvert('Nov 26 2018 12:00:00 JST') # installed time
    get = tconvert('Nov 27 2018 00:00:00 JST')
    cachefile = './WEATHER_IY0.cache'
    basedir = '/frame0' # in cds computer
    basedir = '/gpfs/data/' # in kashiwa computer
    cachelist = get_cachelist(gst,get,basedir=basedir)
    with open(cachefile,'w') as f:
        f.write('\n'.join(cachelist)+'\n')
