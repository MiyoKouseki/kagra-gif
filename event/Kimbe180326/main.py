#
#! coding:utf-8

import sys 
import numpy as np
import miyopy.io.reader as reader
import miyopy.plot as mpplot

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

def getKimbeDataGIFseis(name='Kimbe',option='P-Wave'):
    if option=='P-Wave':
        start,tlen = 400*16,100 # count = 2**4 sec
    elif option=='All':
        start,tlen = 0,2**16        
    date_ = '2018-03-26 18:57:00'
    print start,tlen
    print date_
    EX1_NS = -1*reader.gif('2018-03-26 18:57:00',120,'X1500_TR240velEW')[40*200:140*200]*1.0/1196.5
    exit()
    TR240_EW = read(date_,120,'X1500_TR240velEW')
    TR240_NS = read(date_,120,'X1500_TR240velNS')[40*200:140*200]*1.0/1196.5
    TR_240_UD = read(date_,120,'X1500_TR240velUD')[40*200:140*200]*1.0/1196.5
    CMG3T_EW = read(date_,120,'X1500_CMG3TvelEW')[40*200:140*200]*1.0/2000.0
    CMG3T_NS = read(date_,120,'X1500_CMG3TvelNS')[40*200:140*200]*1.0/2000.0
    CMG3T_UD = read(date_,120,'X1500_CMG3TvelUD')[40*200:140*200]*1.0/2000.0
    time = np.arange(len(TR240_EW))/200.0    
    data = [[time,TR240_NS],[time,TR240_EW],[time,TR_240_UD],
            [time,CMG3T_NS],[time,CMG3T_EW],[time,CMG3T_UD],
            [np.nan,np.nan],[np.nan,np.nan],[np.nan,np.nan],
            ]
    title = ['X1500_TR240velNS','X1500_TR240velEW','X1500_TR240velUD',
             'X1500_CMG3TvelNS','X1500_CMG3TvelEW','X1500_CMG3TvelUD',
             np.nan,np.nan,np.nan
             ]
    start = 1234
    duration = 1234
    return data,title,start,duration
    
def get3seis3axis(start,tlen):
    '''
    3つの地震計の3つの軸の信号を取得してくる。
    '''    
    EX1_NS = -1*reader.kagra(start,tlen,'K1:PEM-EX1_SEIS_WE_SENSINF_OUT16')
    EY1_NS = -1*reader.kagra(start,tlen,'K1:PEM-EY1_SEIS_NS_SENSINF_OUT16')
    IY0_NS = -1*reader.kagra(start,tlen,'K1:PEM-IY0_SEIS_WE_SENSINF_OUT16')
    EX1_WE = -1*reader.kagra(start,tlen,'K1:PEM-EX1_SEIS_NS_SENSINF_OUT16')
    EY1_WE = -1*reader.kagra(start,tlen,'K1:PEM-EY1_SEIS_WE_SENSINF_OUT16')
    IY0_WE = -1*reader.kagra(start,tlen,'K1:PEM-IY0_SEIS_NS_SENSINF_OUT16')
    EX1_Z = 1*reader.kagra(start,tlen,'K1:PEM-EX1_SEIS_Z_SENSINF_OUT16')
    EY1_Z = 1*reader.kagra(start,tlen,'K1:PEM-EY1_SEIS_Z_SENSINF_OUT16')
    IY0_Z = 1*reader.kagra(start,tlen,'K1:PEM-IY0_SEIS_Z_SENSINF_OUT16')
    time = np.arange(len(EX1_NS))/16.0
    #
    data = [[time,EX1_NS],[time,EX1_WE],[time,EX1_Z],
            [time,IY0_NS],[time,IY0_WE],[time,IY0_Z],
            [time,EY1_NS],[time,EY1_WE],[time,EY1_Z]]    
    label = ['EX1_NS','EX1_WE','EX1_Z',
             'IY0_NS','IY0_WE','IY0_Z',
             'EY1_NS','EY1_WE','EY1_Z']    
    return data,label
    
if __name__ == '__main__':
    argvs = sys.argv
    if (len(argvs) != 3):
        print 'Usage: # python %s <EQname> <WaveName>' % argvs[0]
        quit()
    elif(len(argvs) != 2):
        name,option= argvs[1],argvs[2]        
    if option=='P-Wave':
        start,tlen = 1206093078+400,100 # count = 2**4 sec
        title = '{0}_{1}_{2}_{3}'.format(name,option,start,tlen)
    elif option=='All':
        start,tlen = 0,2**16
        title = '{0}_{1}_{2}_{3}'.format(name,option,start,tlen)
    #
    #data,label = get3seis3axis(start,tlen)
    #mpplot.subplot33(data,'3SEIS_{0}.png'.format(title),label)
    data,title,start,tlen = getKimbeDataGIFseis(name,option)
    mpplot.subplot33(data,'GIF_{0}.png'.format(title),label)
    
