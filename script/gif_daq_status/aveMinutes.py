#
#! coding:utf-8

import numpy as np
from multiprocessing import Process, Queue

from miyopy.gif.fromfiles import fromfile


_chname = 'CALC_STRAIN'

def aveMinutes(fname):
    data = fromfile(fname,_chname)
    ave = np.average(data)
    return ave


def main():
    t0=1198800019
    from miyopy.gif.findfiles import findFiles
    fnames = findFiles(t0,1e6,_chname)    
    ave = [aveMinutes(fname) for fname in fnames]
    ave = np.array(ave)
    print ave

def main_mp():
    from miyopy.gif.findfiles import findFiles
    fnames = findFiles(1198803017,60*5e4,_chname)
    n = len(fnames)
    i=0
    fnames_0 = fnames[(n/2)*(i):(n/2)*(i+1)]
    i=1
    fnames_1 = fnames[(n/2)*(i):(n/2)*(i+1)]    
    jobs = [
        Process(target=aveMinutes,args=(fnames_0,)),
        Process(target=aveMinutes,args=(fnames_1,))
        ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
        
def main_mp(n=5):
    from miyopy.gif.findfiles import findFiles
    dt = 60*1e6
    jobs = []
    for i in range(n):
        jobs += [Process(target=findFiles,args=(1198803017+i*dt/n,dt/n,_chname,))]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print jobs
    
if __name__ == '__main__':
    main()
    #main_mp()
