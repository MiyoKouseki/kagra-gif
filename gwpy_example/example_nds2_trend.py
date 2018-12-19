from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np


start = tconvert('Dec 12 00:00:00 JST')
end = tconvert('Dec 19 00:00:00 JST')


'''

<channelname>.mi

'''


chname = [
    #'K1:PEM-IXV_WEATHER_PRES_OUT16.mean,m-trend',    
    #'K1:PEM-IXV_GND_TR120Q_X_OUT16.mean,s-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT16.max,s-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT16.min,s-trend',
    'K1:PEM-IXV_GND_TR120Q_X_OUT16.rms,s-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT16.mean,m-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT16.max,m-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT16.min,m-trend',
    #'K1:PEM-IXV_GND_TR120Q_X_OUT16.rms,m-trend',
    ]
    
data = TimeSeriesDict.fetch(chname,start,end,
                            host='10.68.10.122',port=8088,
                            verbose=True,pad=np.nan)
print data
plot = data.plot()
ax = plot.gca()
ax.set_ylim(0,5)
plot.savefig('ixv_tr120q.png')
