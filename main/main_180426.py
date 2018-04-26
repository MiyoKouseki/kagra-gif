#
#! coding:utf-8

import sys 
import numpy as np
from scipy import signal
from miyopy.types import Seismometer
import miyopy.io.reader as reader
import miyopy.plot.mpplot as mpplot
import subprocess
from scipy.signal import spectral
#import miyopy.types.timeseries as mpdata

'''
memo
M5.8, 2018-04-08-14:32:34(UTC), 1207240372, W of Tottori, Japan
M5.2, 2018-03-27-06:39:10(UTC), 1206167968, WS of Iwo Jima, Japan
M6.6, 2018-03-26-09:51:00(UTC), 1206093078, Kimbe, Papua New Guinea
M6.4, 2018-03-25-20:14:47(UTC), 1206044105, NW of Saumlaki, Indonesia
M5.0, 2018-03-25-15:36:24(UTC), 1206027402, SE of Hachijo-jima, Japan
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
        '0421chiba_all':[1208339257-2**10+100,2**11],
        '0421chiba_p':[1208339257+45,2**4],
        '0421chiba_pslove':[1208339257+45,2**7],
        '0421chiba_ps':[1208339257+40,2**6],
        #'0421chiba_p':[1208339257,2**6],
        '0421chiba':[1208339257-2**10,2**7],
        '0423shimane':[1208448078-2**6,2**9],
        #'hoge':[1207440018,2**6], # 04/11 09:00, 18hour
    }

        
def main_getGPStime():
    '''イベントを指定して、そのイベントの期間を返す関数。    

    Return
    ------
    t0 : int
       開始時刻。GPS時刻。
    tlen : int
       期間。秒。
    '''
    try:
        event = sys.argv[1]
        #option = sys.argv[2]
        t0, tlen = EQ_name[event]
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
    return t0,tlen,title

    
def getKAGRAseismometer(t0,tlen,title,theta=0,plot33=False):    
    '''
    3つの地震計の3つの軸の信号を取得してくる。
    '''
    #theta = 30
    xend = Seismometer(t0,tlen,name='EX1',theta=theta)
    #xend.bandpass(1e-3,1e0,1)
    yend = Seismometer(t0,tlen,name='EY1',theta=theta)
    #yend.bandpass(1e-3,1e0,1)    
    cent = Seismometer(t0,tlen,name='IY0',theta=theta)
    #cent.bandpass(1e-3,1e0,1)
    if False:
        xend = xend/5500.0
        yend = yend/5500.0
        cent = cent/5500.0                
    return xend,yend,cent


def main_rotate_clockwise_180():
    # kagra : 36.4165574,137.3046029 , 400m?  
    # chiba : 35.55N, 141.09, 29km
    # 350km, 105deg
    t0,tlen,title = main_getGPStime()
    for theta in range(0,180,5):
        xend,yend,cent = getKAGRAseismometer(t0,tlen,title,theta=theta,plot33=True)
        if True:
            fname = '{0}/{1}_{2}_{3:03d}.png'.format(title,t0,tlen,theta)
            cmd = 'mkdir -p {0}'.format(title)
            ret  =  subprocess.check_call( cmd.split(" ") )
            data = [xend.x,xend.y,xend.z,
                    yend.x,yend.y,yend.z,
                    cent.x,cent.y,cent.z]
            mpplot.subplot33(data,
                            fname,
                            ylim=[-1.5e-5,1.5e-5],
                            title=u'{0:+04d}\u00b0 Rotate'.format(theta),
                            )
            cmd = 'open {0}'.format(fname)
            print cmd
            ret  =  subprocess.check_call( cmd.split(" ") )        
            
            
def main_():
    # kagra : 36.4165574,137.3046029 , 400m?  
    # chiba : 35.55N, 141.09, 29km
    # 350km, 105deg
    t0,tlen,title = main_getGPStime()
    theta = -75
    #theta = 105
    xend,yend,cent = getKAGRAseismometer(t0,tlen,title,theta=theta,plot33=True)
    if True:
        fname = '{0}/{1}_{2}_{3:03d}.png'.format(title,t0,tlen,theta)
        cmd = 'mkdir -p {0}'.format(title)
        ret  =  subprocess.check_call( cmd.split(" ") )
        data = [xend.x,xend.y,xend.z,
                yend.x,yend.y,yend.z,
                cent.x,cent.y,cent.z]
        mpplot.subplot33(data,
                         fname,
                         ylim=[-1.5e-5,1.5e-5],
                         title=u'{0:+04d}\u00b0 Rotate'.format(theta),
        )
        cmd = 'open {0}'.format(fname)
        print cmd
        ret  =  subprocess.check_call( cmd.split(" ") )        
            
        
def main():
    t0,tlen,title = main_getGPStime()
    theta = -30
    xend,yend,cent = getKAGRAseismometer(t0,tlen,title,theta=theta,plot33=True)
    channels = ['K1:VIS-ETMY_IP_BLEND_LVDTL_OUT16',
                'K1:VIS-ETMY_IP_BLEND_LVDTT_OUT16',]
    etmy_ip_l,etmy_ip_t = reader.kagra.readKAGRAdata(t0,
                                                     tlen,
                                                     channels)
    channels = ['K1:VIS-ETMX_IP_BLEND_LVDTL_OUT16',
                'K1:VIS-ETMX_IP_BLEND_LVDTT_OUT16',]
    etmx_ip_l,etmx_ip_t = reader.kagra.readKAGRAdata(t0,
                                                     tlen,
                                                     channels)
    
    #etmy_ip_l.bandpass(1e-3,1e0,1)
    #etmy_ip_t.bandpass(1e-3,1e0,1)
    #etmx_ip_l.bandpass(1e-3,1e0,1)
    #etmx_ip_t.bandpass(1e-3,1e0,1)
    if True:
        fname = '{0}/etmx_ip_{1}_{2}_{3:03d}.png'.format(title,t0,tlen,theta)
        cmd = 'mkdir -p {0}'.format(title)
        ret  =  subprocess.check_call( cmd.split(" ") )
        data = [xend.x,xend.y,xend.z,
                etmy_ip_t,etmy_ip_l,yend.z,
                etmx_ip_l,etmx_ip_t,cent.z,]
        mpplot.subplot33(data,
                         fname,
                         #ylim=[-1.5e-5,1.5e-5],
                         title=u'{0:+04d}\u00b0 Rotate'.format(theta),
                         )
        cmd = 'open {0}'.format(fname)
        print cmd
        ret  =  subprocess.check_call( cmd.split(" ") )
    if True:
        fname = '{0}/etmy_ip_{1}_{2}_{3:03d}.png'.format(title,t0,tlen,theta)
        cmd = 'mkdir -p {0}'.format(title)
        ret  =  subprocess.check_call( cmd.split(" ") )
        data = [yend.x,yend.y,yend.z,
                etmy_ip_t,etmy_ip_l,yend.z,
                etmx_ip_l,etmx_ip_t,cent.z,]
        mpplot.subplot33(data,
                         fname,
                         #ylim=[-1.5e-5,1.5e-5],
                         title=u'{0:+04d}\u00b0 Rotate'.format(theta),
                         )
        cmd = 'open {0}'.format(fname)
        print cmd
        ret  =  subprocess.check_call( cmd.split(" ") )
        
        
if __name__ == '__main__':
    #main_rotate_clockwise_180()
    main_()
