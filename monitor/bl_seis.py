from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np


start = tconvert('Dec 01 00:00:00 JST')
start = tconvert('Dec 25 00:00:00 JST')
end = tconvert('Dec 25 13:00:00 JST')


chname = [
    'K1:PEM-EXV_GND_TR120Q_X_BLRMS_30M_100M_OUT_DQ.mean,s-trend',
    'K1:PEM-EXV_GND_TR120Q_X_BLRMS_100M_300M_OUT_DQ.mean,s-trend',
    'K1:PEM-EXV_GND_TR120Q_X_BLRMS_300M_1_OUT_DQ.mean,s-trend',
    'K1:PEM-EXV_GND_TR120Q_X_BLRMS_1_3_OUT_DQ.mean,s-trend',
    'K1:PEM-EXV_GND_TR120Q_X_BLRMS_3_10_OUT_DQ.mean,s-trend',
    'K1:PEM-EXV_GND_TR120Q_X_BLRMS_10_30_OUT_DQ.mean,s-trend',
    'K1:PEM-EXV_GND_TR120Q_X_BLRMS_30_100_OUT_DQ.mean,s-trend',
    ]

    
data = TimeSeriesDict.fetch(chname,start,end,
                            host='10.68.10.122',port=8088,
                            verbose=True,pad=np.nan)
labelname = [c.replace('_',' ') for c in chname]
epoch = data.values()[0].epoch


from matplotlib import pyplot
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
n = len(data)
gs = GridSpec(n,3)

plot, ax = pyplot.subplots(nrows=len(data), ncols=2, sharex=True, figsize=(16, 12),
                           #gridspec_kw={'width_ratios': [2, 1]}
                           )
#fig = pyplot.figure(figsize=(16,12))
print ax[0]

for i,value in enumerate(data.values()):
    ax[i] = pyplot.subplot(gs[i,:2])
    ax[i].plot(value,label=labelname[i])
    ax[i].set_ylim(-3,3)
    ax[i].set_xlabel('')
    ax[i].set_xlabel('')
    ax[i].legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=10)
ax[-1].set_xlabel('Time')
#ax.set_xscale('auto-gps')
plot.savefig('exv_tr120q.png')
