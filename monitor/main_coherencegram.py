
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np

start = tconvert('Dec 4 18:00:00 2018 JST')
end = tconvert('Dec 7 18:00:00 2018 JST')
chnames = ['K1:PEM-IXV_GND_TR120Q_X_OUT16',
           'K1:VIS-ITMX_TM_OPLEV_TILT_PIT_OUT16',
           'K1:VIS-ITMX_TM_OPLEV_TILT_YAW_OUT16',
               ]
data = TimeSeriesDict.fetch(chnames,start,end,host='10.68.10.122',port=8088,verbose=True,pad=np.nan)

ixv_x = data['K1:PEM-IXV_GND_TR120Q_X_OUT16']
itmx_pit = data['K1:VIS-ITMX_TM_OPLEV_TILT_PIT_OUT16']
itmx_yaw = data['K1:VIS-ITMX_TM_OPLEV_TILT_YAW_OUT16']


fftlen = 128
# coh = ixv_x.coherence(itmx_pit,fftlength=fftlen)
# plot = coh.plot(
#     xlabel='Frequency [Hz]', xscale='log',
#     ylabel='Coherence', yscale='linear', ylim=(0, 1),
# )
# plot.savefig('Coherence.png')

#specgram = ixv_x.coherence_spectrogram(itmx_pit,stride=fftlen*2,fftlength=fftlen)
specgram = ixv_x.coherence_spectrogram(itmx_yaw,stride=fftlen*2,fftlength=fftlen)
plot = specgram.imshow(vmin=0.0,vmax=1.0)
ax = plot.gca()
ax.set_yscale('log')
ax.set_ylim(1e-2, 10)
ax.colorbar(label=r'Coherence')
plot.savefig('Coherencegram.png')
