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
        '0416_00h00m':[1207839618,2**14],
        '0416_00h00m':[1207839618,2**12],
        '0413_20h00m':[1207652418,2**14],
        '0413_20h00m':[1207652418,2**13],
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

def getKAGRAseismometer(start,tlen,title,option,theta=0.0,plot33=False,after_28Mar=True,after_12Mar=False,do_you_want_to_calib=True):    
    '''
    3つの地震計の3つの軸の信号を取得してくる。
    '''
    fs = 8.0    
    EX1_SEIS = reader.kagra(start,tlen,['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16','K1:PEM-EX1_SEIS_WE_SENSINF_OUT16','K1:PEM-EX1_SEIS_Z_SENSINF_OUT16']).T    
    EY1_SEIS = reader.kagra(start,tlen,['K1:PEM-EY1_SEIS_WE_SENSINF_OUT16','K1:PEM-EY1_SEIS_NS_SENSINF_OUT16','K1:PEM-EY1_SEIS_Z_SENSINF_OUT16']).T
    IY0_SEIS = reader.kagra(start,tlen,['K1:PEM-IY0_SEIS_NS_SENSINF_OUT16','K1:PEM-IY0_SEIS_WE_SENSINF_OUT16','K1:PEM-IY0_SEIS_Z_SENSINF_OUT16']).T
    if do_you_want_to_calib:
        v = 5500.0
        EX1_SEIS = EX1_SEIS/v
        EY1_SEIS = EY1_SEIS/v
        IY0_SEIS = IY0_SEIS/v    
    if after_28Mar:
        # 3/28 -  , all 210 deg rotation to X arm        
        Xend_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),EX1_SEIS))
        Yend_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),EY1_SEIS))
        Cent_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),IY0_SEIS))
    if after_12Mar:
        # 3/12- 3/28 , Y:180,X:90,C:90.
        Xend_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),EX1_SEIS))
        Yend_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),EY1_SEIS))
        Cent_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),IY0_SEIS))    
    # Rotate EW axis to X-arm.
    Xend_Xarm, Xend_Yarm, Xend_Z = Xend_NSEW.T
    Cent_Xarm, Cent_Yarm, Cent_Z = Cent_NSEW.T
    Yend_Xarm, Yend_Yarm, Yend_Z = Yend_NSEW.T
    time = np.arange(len(Xend_Xarm))/fs   
    # for plotting 3x3 plot
    if plot33:
        data = [[time,Xend_Xarm],[time,Xend_Yarm],[time,Xend_Z],
                [time,Cent_Xarm],[time,Cent_Yarm],[time,Cent_Z],
                [time,Yend_Xarm],[time,Yend_Yarm],[time,Yend_Z]]    
        label = ['Xend2F_Xarm','Xend2F_Yarm','Xend2F_Z',
                'Cent1F_Xarm','Cent1F_Yarm','Cent1F_Z',
                'Yend2F_Xarm','Yend2F_Yarm','Yend2F_Z']
        fname = '{0}/{1}_{2}_{3}.png'.format(title,start,tlen,option)
        cmd = 'mkdir -p {0}'.format(title)
        print cmd
        ret  =  subprocess.check_call( cmd.split(" ") )
        mpplot.subplot33(data,fname,label)
        exit()
    else:
        Yend_Xarm = mptypes.Timeseries(Yend_Xarm,fs=8,name='Yend_x')
        Xend_Xarm = mptypes.Timeseries(Xend_Xarm,fs=8,name='Xend_x')
        Cent_Xarm = mptypes.Timeseries(Cent_Xarm,fs=8,name='Cent_x')
        Yend_Xarm.get_psd(ave=8,plot=False)
        Xend_Xarm.get_psd(ave=8,plot=False)
        Cent_Xarm.get_psd(ave=8,plot=False)
        #
        Yend_Yarm = mptypes.Timeseries(Yend_Yarm,fs=8,name='Yend_x')
        Xend_Yarm = mptypes.Timeseries(Xend_Yarm,fs=8,name='Xend_x')
        Cent_Yarm = mptypes.Timeseries(Cent_Yarm,fs=8,name='Cent_x')
        Yend_Yarm.get_psd(ave=8,plot=False)
        Xend_Yarm.get_psd(ave=8,plot=False)
        Cent_Yarm.get_psd(ave=8,plot=False)
        #
        Yend_Z = mptypes.Timeseries(Yend_Z,fs=8,name='Yend_x')
        Xend_Z = mptypes.Timeseries(Xend_Z,fs=8,name='Xend_x')
        Cent_Z = mptypes.Timeseries(Cent_Z,fs=8,name='Cent_x')
        Yend_Z.get_psd(ave=8,plot=False)
        Xend_Z.get_psd(ave=8,plot=False)
        Cent_Z.get_psd(ave=8,plot=False)        
        print 'get KAGRA data'
        return [[Xend_Xarm,Yend_Xarm,Cent_Xarm],[Xend_Yarm,Yend_Yarm,Cent_Yarm],[Xend_Z,Yend_Z,Cent_Z]]

