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

from mpio import fetch_data, dump, load
import mpplot
from _timeseries import *
    
class TimeSeries():
    def __init__(self,start,duration):       
        self.chlst_fname = '1.chlst'
        self.start = start
        self.duration = duration
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
        print(start,end)
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
        print(pickle_fname)
        data = load(pickle_fname)
        return data

    def dumpData_pickle(self,data):
        pickle_fname = '../../data/{0}_{1}_{2}.pickle'.format(
            self.start,
            self.duration,
            self.chlst_fname.split('.chlst')[0]
            )
        self.start,self.duration = is_record_in_fw0(self.start,self.duration)
        dump(pickle_fname,data)        
