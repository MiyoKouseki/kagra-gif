#
#! coding:utf-8

import sys 
import numpy as np
from scipy import signal
from miyopy.types import Seismometer,Timeseries
import miyopy.io.reader as reader
import miyopy.plot.mpplot as mpplot
import subprocess
from scipy.signal import spectral
from miyopy.parse.arg import get_gpstime
import pickle

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
    '0421chiba':[1208339257-2**10,2**7],
    '0423shimane':[1208448078-2**6,2**9],
    '0425_heavy_rain':[],
    '0425_00':[1208617218,2**16],
    '0424_23':[1208617218-3600,2**10],
    '0424_18':[1208595618,2**17], # start 04-24-18:00
    '0426_18':[1208769618,2**17], # start04-26-18:20               
    '0428_09':[1208908938,2**17], # start04-28-09:02
    #'0428_09_':[1208908938+92400,1000], # start04-28-09:02,
    '0428_09_1':[1208908938,2**16], # start04-28-09:02,
    '0428_09_2':[1208908938+93400,2**16], # start04-28-
    '0428_09_2':[1208908938+93400,2**16], # start04-28-
    # 1208908938+92400から200秒データがおかしい
    # 2018-04-29 JST 10:42:00から200秒
    #'0430_09_2':[1208908938,2**16], # start04-28-
    #'0430_22':[1209128418,2**14] #[data] JST 04-30-22:00 many lockloss!
    '0429_22':[1209042018,2**14], #[data] JST 04-29-22:00
    '0418_00_STRAIN':[1208044818,2**20], #[data] JST   
    }


def main_plotSEismometerSepctrogram(*args):
    theta = 0
    ave = 16
    ex1 = Seismometer(t0,tlen,'EX1',theta=theta)    
    ey1 = Seismometer(t0,tlen,'EY1',theta=theta)
    cen = Seismometer(t0,tlen,'IY0',theta=theta)
    # Yend-Xend
    if True:
        from spectrogram import spectrogram
        sec = 1
        wlen = 128
        clip = [0,1]
        print title
        # Xend
        spectrogram(ex1.x.timeseries,ex1.x._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ex1.x._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(ex1.y.timeseries,ex1.y._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ex1.y._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(ex1.z.timeseries,ex1.z._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ex1.z._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)        
        # Yend
        spectrogram(ey1.y.timeseries,ey1.y._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ey1.y._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(ey1.x.timeseries,ey1.x._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ey1.x._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(ey1.z.timeseries,ey1.z._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ey1.z._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)        
        # Cent
        spectrogram(cen.y.timeseries,cen.y._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,cen.y._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(cen.x.timeseries,cen.x._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,cen.x._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(cen.z.timeseries,cen.z._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,cen.z._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)


def main_Lock(*args):
    channels = ['K1:VIS-BS_TM_OPLEV_SERVO_PIT_OFFSET',
                #'K1:VIS-BS_TM_OPLEV_SERVO_YAW_OFFSET',
                'K1:VIS-BS_IM_LOCK_L_OUT16',
                'K1:GRD-LSC_MICH_STATE_N']
    data = reader.kagra.readKAGRAdata(t0,tlen,channels)
    label=['Time','Value']
    filename = '{0}/TimeseriesMultPlot_{1}_{2}.png'.format(title,t0,tlen)
    legend = [d_._name for d_ in data]
    mpplot.MultiPlot_new(data,label,filename,legend)
    

def main_StrainmeterSignalBudjet(theta=0.0,*args):
    MICH_CTRL_L = reader.kagra.readKAGRAdata(t0,tlen,
                                             ['K1:VIS-BS_IM_LOCK_L_OUT16'],
                                             plot=True,
                                             detrend=True,
                                             )[0]
    X1500_TR_X = Seismometer(t0,tlen,
                             'X1500_TR240',
                             plot=True,
                             detrend=True).x
    GIF_X = reader.gif.readGIFdata(t0,tlen,
                                   'CALC_STRAIN',
                                   name='X_strainmeter',
                                   plot=True,
                                   detrend=True)
    X500_BARO = reader.gif.readGIFdata(t0,tlen,
                                       'X500_BARO',
                                       name='x500_pressure',
                                       plot=True,detrend=True)
    X2000_BARO = reader.gif.readGIFdata(t0,tlen,
                                        'X2000_BARO',
                                        name='x2000_pressure',
                                        plot=True,detrend=True)
    X500_TEMP = reader.gif.readGIFdata(t0,tlen,
                                       'X500_TEMP',
                                       name='x500_temperature',
                                       plot=True,detrend=True)
    # convert
    X1500_TR_X = X1500_TR_X/5500.0/1196.5
    X500_BARO = X500_BARO*2e-8
    X2000_BARO = X2000_BARO*2e-8
    MICH_CTRL_L = MICH_CTRL_L
    # psd
    ave = 4
    MICH_CTRL_L.get_psd(ave=ave,plot=False)
    GIF_X.get_psd(ave=ave,plot=False)
    X1500_TR_X.get_psd(ave=ave,plot=False)
    X500_BARO.get_psd(ave=ave,plot=False)
    X500_TEMP.get_psd(ave=ave,plot=False)
    X2000_BARO.get_psd(ave=ave,plot=False)
    #
    datalist = [GIF_X,
                X1500_TR_X,
                X500_BARO,
                MICH_CTRL_L
                ]
    #mpplot.LogLogPlot(datalist,label=['Frequency [Hz]','Strain [1/rtHz]'],lim=(None,[1e-13,1e-8]),filename='./StrainmeterSignalBudjet_{0:03d}'.format(theta))
    mpplot.LogLogPlot(datalist,label=['Frequency [Hz]','Strain [1/rtHz]'],lim=(None,None),filename='./StrainmeterSignalBudjet_{0:03d}'.format(theta))


def main_strain(init=False,save=False,load=True):
    EQ_name = {'0418_00_STRAIN':[1208044818,2**20]}
    event = '0418_00_STRAIN'
    t0,tlen = EQ_name[event]
    title = '../event/{0}'.format(event)
    #
    if init:
        GIF_X = reader.gif.readGIFdata(t0,tlen,
                                    'CALC_STRAIN',
                                    name='X_strainmeter',
                                    plot=True,
                                    detrend=True)    
    if save:
        print 'saving...'
        with open('0418_00_STRAIN.pickle', mode='wb') as f:
            pickle.dump(GIF_X, f)
    if load:
        print 'loading...'
        with open('0418_00_STRAIN.pickle', mode='rb') as f:
            GIF_X = pickle.load(f)
    #
    gotic = reader.gotic.readGOTICdata(t0,tlen,'Xarm',plot=True,detrend=False)
    #
    import matplotlib.pyplot as plt
    plt.plot(GIF_X._time,GIF_X.timeseries,label=GIF_X._name)
    plt.plot(gotic._time,gotic.timeseries,label=gotic._name)
    plt.savefig('hoge.png')
    plt.close()
    
if __name__ == '__main__':
    t0,tlen,title = get_gpstime(EQ_name)
    #main_plotSEismometerSepctrogram(t0,tlen,title)
    #main_Lock(t0,tlen,title)
    #main_StrainmeterSignalBudjet(t0,tlen,title)   
    main_strain()
