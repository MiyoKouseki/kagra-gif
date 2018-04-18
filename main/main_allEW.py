#
#! coding:utf-8

import sys 
import numpy as np
from scipy import signal
import miyopy.io.reader as reader
import miyopy.plot.mpplot as mpplot
import subprocess
from scipy.signal import spectral
#import miyopy.types.timeseries as mpdata
from miyopy import types as mptypes

'''
memo
M5.8, 2018-04-08-14:32:34(UTC), 1207240372, W of Tottori, Japan
M5.2, 2018-03-27-06:39:10(UTC), 1206167968, WS of Iwo Jima, Japan
M6.6, 2018-03-26-09:51:00(UTC), 1206093078, Kimbe, Papua New Guinea
M6.4, 2018-03-25-20:14:47(UTC), 1206044105, NW of Saumlaki, Indonesia
M5.0, 2018-03-25-15:36:24(UTC), 1206027402, SE of Hachijo-jima, Japan
'''    

def R(theta):
    theta = np.deg2rad(float(theta))
    mat = np.array([
        [np.cos(theta),-1*np.sin(theta),0.],
        [np.sin(theta),np.cos(theta),0.],
        [0.,0.,1.]
    ])
    return mat


def main_getGPStime():
    '''イベントを指定して、そのイベントの期間を返す関数。    

    Return
    ------
    start : int
       開始時刻。GPS時刻。
    tlen : int
       期間。秒。
    '''
    EQ_name = {
        'Tottori':[1207240372,2**12],
        'Tottori_P-Wave':[1207240372,2**12],
        'Kimbe':[1206093078,32*2*64],
        'Kimbe_P-Wave':[1206093078+440,2**7],
        'Kimbe_S-Wave':[1206093078+800,2**11],
        'Kimbe_S-Wave':[1206093078+1200,2**9],
        'Kimbe_Other-Wave':[1206093078+1200,2**11],        
        'Saumlaki':[1206044105,32*2*32],
        'Hachijo-jima':[1206027402,32*2*64],
        'Example_MidNight':[1207407618,2**10], # 4/10 24:00
        'Example_MidNight':[1207407618,2**10], # 4/10 24:00
        'Example_MidNight2':[1207411218,2**10], # 4/10 25:00
        'Example_MidNight_Long':[1207234818,2**15], # 4/08 24:00        
        'Example_MidNight_Long2':[1207152018,2**16], # 4/08 24:00
        'Example_Night_Long':[1207213218,2**15], # 4/08 24:00
        'Example_Long_1day':[1207440018,2**16], # 04/11 09:00, 18hour
        #'Example_Long_1day':[1207440018,2**10], # 04/11 09:00, 18hour
        '0416_00h00m':[1207839618,2**14]
        #'hoge':[1207440018,2**6], # 04/11 09:00, 18hour
    }
    try:
        event = sys.argv[1]
        option = sys.argv[2]
        start, tlen = EQ_name[event]
        title = '../event/{0}'.format(event)
    except IndexError as e:
        print type(e),e
        print 'Please add event. ex, python main.py <EQname>'
        print '\n'.join(EQ_name.keys())
        print 'exit...'
        exit()
    except KeyError as e:
        print type(e),e
        print '{0} is not in EQ_name.'.format(e)
        print 'Please use argvs bellow;'
        print '\n'.join(EQ_name.keys())
        exit()
    return start,tlen,title,option


def get3seis3axis(start,tlen,title,option,theta=0.0):
    '''
    3つの地震計の3つの軸の信号を取得してくる。
    '''
    fs = 8.0    
    EX1_SEIS = reader.kagra(start,tlen,['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16','K1:PEM-EX1_SEIS_WE_SENSINF_OUT16','K1:PEM-EX1_SEIS_Z_SENSINF_OUT16']).T    
    EY1_SEIS = reader.kagra(start,tlen,['K1:PEM-EY1_SEIS_WE_SENSINF_OUT16','K1:PEM-EY1_SEIS_NS_SENSINF_OUT16','K1:PEM-EY1_SEIS_Z_SENSINF_OUT16']).T
    IY0_SEIS = reader.kagra(start,tlen,['K1:PEM-IY0_SEIS_NS_SENSINF_OUT16','K1:PEM-IY0_SEIS_WE_SENSINF_OUT16','K1:PEM-IY0_SEIS_Z_SENSINF_OUT16']).T 
    #
    Xend_NSEW = np.array(map(lambda x:np.dot(x,R(30.+theta)),EX1_SEIS))
    Yend_NSEW = np.array(map(lambda x:np.dot(x,R(210.+theta)),EY1_SEIS))
    Cent_NSEW = np.array(map(lambda x:np.dot(x,R(30.+theta)),IY0_SEIS))
    #
    Xend_EW, Xend_NS, Xend_UD = Xend_NSEW.T
    Cent_EW, Cent_NS, Cent_UD = Cent_NSEW.T
    Yend_EW, Yend_NS, Yend_UD = Yend_NSEW.T
    time = np.arange(len(Xend_EW))/fs
    data = [[time,Xend_EW],[time,Xend_NS],[time,Xend_UD],
            [time,Cent_EW],[time,Cent_NS],[time,Cent_UD],
            [time,Yend_EW],[time,Yend_NS],[time,Yend_UD]]    
    label = ['Xend2F_EW','Xend2F_NS','Xend2F_UD',
             'Cent1F_EW','Cent1F_NS','Cent1F_UD',
             'Yend2F_EW','Yend2F_NS','Yend2F_UD']
    #
    print 'tlen',tlen
    fname = '{0}/{1}_{2}_{3}.png'.format(title,start,tlen,option)
    # mkdir 
    cmd = 'mkdir -p {0}'.format(title)
    print cmd
    ret  =  subprocess.check_call( cmd.split(" ") )
    # plot timeseries
    mpplot.subplot33(data,fname,label)
    #plt.plot(data)
    #plt.savefig('hoge.png')
    #plt.close()
    return data,label