def getGIFdata(start,tlen,title,option,theta=0.0,plot33=False,after_28Mar=True,after_12Mar=False,do_you_want_to_calib=True):
    TR240_EW = reader.gif(start,tlen,'X1500_TR240velEW',)
    TR240_NS = reader.gif(start,tlen,'X1500_TR240velNS',)
    TR240_UD = reader.gif(start,tlen,'X1500_TR240velUD',)
    v2hPa = 1.0
    v2cdegree = 1.0
    #
    Strain = reader.gif(start,tlen,'CALC_STRAIN',)
    Baro_x500 = reader.gif(start,tlen,'X500_BARO',)*v2hPa*-2e-8
    Baro_x2000 = reader.gif(start,tlen,'X2000_BARO',)*v2hPa*2e-8
    Temp_x500 = reader.gif(start,tlen,'X500_TEMP',)*v2cdegree
    Temp_x2000 = reader.gif(start,tlen,'X2000_TEMP',)*v2cdegree
    TR240_SEIS = np.array([TR240_EW,TR240_NS,TR240_UD]).T
    if do_you_want_to_calib:
        v = 5500.0
        TR240_SEIS = TR240_SEIS/v/1196.5            
    TR240_NSEW = np.array(map(lambda x:np.dot(x,R(-30+theta)),TR240_SEIS))
    TR240_Xarm, TR240_Yarm, TR240_Z = TR240_NSEW.T
    do_you_want_to_calib = True
    #
    Strain = mptypes.Timeseries(Strain,fs=8,name='GIF_X',plot=True)
    TR240_Xarm = mptypes.Timeseries(TR240_Xarm,fs=8,name='X1500_x',plot=True)
    TR240_Yarm = mptypes.Timeseries(TR240_Yarm,fs=8,name='X1500_y',plot=True)
    TR240_Z = mptypes.Timeseries(TR240_Z,fs=8,name='X1500_z',plot=True)
    Baro_x500 = mptypes.Timeseries(Baro_x500,fs=8,name='X500_Pres',plot=True)
    Baro_x2000 = mptypes.Timeseries(Baro_x2000,fs=8,name='X2000_Pres',plot=True)
    Temp_x500 = mptypes.Timeseries(Temp_x500,fs=8,name='X500_Temp',plot=True)
    Temp_x2000 = mptypes.Timeseries(Temp_x2000,fs=8,name='X2000_temp',plot=True)
    #
    Strain.get_psd(ave=8,plot=False)
    Baro_x500.get_psd(ave=8,plot=False)
    Baro_x2000.get_psd(ave=8,plot=False)
    Temp_x500.get_psd(ave=8,plot=False)
    Temp_x2000.get_psd(ave=8,plot=False)    
    TR240_Xarm.get_psd(ave=8,plot=False)
    TR240_Yarm.get_psd(ave=8,plot=False)
    TR240_Z.get_psd(ave=8,plot=False)    
    return Strain,TR240_Xarm,Baro_x500,Baro_x2000,Temp_x500,Temp_x2000


def coherence(x,y):
    import matplotlib.pyplot as plt
    fs = 8
    ave = 8.0
    fname = '{0}-{1}'.format(x._name,y._name)
    f, Cxy = signal.coherence(x.timeseries, y.timeseries, fs, nperseg=len(x.timeseries)/ave)    
    plt.semilogx(f, Cxy,label='{0} / {1}'.format(y._name,x._name))
    #
    clfunc = lambda a: 1.0-(1.0-a/100.0)**(1./(ave-1.0))            
    cl = 99.7 # %    
    plt.plot(f,np.ones(len(f))*clfunc(cl),'k--',linewidth=1,alpha=0.5)
    plt.text(f[1], clfunc(cl)*0.9, '{0:3.2f}%'.format(cl),bbox={'facecolor':'w', 'alpha':0.9, 'pad':0.5},alpha=0.5)
    #
    plt.xlabel('frequency [Hz]')
    plt.ylabel('Coherence')
    plt.legend()
    plt.ylim(0,1)
    plt.savefig('Coherence_{0}.png'.format(fname))
    plt.close()    


if __name__ == '__main__':
    start,tlen,title,option = main_getGPStime()
    theta = 0.0
    data = getKAGRAseismometer(start,tlen,title,option,theta=theta)
    Xend_x,Yend_x,Cent_x = data[0]
    Xend_y,Yend_y,Cent_y = data[1]
    Xend_z,Yend_z,Cent_z = data[2]    
    data = getGIFdata(start,tlen,title,option,theta=theta)
    Strain,TR240_x,Baro_x500,Baro_x2000,Temp_x500,Temp_x2000 = data
    plot_Strain=False
    if plot_Strain:
        data = [Strain,TR240_x,Baro_x500,Baro_x2000]#,Xend_x,Cent_x]
        mpplot.LogLogPlot(data,
                        lim=(None,[0.5e-14,1e-10]),
                        filename='./XarmStrain',
                        label=['Frequency [Hz]','Strain [1/rtHz]']
        )
    plot_Seismometer=False
    if plot_Seismometer:
        data = [TR240_x,Xend_x,Cent_x,Yend_x,Baro_x500]
        mpplot.LogLogPlot(data,
                        lim=(None,[0.5e-14,1e-10]),
                        filename='./AllSeismometer',
                        label=['Frequency [Hz]','Strain [1/rtHz]']
        )        
    coherence(TR240_x,Temp_x500)
    coherence(TR240_x,Baro_x500)
    coherence(TR240_x,Temp_x2000)
    coherence(TR240_x,Baro_x2000)
    coherence(TR240_x,Xend_x)
    coherence(TR240_x,Cent_x)
    coherence(TR240_x,Yend_x)
    #
    coherence(Strain,Temp_x500)
    coherence(Strain,Baro_x500)
    coherence(Strain,Temp_x2000)
    coherence(Strain,Baro_x2000)
    coherence(Strain,TR240_x)
    coherence(Strain,Xend_x)
    coherence(Strain,Cent_x)
    coherence(Strain,Yend_x)
    #
    coherence(Xend_x,Yend_x)
    coherence(Xend_x,Cent_x)
    coherence(Yend_x,Cent_x)
    coherence(Xend_y,Yend_y)
    coherence(Xend_y,Cent_y)
    coherence(Yend_y,Cent_y)
    coherence(Xend_z,Yend_z)
    coherence(Xend_z,Cent_z)
    coherence(Yend_z,Cent_z)
