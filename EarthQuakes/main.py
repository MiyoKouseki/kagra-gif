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

class EarthQuake():
    def __init__(self):       
        self.chlst_fname = '1.chlst'
        self.start = 1205810784 # 03/23 12
        self.start = 1204969376 # 03/13 10:00:00 (UTC)
        self.duration = 23040 # sec
        self._loadchlst()
        
    def _loadchlst(self):
        '''
        使用するデータのチャンネルを".chlst"ファイルから取得する           
        '''
        with open(self.chlst_fname,'r') as f:
            self.chlst = f.read().splitlines()    
            self.chdic = {str(ch):i for i,ch in enumerate(self.chlst)}

    def loadData_nds(self):
        data = fetch_data(self.chlst)
        return data
            
    def loadData_pickle(self):
        '''
        データをpickleから読み込む。
        '''
        pickle_fname = '../../data/{0}_{1}_{2}.pickle'.format(
            self.start,
            self.duration,
            self.chlst_fname.split('.chlst')[0]
            )
        self.start,self.duration = is_record_in_fw0(self.start,self.duration)
        data = load(pickle_fname)        

if __name__ == '__main__':
    pm = EarthQuake()
    pm.loadData_pickle()
