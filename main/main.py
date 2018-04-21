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
if False:   
    a = np.array([1,0,0]).T
    print a
    b = np.dot(R(45),a)
    print b
    exit()

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
        '0413_20h00m':[1207652418,2**14],
        '0413_20h00m':[1207652418,2**13], # 2**13 Ok KAGRA,GIF, 2**16made
        '0416_00h00m':[1207839618,2**13],        #2**15made
        '0416_13h00m':[1207886418,2**13], # 2**13 ok 
        '0416_16h00m':[1207897218,2**13], # OK
        '0416_19h00m':[1207908018,2**13], # OK
        '0416_22h00m':[1207918818,2**13], # OK
        '0417_01h00m':[1207929618,2**13], # OK 
        '0417_17h00m':[1207987218,2**13], # OK,2**16 made
        '0417_20h00m':[1207998018,2**13], # OK ,2**16 made
        '0417_23h00m':[1208008818,2**13], # OK ,2**16 made
        '0421chiba':[1208339257-2**10,2**12], 
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


def getGIFdata(start,tlen,title,option,theta=0.0,plot33=False,after_28Mar=True,after_12Mar=False,do_you_want_to_calib=True):
    TR240_EW = reader.gif(start,tlen,'X1500_TR240velEW',)
    TR240_NS = reader.gif(start,tlen,'X1500_TR240velNS',)
    TR240_UD = reader.gif(start,tlen,'X1500_TR240velUD',)
    v2hPa = 1.0
    v2cdegree = 1.0
    #
    Strain = reader.gif(start,tlen,'CALC_STRAIN',)#*1.5e3
    Baro_x500 = reader.gif(start,tlen,'X500_BARO',)*v2hPa*-2e-8
    Baro_x2000 = reader.gif(start,tlen,'X2000_BARO',)*v2hPa*2e-8
    Temp_x500 = reader.gif(start,tlen,'X500_TEMP',)*v2cdegree
    Temp_x2000 = reader.gif(start,tlen,'X2000_TEMP',)*v2cdegree
    TR240_SEIS = np.array([TR240_EW,TR240_NS,TR240_UD]).T
    if True:
        v = 5500.0
        #v = 1
        TR240_SEIS = TR240_SEIS/v/1196.5            
    TR240_NSEW = np.array(map(lambda x:np.dot(x,R(-30+theta)),TR240_SEIS))
    TR240_x, TR240_y, TR240_z = TR240_NSEW.T
    #
    Strain = mptypes.Timeseries(Strain,fs=8,name='GIF_X',plot=True)
    TR240_x = mptypes.Timeseries(TR240_x,fs=8,name='X1500_x',plot=True)
    TR240_y = mptypes.Timeseries(TR240_y,fs=8,name='X1500_y',plot=True)
    TR240_z = mptypes.Timeseries(TR240_z,fs=8,name='X1500_z',plot=True)
    CMRR_timeseries = Xend_x.timeseries - Cent_x.timeseries
    CMRR = mptypes.Timeseries(CMRR_timeseries,fs=8,name='CMRR',plot=True)
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
    CMRR.get_psd(ave=8,plot=False,integ=False)
    TR240_x.get_psd(ave=8,plot=False,integ=False,savefile=True)
    TR240_y.get_psd(ave=8,plot=False,integ=False)
    TR240_z.get_psd(ave=8,plot=False,integ=False)    
    return Strain,TR240_x,Baro_x500,Baro_x2000,Temp_x500,Temp_x2000,CMRR


