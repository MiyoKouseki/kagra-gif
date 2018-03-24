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
        self.chlst_fname = '1.chlst'
        self.start = 1204969376 # 03/13 10:00:00 (UTC)
        self.duration = 23040 # sec
        with open(self.chlst_fname,'r') as f:
            self.chlst = f.read().splitlines()    
            chdic = {str(ch):i for i,ch in enumerate(self.chlst)}
        
    def loadData(self):        
        pickle_fname = '../../data/{0}_{1}_{2}.pickle'.format(
            self.start,
            self.duration,
            self.chlst_fname.split('.chlst')[0]
            )
        self.start,self.duration = is_record_in_fw0(self.start,self.duration)
        self.data = load(pickle_fname)

    def filtData(self):
        

if __name__ == '__main__':
    pm = ParticleMotion()
    pm.loadData()
    
