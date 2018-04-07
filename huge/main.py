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

EQ_name = {
    'Kimbe':[1206093078,32*2*64],
    'Saumlaki':[1206044105,32*2*32],
    'Hachijo-jima':[1206027402,32*2*64],
    }

class EarthQuake():
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
        print pickle_fname
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

EQ_name = {
    'Kimbe':[1206093078,32*2*64],
    'Saumlaki':[1206044105,32*2*32],
    'Hachijo-jima':[1206027402,32*2*64],
    }


def mpplot_plot(ax,x,y,xlabel=None,ylabel=None,legend='None'):    
    ax.plot(x,y,label=legend,color='k',linewidth=0.8)
    #ax.set_xlabel(xlabel,fontsize=15)
    #ax.set_ylabel(ylabel,fontsize=15)        
    ax.set_ylim(-5e-5,5e-5)
    ax.grid(color='black', linestyle='--', linewidth=0.6,alpha=0.3)
    ax.legend()
    return ax

def subplot33(data,fname,label):
    fig, ax = plt.subplots(3, 3, figsize=(14, 10))
    fig.suptitle(fname.split('.')[0],fontsize=20)
    ax_ = ax.reshape(1,9)[0]
    for i in range(len(ax_)):
        ax_[i] = mpplot_plot(
            ax_[i],
            data[i][0],
            data[i][1],           
            xlabel='Time',
            ylabel='Value',
            legend=label[i]            
        )        
    for i in filter(lambda x:x<6,range(6)):
        plt.setp(ax_[i].get_xticklabels(),visible=False)
    for i in filter(lambda x:(x%3)!=0,range(9)):
        plt.setp(ax_[i].get_yticklabels(),visible=False)
    for i in filter(lambda x:x==7,range(9)):
        ax_[i].set_xlabel('Time [sec]',fontsize=20)
    for i in filter(lambda x:x==3,range(9)):
        ax_[i].set_ylabel('Velocity [m/sec]',fontsize=20)
    fig.tight_layout(rect=[0, 0, 0.99, 0.95])
    plt.savefig(fname)
    plt.close()    
        
if __name__ == '__main__':
    name = 'Hachijo-jima'
    name = 'Kimbe'
    #name = 'Saumlaki'
    gpsstart = EQ_name[name][0]
    duration = EQ_name[name][1]
    pm = EarthQuake(gpsstart,duration)
    #data = pm.loadData_nds()
    #pm.dumpData_pickle(data)
    #exit()
    data = pm.loadData_pickle()
    #
    start,end = 0,2**16
    start,end = 2**13,2**15
    start,end = 2**11,2**15
    #start,end = 0,4000
    EX1_NS = data[pm.chdic['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16']][start:end]
    EY1_NS = data[pm.chdic['K1:PEM-EY1_SEIS_NS_SENSINF_OUT16']][start:end]
    IY0_NS = data[pm.chdic['K1:PEM-IY0_SEIS_NS_SENSINF_OUT16']][start:end]
    #
    EX1_WE = data[pm.chdic['K1:PEM-EX1_SEIS_WE_SENSINF_OUT16']][start:end]
    EY1_WE = data[pm.chdic['K1:PEM-EY1_SEIS_WE_SENSINF_OUT16']][start:end]
    IY0_WE = data[pm.chdic['K1:PEM-IY0_SEIS_WE_SENSINF_OUT16']][start:end]
    #
    EX1_Z = data[pm.chdic['K1:PEM-EX1_SEIS_Z_SENSINF_OUT16']][start:end]
    EY1_Z = data[pm.chdic['K1:PEM-EY1_SEIS_Z_SENSINF_OUT16']][start:end]
    IY0_Z = data[pm.chdic['K1:PEM-IY0_SEIS_Z_SENSINF_OUT16']][start:end]    
    time = np.arange(len(EX1_NS))/16
    #
    data = [[time,EX1_NS],[time,EX1_WE],[time,EX1_Z],
            [time,IY0_NS],[time,IY0_WE],[time,IY0_Z],
            [time,EY1_NS],[time,EY1_WE],[time,EY1_Z]
            ]    
    title = ['EX1_NS','EX1_WE','EX1_Z','IY0_NS','IY0_WE','IY0_Z','EY1_NS','EY1_WE','EY1_Z',]    
    subplot33(data,'{0}_{1}.png'.format(name,gpsstart),title)