def getKAGRAseismometer(start,tlen,title,option,theta=0.0,plot33=False,after_28Mar=True,after_12Mar=False,do_you_want_to_calib=True):    
    '''
    3つの地震計の3つの軸の信号を取得してくる。
    '''
    fs = 8.0    
    EX1_SEIS = reader.kagra(start,tlen,['K1:PEM-EX1_SEIS_WE_SENSINF_OUT16','K1:PEM-EX1_SEIS_NS_SENSINF_OUT16','K1:PEM-EX1_SEIS_Z_SENSINF_OUT16']).T    
    IY0_SEIS = reader.kagra(start,tlen,['K1:PEM-IY0_SEIS_WE_SENSINF_OUT16','K1:PEM-IY0_SEIS_NS_SENSINF_OUT16','K1:PEM-IY0_SEIS_Z_SENSINF_OUT16']).T
    EY1_SEIS = reader.kagra(start,tlen,['K1:PEM-EY1_SEIS_WE_SENSINF_OUT16','K1:PEM-EY1_SEIS_NS_SENSINF_OUT16','K1:PEM-EY1_SEIS_Z_SENSINF_OUT16']).T    
    if True:
        v = 5500.0
        EX1_SEIS = EX1_SEIS/v
        EY1_SEIS = EY1_SEIS/v
        IY0_SEIS = IY0_SEIS/v    
    if False:
        Xend_NSEW = EX1_SEIS
        Yend_NSEW = EY1_SEIS
        Cent_NSEW = IY0_SEIS
    if True:
        # 3/28 -  , all 210 deg rotation to X arm
        Xend_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),EX1_SEIS))
        Yend_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),EY1_SEIS))
        Cent_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),IY0_SEIS))        
    if False:
        # 3/12- 3/28 , Y:180,X:90,C:90.
        Xend_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),EX1_SEIS))
        Yend_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),EY1_SEIS))
        Cent_NSEW = np.array(map(lambda x:np.dot(x,R(180.+theta)),IY0_SEIS))    
    # Rotate EW axis to X-arm.
    Xend_x, Xend_y, Xend_z = Xend_NSEW.T
    Cent_x, Cent_y, Cent_z = Cent_NSEW.T
    Yend_x, Yend_y, Yend_z = Yend_NSEW.T
    time = np.arange(len(Xend_x))/fs   
    # for plotting 3x3 plot
    if True:
        data = [[time,Xend_x],[time,Xend_y],[time,Xend_z],
                [time,Cent_x],[time,Cent_y],[time,Cent_z],
                [time,Yend_x],[time,Yend_y],[time,Yend_z]]    
        label = ['Xend2F_x','Xend2F_y','Xend2F_z',
                'Cent1F_x','Cent1F_y','Cent1F_z',
                'Yend2F_x','Yend2F_y','Yend2F_z']
        fname = '{0}/{1}_{2}_{3}.png'.format(title,start,tlen,option)
        cmd = 'mkdir -p {0}'.format(title)
        print cmd
        ret  =  subprocess.check_call( cmd.split(" ") )
        mpplot.subplot33(data,fname,label)
    if True:
        Yend_x = mptypes.Timeseries(Yend_x,fs=8,name='Yend_x')
        Xend_x = mptypes.Timeseries(Xend_x,fs=8,name='Xend_x')
        Cent_x = mptypes.Timeseries(Cent_x,fs=8,name='Cent_x')
        Yend_x.get_psd(ave=8,plot=False,integ=True)
        Xend_x.get_psd(ave=8,plot=False,integ=True)
        Cent_x.get_psd(ave=8,plot=False,integ=True)
        #
        Yend_y = mptypes.Timeseries(Yend_y,fs=8,name='Yend_y')
        Xend_y = mptypes.Timeseries(Xend_y,fs=8,name='Xend_y')
        Cent_y = mptypes.Timeseries(Cent_y,fs=8,name='Cent_y')
        Yend_y.get_psd(ave=8,plot=False,integ=False)
        Xend_y.get_psd(ave=8,plot=False,integ=False)
        Cent_y.get_psd(ave=8,plot=False,integ=False)
        #
        Yend_z = mptypes.Timeseries(Yend_z,fs=8,name='Yend_z')
        Xend_z = mptypes.Timeseries(Xend_z,fs=8,name='Xend_z')
        Cent_z = mptypes.Timeseries(Cent_z,fs=8,name='Cent_z')
        Yend_z.get_psd(ave=8,plot=False,integ=False)
        Xend_z.get_psd(ave=8,plot=False,integ=False)
        Cent_z.get_psd(ave=8,plot=False,integ=False)
        print 'get KAGRA data'
        return [[Xend_x,Yend_x,Cent_x],[Xend_y,Yend_y,Cent_y],[Xend_z,Yend_z,Cent_z]]
    
