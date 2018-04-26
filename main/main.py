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
    }


def main():
    import pandas as pd
    kamioka = pd.read_csv("../event/0425_heavy_rain/jma_kamioka_180423-180425.csv",
                          delimiter=','
                          )
    print kamioka[:,0]
    
    
if __name__ == '__main__':
    main()    
