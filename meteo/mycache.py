#
#!/usr/bin/env python2

from os import listdir
import numpy as np
import re

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
    gpsdir =  [s for s in listdir(basedir+'full') if re.match('[0-9]{5}', s)]
    for _dir in sorted(gpsdir):
        _start = int(_dir) * DT
        _stop  = _start + DT
        fnames = sorted(listdir(basedir+'full/'+_dir))
        fnames = filter(is_this_gomi,fnames)
        for fname in fnames:
            f_start = int(fname.split('-')[-2])
            if (f_start < _start) or (f_start > _stop):
                break
            else:
                cachelist.append(cachefmt.format(f_start,dt,basedir,_dir,fname))
    return cachelist


if __name__ == '__main__':
    # from
    gst = 1227322818
    get = 1227398418    
    cachefile = './WEATHER_IY0.cache'
    cachelist = get_cachelist(gst,get,basedir='/frame0/')
    with open(cachefile,'w') as f:
        f.write('\n'.join(cachelist)+'\n')
