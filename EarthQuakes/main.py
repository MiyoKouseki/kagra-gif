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

'''
memo
M5.2, 2018-03-27-06:39:10(UTC), 1206167968, WS of Iwo Jima, Japan
M6.6, 2018-03-26-09:51:00(UTC), 1206093078, Kimbe, Papua New Guinea
M6.4, 2018-03-25-20:14:47(UTC), 1206044105, NW of Saumlaki, Indonesia
M5.0, 2018-03-25-15:36:24(UTC), 1206027402, SE of Hachijo-jima, Japan
'''

class EarthQuake():
    def __init__(self):       
        self.chlst_fname = '1.chlst'
        self.start = 1206093078 # Kimbe
        #self.start = 1206044105 # Saumlaki 
        #self.start = 1206167968 # Iwo No data
        #self.start = 1206027402 # Hachi
        self.duration = 32*32 # sec
        self._loadchlst()
        
    def _loadchlst(self):
        '''
        使用するデータのチャンネルを".chlst"ファイルから取得する           
        '''
        with open(self.chlst_fname,'r') as f:
            self.chlst = f.read().splitlines()    
            self.chdic = {str(ch):i for i,ch in enumerate(self.chlst)}

    def loadData_nds(self):
        start = self.start
        end = self.start + self.duration
        print start,end
        data = fetch_data(start,end,self.chlst)
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

    def dumpData_pickle(self,data):
        pickle_fname = '../../data/{0}_{1}_{2}.pickle'.format(
            self.start,
            self.duration,
            self.chlst_fname.split('.chlst')[0]
            )
        self.start,self.duration = is_record_in_fw0(self.start,self.duration)
        dump(pickle_fname,data)        

if __name__ == '__main__':
    pm = EarthQuake()
    data = pm.loadData_pickle()
    #data = pm.loadData_nds()
    #pm.dumpData_pickle(data)