if __name__ == '__main__':
    
    start,tlen,title,option = main_getGPStime()
    theta = 0.0
    data = getKAGRAseismometer(start,tlen,title,option,theta=theta)
    Xend_x,Yend_x,Cent_x = data[0]
    Xend_y,Yend_y,Cent_y = data[1]
    Xend_z,Yend_z,Cent_z = data[2]    
    data = getGIFdata(start,tlen,title,option,theta=theta)
    Strain,TR240_x,Baro_x500,Baro_x2000,Temp_x500,Temp_x2000,CMRR = data
    #
    if True:
        data = [Strain,TR240_x,Baro_x500,Baro_x2000]#,Xend_x,Cent_x]
        mpplot.LogLogPlot(data,
                        lim=([1e-3,4e0],[0.5e-13,1e-9]),
                        filename='{0}/XarmStrain_{1}_{2}_{3}'.format(title,start,tlen,option),
                        label=['Frequency [Hz]','Strain [1/rtHz]']
        )
    if False:
        data = [Strain,TR240_x,CMRR]
        #data = [Xend_x]        
        mpplot.LogLogPlot(data,
                        lim=(None,[1e-3,1e3]),
                        filename='{0}/XarmDisplace_{1}_{2}_{3}'.format(title,start,tlen,option),
                        label=['Frequency [Hz]','Displacement [m/rtHz]']
        )
    if False:
        data = [TR240_x,Xend_x,Cent_x,Yend_x,Baro_x500]
        mpplot.LogLogPlot(data,
                        lim=(None,[0.5e-14,1e-10]),
                        filename='{0}/AllSeismometer_{1}_{2}_{3}'.format(title,start,tlen,option),                        
                        label=['Frequency [Hz]','Strain [1/rtHz]']
        )        
    if False:
        for a in [Xend_x,Yend_x,Cent_x]:
            for b in [Xend_x,Yend_x,Cent_x]:
                a.get_coherence(b,8.0,plot=True)
        for a in [Xend_y,Yend_y,Cent_y]:
            for b in [Xend_y,Yend_y,Cent_y]:
                a.get_coherence(b,8.0,plot=True)
        for a in [Xend_z,Yend_z,Cent_z]:
            for b in [Xend_z,Yend_z,Cent_z]:
                a.get_coherence(b,8.0,plot=True)
        for a in [Cent_x,Cent_x,Cent_x]:
            for b in [Xend_x,Yend_x,Cent_x]:
                a.get_coherence(b,8.0,plot=True)
        for a in [Cent_x,Cent_x,Cent_x]:
            for b in [Xend_y,Yend_y,Cent_y]:
                a.get_coherence(b,8.0,plot=True)
        for a in [Cent_x,Cent_x,Cent_x]:
            for b in [Xend_z,Yend_z,Cent_z]:
                a.get_coherence(b,8.0,plot=True)
                
        Strain.get_coherence(Xend_x,8.0,plot=True)
        Strain.get_coherence(Yend_x,8.0,plot=True)
        Strain.get_coherence(Cent_x,8.0,plot=True)
        Strain.get_coherence(TR240_x,8.0,plot=True)
        Strain.get_coherence(Baro_x500,8.0,plot=True)
        Strain.get_coherence(Baro_x2000,8.0,plot=True)
        TR240_x.get_coherence(Xend_x,8.0,plot=True)
        TR240_x.get_coherence(Yend_x,8.0,plot=True)
        TR240_x.get_coherence(Cent_x,8.0,plot=True)
        TR240_x.get_coherence(Baro_x500,8.0,plot=True)
        TR240_x.get_coherence(Baro_x2000,8.0,plot=True)
