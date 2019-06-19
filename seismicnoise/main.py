

#
from numpy.random import *
import numpy as np

import subprocess
from gwpy.segments import Segment,SegmentList,DataQualityFlag

from gwpy.time import tconvert

def fw_segments(fw_name='fw0'):
    ''' Make dqflag when frame writer save data
    '''
    cmd = 'scp k1ctr7:/users/DGS/Frame/{0}-latest.txt ./ '.format(fw_name)
    #proc = subprocess.call( cmd , shell=True)
    cmd = "less ./{0}-latest.txt".format(fw_name) + " | awk '{if ($4>86400) print $1 , $2}' > "+"tmp_{0}.txt".format(fw_name)
    proc = subprocess.call( cmd , shell=True)
    ok = SegmentList.read('tmp_{0}.txt'.format(fw_name))
    #print ok
    #dqf = DataQualityFlag(name='fw0',active=ok,label='No lack of data')
    cmd = "rm tmp_{0}.txt".format(fw_name)
    proc = subprocess.call( cmd , shell=True)
    return ok


def hoge():
    np.random.seed(seed=3434)
    fw0 = fw_segments(fw_name='fw0')
    
    start = int(tconvert("Feb 01 2019 00:00:00 JST"))
    end = int(tconvert("May 01 2019 00:00:00 JST"))
    tlen = end - start
    n = 200
    _start = start*np.ones(n) + tlen*rand(n)
    _end = _start + 3600    
    ok = SegmentList(map(Segment,zip(_start,_end)))
    _ok = DataQualityFlag(name='random',active=ok,label='random time 1 hour data')
    good = SegmentList([ _ok for _ok in ok if _ok in fw0])
    good.write('availabledata.txt')
    return good


if __name__ == "__main__":
    available = hoge()      
    print available
