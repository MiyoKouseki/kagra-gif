#
#! coding: utf-8
from miyopy.gif import findfiles
from astropy import units as u
import numpy as np
import sys

def main():
    argvs = sys.argv
    chname = argvs[1]
    t0 = 1198800018*u.second # 2018-01-01 00:00:00 UTC    
    tlen = 1211846417*u.second - t0 # till 2018-05-31 23:59:59 UTC
    tlen = 3600*24*16*u.second
    #
    fnames = findfiles.findFiles(t0,tlen,chname)
    size = findfiles.check_filesize(fnames,chname)
    array2d = np.c_[fnames,size]
    #
    fmt = '%s %s'
    fname = '{2}_{0}_{1}.csv'.format(int(t0.value),int(tlen.value),chname)
    print 'Save csv data in "{0}"'.format(fname)            
    np.savetxt(fname,array2d,fmt=fmt)

    
if __name__ == '__main__':
    main()
   
