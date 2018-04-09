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

def getKimbeDataGIFseis(start,tlen):
    TR240_EW = reader.gif(start,tlen,'X1500_TR240velEW')*1.0/1196.5
    TR240_NS = reader.gif(start,tlen,'X1500_TR240velNS')*1.0/1196.5
    TR240_UD = reader.gif(start,tlen,'X1500_TR240velUD')*1.0/1196.5
    CMG3T_EW = reader.gif(start,tlen,'X1500_CMG3TvelEW')*1.0/2000.0
    CMG3T_NS = reader.gif(start,tlen,'X1500_CMG3TvelNS')*1.0/2000.0
    CMG3T_UD = reader.gif(start,tlen,'X1500_CMG3TvelUD')*1.0/2000.0
    time = np.arange(len(TR240_EW))/200.0    
    data = [[time,TR240_NS],[time,TR240_EW],[time,TR240_UD],
            [time,CMG3T_NS],[time,CMG3T_EW],[time,CMG3T_UD],
            [np.nan,np.nan],[np.nan,np.nan],[np.nan,np.nan],
            ]
    label = ['X1500_TR240velNS','X1500_TR240velEW','X1500_TR240velUD',
             'X1500_CMG3TvelNS','X1500_CMG3TvelEW','X1500_CMG3TvelUD',
             np.nan,np.nan,np.nan
             ]
    return data,label
    
def get3seis3axis(start,tlen):
    '''
    3つの地震計の3つの軸の信号を取得してくる。
    '''
    EX1_SEIS = np.array( # EW,NS,UD    
        [reader.kagra(start,tlen,'K1:PEM-EX1_SEIS_NS_SENSINF_OUT16'),
        reader.kagra(start,tlen,'K1:PEM-EX1_SEIS_WE_SENSINF_OUT16'),
        reader.kagra(start,tlen,'K1:PEM-EX1_SEIS_Z_SENSINF_OUT16')]
        ).T
    EY1_SEIS = np.array( # EW,NS,UD
        [reader.kagra(start,tlen,'K1:PEM-EY1_SEIS_WE_SENSINF_OUT16'),
        reader.kagra(start,tlen,'K1:PEM-EY1_SEIS_NS_SENSINF_OUT16'),   
        reader.kagra(start,tlen,'K1:PEM-EY1_SEIS_Z_SENSINF_OUT16')]
        ).T
    IY0_SEIS = np.array( # EW,NS,UD
        [reader.kagra(start,tlen,'K1:PEM-IY0_SEIS_NS_SENSINF_OUT16'),
        reader.kagra(start,tlen,'K1:PEM-IY0_SEIS_WE_SENSINF_OUT16'),   
        reader.kagra(start,tlen,'K1:PEM-IY0_SEIS_Z_SENSINF_OUT16')]
        ).T   
    #
    R_xend = np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])
    R_yend = np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])
    R_cent = np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])
    #
    Xend_NSEW = np.array(map(lambda x:np.dot(x,R_xend),EX1_SEIS))
    Yend_NSEW = np.array(map(lambda x:np.dot(x,R_yend),EY1_SEIS))
    Cent_NSEW = np.array(map(lambda x:np.dot(x,R_cent),IY0_SEIS))
    #
    Xend_EW, Xend_NS, Xend_UD = Xend_NSEW.T
    Cent_EW, Cent_NS, Cent_UD = Cent_NSEW.T
    Yend_EW, Yend_NS, Yend_UD = Yend_NSEW.T
    time = np.arange(len(Xend_EW))/16.0
    data = [[time,Xend_EW],[time,Xend_NS],[time,Xend_UD],
            [time,Cent_EW],[time,Cent_NS],[time,Cent_UD],
            [time,Yend_EW],[time,Yend_NS],[time,Yend_UD]]    
    label = ['Xend_EW','Xend_NS','Xend_UD',
             'Cent_EW','Cent_NS','Cent_UD',
             'Yend_EW','Yend_NS','Yend_UD']    
    return data,label
    
if __name__ == '__main__':
    EQ_name = {
        'Kimbe':[1206093078,32*2*64],
        'Saumlaki':[1206044105,32*2*32],
        'Hachijo-jima':[1206027402,32*2*64],
    }
    #
    argvs = sys.argv
    if (len(argvs) != 3):
        print 'Usage: # python %s <EQname> <WaveName>' % argvs[0]
        quit()
    elif(len(argvs) != 2):
        name,option= argvs[1],argvs[2]
    #    
    if option=='P-Wave':
        start,tlen = 1206093078+400,100 # count = 2**4 sec
        title = '{0}_{1}_{2}_{3}'.format(name,option,start,tlen)
    elif option=='All':
        start,tlen = 0,2**16
        title = '{0}_{1}_{2}_{3}'.format(name,option,start,tlen)
    #
    #data,label = get3seis3axis(start,tlen)
    data,label = getKimbeDataGIFseis(start, tlen)
    #mpplot.subplot33(data,'3SEIS_{0}.png'.format(title),label)    
    mpplot.subplot33(data,'GIF_{0}.png'.format(title),label)
    
