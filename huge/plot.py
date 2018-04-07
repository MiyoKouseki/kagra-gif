#
#! coding:utf-8

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
    
if __name__ == '__main__':
    name = 'Kimbe'
    gpsstart = EQ_name[name][0]
    duration = EQ_name[name][1]
    pm = TimeSeries(gpsstart,duration)
    data = pm.loadData_pickle()
    #
    start,end = 0,2**16
    #start,end = 2**13,2**15
    start,end = 2**14+2**12,2**14+2**14
    #start,end = 8000,10000
    EX1_NS = data[pm.chdic['K1:PEM-EX1_SEIS_WE_SENSINF_OUT16']][start:end]
    EY1_NS = data[pm.chdic['K1:PEM-EY1_SEIS_NS_SENSINF_OUT16']][start:end]
    IY0_NS = data[pm.chdic['K1:PEM-IY0_SEIS_WE_SENSINF_OUT16']][start:end]
    #
    EX1_WE = data[pm.chdic['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16']][start:end]
    EY1_WE = data[pm.chdic['K1:PEM-EY1_SEIS_WE_SENSINF_OUT16']][start:end]
    IY0_WE = data[pm.chdic['K1:PEM-IY0_SEIS_NS_SENSINF_OUT16']][start:end]
    #
    EX1_Z = data[pm.chdic['K1:PEM-EX1_SEIS_Z_SENSINF_OUT16']][start:end]
    EY1_Z = data[pm.chdic['K1:PEM-EY1_SEIS_Z_SENSINF_OUT16']][start:end]
    IY0_Z = data[pm.chdic['K1:PEM-IY0_SEIS_Z_SENSINF_OUT16']][start:end]    
    time = np.arange(len(EX1_NS))/16.0
    #
    data = [[time,EX1_NS],[time,EX1_WE],[time,EX1_Z],
            [time,IY0_NS],[time,IY0_WE],[time,IY0_Z],
            [time,EY1_NS],[time,EY1_WE],[time,EY1_Z]]    
    title = ['EX1_NS','EX1_WE','EX1_Z',
             'IY0_NS','IY0_WE','IY0_Z',
             'EY1_NS','EY1_WE','EY1_Z']
    i,k = 0,1
    #plt.plot(data[1][0],data[1][1],label=title[1],alpha=1)
    #plt.plot(data[4][0],data[4][1],label=title[4],alpha=0.7)
    #plt.plot(data[7][0],data[7][1],label=title[7],alpha=0.5)
    #plt.subplot(131)
    #plt.plot(data[1][1],data[4][1],label=title[1]+'-'+title[4])
    #plt.legend()
    #plt.subplot(132)
    #plt.plot(data[1][1],data[7][1],label=title[1]+'-'+title[7])
    #plt.legend()    
    #plt.subplot(133)
    plt.plot(data[0][1],data[2][1],label=title[0]+'-'+title[2])
    plt.legend()
    plt.savefig('hoge.png')
    plt.close()
    plt.plot(data[2][0],data[2][1],label=title[2],alpha=1)
    plt.plot(data[0][0],data[0][1],label=title[0],alpha=1)
    plt.legend()
    plt.savefig('hoge_.png')
    plt.close()
    #mpplot.subplot33(data,'{0}_{1}.png'.format(name,gpsstart),title)
