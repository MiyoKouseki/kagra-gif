#
#! coding:utf-8
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib
import numpy as np
from  check_fw import is_record_in_fw0
import sys
sys.path.append("../../../lib/miyopy/miyopy")

from  mpio import fetch_data, dump, load

class ParticleMotion():
    def __init__(self):       
        chlst_fname = '1.chlst'
        #start = 1205201472 # 03/16 11
        start = 1205810784 # 03/23 12
        start = 1204969376 # 03/13 10:00:00 (UTC)
        #duration = 4096 # sec
        duration = 23040 # sec
        #duration = 55872
        pickle_fname = '../../data/{0}_{1}_{2}.pickle'.format(start,duration,chlst_fname.split('.chlst')[0])
        # get chlst
        with open(chlst_fname,'r') as f:
            chlst = f.read().splitlines()    
            chdic = {str(ch):i for i,ch in enumerate(chlst)}
        # get data
        start,duration = is_record_in_fw0(start,duration)
        #data = fetch_data(start,start+duration,chlst)
        #dump(pickle_fname,data)
        data = load(pickle_fname)

if __name__ == '__main__':
    pm = ParticleMotion()
    