if __name__ == '__main__':
    start,tlen,title,option = main_getGPStime()
    #get3seis3axis(start,tlen,title,option)
    #
    import matplotlib.pyplot as plt
    chnames = ['K1:PEM-EY1_SEIS_NS_SENSINF_OUT16',
               'K1:PEM-EY1_SEIS_WE_SENSINF_OUT16',
               'K1:PEM-EY1_SEIS_Z_SENSINF_OUT16']        
    EY1_SEIS = reader.kagra(start,
                            tlen,
                            chnames,
                            detrend='constant'
                            ).T
    chnames = ['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16',
               'K1:PEM-EX1_SEIS_WE_SENSINF_OUT16',
               'K1:PEM-EX1_SEIS_Z_SENSINF_OUT16']        
    EX1_SEIS = reader.kagra(start,
                            tlen,
                            chnames,
                            detrend='constant'
                            ).T
    chnames = ['K1:PEM-IY0_SEIS_NS_SENSINF_OUT16',
               'K1:PEM-IY0_SEIS_WE_SENSINF_OUT16',
               'K1:PEM-IY0_SEIS_Z_SENSINF_OUT16']        
    IY0_SEIS = reader.kagra(start,
                            tlen,
                            chnames,
                            detrend='constant'
                            ).T
    print len(IY0_SEIS)
    TR240_EW = reader.gif(start,tlen,'X1500_TR240velEW',)
    TR240_NS = reader.gif(start,tlen,'X1500_TR240velNS',)
    TR240_UD = reader.gif(start,tlen,'X1500_TR240velUD',)
    TR240_EW = TR240_EW/1196.5
    TR240_NS = TR240_NS/1196.5
    TR240_UD = TR240_UD/1196.5
    TR240_SEIS = np.array([TR240_EW,TR240_NS,TR240_UD]).T
    print len(TR240_SEIS)
    for theta in np.arange(0,180,1):
        print theta
        Yend_NSEW = np.array(map(lambda x:np.dot(x,R(210+theta)),EY1_SEIS))
        Xend_NSEW = np.array(map(lambda x:np.dot(x,R(120+theta)),EX1_SEIS))
        Center_NSEW = np.array(map(lambda x:np.dot(x,R(120+theta)),IY0_SEIS))
        TR240_NSEW = np.array(map(lambda x:np.dot(x,R(theta)),TR240_SEIS))
        Yend_EW, Yend_NS, Yend_UD = Yend_NSEW.T
        Xend_EW, Xend_NS, Xend_UD = Xend_NSEW.T
        Center_EW, Center_NS, Center_UD = Center_NSEW.T
        TR240_EW, TR240_NS, TR240_UD = TR240_NSEW.T        
        Yend_EW = mptypes.Timeseries(Yend_EW,fs=8,name='Yend_EW')
        Xend_EW = mptypes.Timeseries(Xend_EW,fs=8,name='Xend_EW')
        Center_EW = mptypes.Timeseries(Center_EW,fs=8,name='Center_EW')
        TR240_EW = mptypes.Timeseries(TR240_EW,fs=8,name='TR240_EW',plot=False)        
        Yend_EW.get_psd(ave=16,plot=False)
        Xend_EW.get_psd(ave=16,plot=False)
        Center_EW.get_psd(ave=16,plot=False)
        TR240_EW.get_psd(ave=16,plot=False)        
        #mpplot.LogLogPlot([Yend_EW,Yend_EW,Yend_EW],lim=(None,[1e-11,1e-7]),filename='./{0:03d}'.format(theta))
        mpplot.LogLogPlot([Yend_EW,Xend_EW,Center_EW,TR240_EW],lim=(None,[1e-11,1e-7]),filename='./XYC_TR240_EW/{0:03d}'.format(theta))
        #plt.plot(Yend_EW._time,Yend_EW.timeseries)
        #plt.savefig('hoge.png')    
