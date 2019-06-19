#
#! coding:utf-8
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np
'''
神岡のNDSをつかって、複数チャンネルのトレンドデータをプロットするスクリプト
'''

start = tconvert('May 01 2019 00:00:00 JST')
start = tconvert('Jun 01 2019 00:00:00 JST')
end = tconvert('Jun 10 2019 00:00:00 JST')

chname = [
    'K1:PEM-SEIS_EXV_GND_X_OUT_DQ.rms,m-trend',
    'K1:PEM-SEIS_EXV_GND_Y_OUT_DQ.rms,m-trend',
    'K1:PEM-SEIS_EXV_GND_Z_OUT_DQ.rms,m-trend',        
    #'K1:PEM-SEIS_EXV_GND_X_BLRMS_30M_100M_OUT16.rms,m-trend',    
    #'K1:PEM-SEIS_EXV_GND_X_BLRMS_100M_300M_OUT16.rms,m-trend',
    #'K1:PEM-SEIS_EXV_GND_X_BLRMS_300M_1_OUT16.rms,s-trend',
    #'K1:PEM-SEIS_EXV_GND_X_BLRMS_1_3_OUT16.rms,s-trend',
    #'K1:PEM-SEIS_EXV_GND_X_BLRMS_3_10_OUT16.rms,s-trend',
    #'K1:PEM-SEIS_EXV_GND_X_BLRMS_10_30_OUT16.rms,s-trend',
    #'K1:PEM-SEIS_EXV_GND_X_BLRMS_30_100_OUT16.rms,s-trend',
    ]
    
data = TimeSeriesDict.fetch(chname,start,end,
                            host='10.68.10.122',port=8088,
                            verbose=True,pad=np.nan)
labelname = [c.replace('_',' ') for c in chname]
epoch = data.values()[0].epoch

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
figure, ax = plt.subplots(3,1,figsize=(15,15))
for i,value in enumerate(data.values()):
    print value
    ax[i].plot(value,label=labelname[i])
    ax[i].set_ylabel('Velocity [um/sec]')
    ax[i].legend(fontsize=20)
    ax[i].set_xscale('auto-gps')
    ax[i].set_ylim(0,2)

plt.savefig('img_trend.png')
