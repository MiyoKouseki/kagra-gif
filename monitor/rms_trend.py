from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np


start = tconvert('Dec 25 21:00:00 JST')
end = tconvert('Dec 26 07:00:00 JST')


'''

<channelname>.mi

'''


chname = [
    #'K1:PEM-IXV_WEATHER_PRES_OUT_DQ.mean,m-trend',
    
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.mean,s-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.max,s-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.min,s-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.rms,s-trend',

    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.mean,m-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.max,m-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ.min,m-trend',
    'K1:PEM-EXV_GND_TR120Q_X_OUT_DQ.mean,s-trend',
    'K1:PEM-EXV_GND_TR120Q_Y_OUT_DQ.mean,s-trend',
    'K1:PEM-EXV_GND_TR120Q_Z_OUT_DQ.mean,s-trend',
    #'K1:PEM-IMC_GND_TR120C_MCI_X_OUT_DQ.rms,m-trend',
    #'K1:PEM-IMC_GND_TR120C_MCI_Y_OUT_DQ.rms,m-trend',
    #'K1:PEM-IMC_GND_TR120C_MCI_Z_OUT_DQ.rms,m-trend',
    ]
    
data = TimeSeriesDict.fetch(chname,start,end,
                            host='10.68.10.122',port=8088,
                            verbose=True,pad=np.nan)
labelname = [c.replace('_',' ')for c in chname]
epoch = data.values()[0].epoch
plot = data.plot(epoch=start)
ax = plot.gca()
ax.set_ylabel('Ground Velocity [um/s]')
ax.legend(labelname)
ax.set_ylim(-2,2)
plot.savefig('ixv_tr120q.png')
