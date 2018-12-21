from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np


start = tconvert('Dec 12 23:59:42 JST')
#start = tconvert('Dec 11 23:59:42 JST')
#end = tconvert('Dec 12 23:59:42 JST')
end = tconvert('Dec 19 23:59:42 JST')


'''

<channelname>.mi

'''
chname = [
    'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ',
    ]
    
data = TimeSeriesDict.fetch(chname,start,end,
                            host='10.68.10.122',port=8088,
                            verbose=True,pad=np.nan)

chname = [
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.mean,s-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.max,s-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.min,s-trend',
    'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.rms,s-trend',
    ]
    
data_s = TimeSeriesDict.fetch(chname,start,end,
                            host='10.68.10.122',port=8088,
                            verbose=True,pad=np.nan)
chname = [
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.mean,m-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.max,m-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.min,m-trend',
    'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.rms,m-trend',
    ]    
data_m = TimeSeriesDict.fetch(chname,start,end,
                             host='10.68.10.122',port=8088,
                             verbose=True,pad=np.nan)

rms_s = data.values()[0].rms(1)
rms_m = data.values()[0].rms(60)
import matplotlib.pyplot as plt
fig,ax = plt.subplots(1,1)
ax.plot(rms_s,rms_m)
ax.set_ylim(0,5)
ax.legend(['rms'])
plt.savefig('ixv_tr120q.png')
