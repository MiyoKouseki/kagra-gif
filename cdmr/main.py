
import numpy as np
from gwpy.plot import Plot
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.time import tconvert

from miyopy.gif import GifData
from miyopy.calibration import vel2vel

vel_p = 5500.0
fftlength = 2**10

# Download data
start = tconvert('Jan 14 00:00:00 JST')
print start
#end = tconvert('Jan 14 01:00:00 JST')
#end = tconvert('Jan 14 13:00:00 JST')
end = start + fftlength*16
#print(tconvert(end+2**10*46))
#exit()

kwargs = {}
kwargs['port'] = 8088
kwargs['host'] = '10.68.10.122'
kwargs['verbose'] = True
channels = ['K1:PEM-IXV_GND_TR120Q_X_OUT_DQ',
            'K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ',
            'K1:PEM-EXV_GND_TR120Q_X_OUT_DQ',
            ]
data = TimeSeriesDict.fetch(channels,start,end,pad=np.nan,**kwargs)
# 
seis1 = data['K1:PEM-IXV_GND_TR120Q_X_OUT_DQ']
seis2 = data['K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ']
seis3 = data['K1:PEM-EXV_GND_TR120Q_X_OUT_DQ']
# specgram = seis3.spectrogram(fftlength*2, fftlength, overlap=fftlength*0.5) ** (1/2.)
# plot = specgram.imshow(norm='log', vmin=1e-5, vmax=10)
# ax = plot.gca()
# ax.set_yscale('log')
# ax.set_ylim(1e-3, 100)
# ax.colorbar(label=r'Ground Velocity [um/sec$\sqrt{\mathrm{Hz}}$]')
# plot.savefig('specgram.png')


diff12 = (seis1-seis2)/np.sqrt(2.0)
sg = diff12.spectrogram2(fftlength=fftlength, overlap=fftlength/2, window='hanning') ** (1/2.)
median = vel2vel(sg.percentile(50))
low = vel2vel(sg.percentile(5))
high = vel2vel(sg.percentile(95))

from gwpy.plot import Plot
plot = Plot()
ax = plot.gca(xscale='log', xlim=(1e-3, 100), xlabel='Frequency [Hz]',
              yscale='log', ylim=(1e-5, 1e1),
              ylabel=r'Velocity [um/sec/rtHz]')
ax.plot_mmm(median, low, high, color='gwpy:ligo-hanford')

sg = seis1.spectrogram2(fftlength=fftlength, overlap=fftlength/2, window='hanning') ** (1/2.)
median = vel2vel(sg.percentile(50))
low = vel2vel(sg.percentile(5))
high = vel2vel(sg.percentile(95))
ax.plot_mmm(median, low, high, color='gwpy:ligo-livingston')
#ax.set_title('LIGO-Hanford strain noise variation around GW170817',
#             fontsize=16)
plot.savefig('ASD.png')


exit()

seis1 = seis1/vel_p*1e-6
seis2 = seis2/vel_p*1e-6
seis3 = seis3/vel_p*1e-6
diff13 = seis1-seis3
diff23 = seis2-seis3


# chname = 'CALC_STRAIN'
# segments = GifData.findfiles(chname,start,end)
# allfiles = [path for files in segments for path in files]

# gifx = TimeSeries.read(source=allfiles,name='CALC_STRAIN',
#                        verbose=True,
#                        format='gif',pad=np.nan,nproc=2)

# gifx = gifx

# specgram = gifx.spectrogram(fftlength*2, fftlength, overlap=fftlength*0.5) ** (1/2.)
# plot = specgram.imshow(norm='log')#, vmin=1e-5, vmax=10)
# ax = plot.gca()
# ax.set_yscale('log')
# ax.set_ylim(1e-3, 100)
# ax.colorbar(label=r'Ground Velocity [um/sec$\sqrt{\mathrm{Hz}}$]')
# plot.savefig('specgram_gifx.png')




exit()
asd_seis1 = seis1.psd(fftlength,overlap=fftlength*0.5)**0.5
asd_seis2 = seis2.psd(fftlength,overlap=fftlength*0.5)**0.5
asd_seis3 = seis3.psd(fftlength,overlap=fftlength*0.5)**0.5
asd_diff13 = diff13.psd(fftlength,overlap=fftlength*0.5)**0.5
asd_diff23 = diff23.psd(fftlength,overlap=fftlength*0.5)**0.5

asd_seis1 = vel2vel(asd_seis1)
asd_seis2 = vel2vel(asd_seis2)
asd_seis3 = vel2vel(asd_seis3)


f = asd_diff13.frequencies.value
asd_diff13 = asd_diff13/(2.0*np.pi*f)
asd_diff23 = asd_diff23/(2.0*np.pi*f)

asd_gifx = gifx.psd(fftlength,overlap=fftlength*0.5)**0.5


plot = Plot(asd_seis1,asd_seis2,asd_seis3,asd_gifx,
#plot = Plot(asd_diff13,asd_diff13,asd_gifx,
            yscale='log',xscale='log')
plot.savefig('hoge.png')
