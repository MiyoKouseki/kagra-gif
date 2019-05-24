from gwpy.timeseries import TimeSeries
from gwpy.plot import Plot

'''
Fetch seismometer data from nds.

'''


# - data1 -----------------------------
start = '2019 May 13 00:00:00 JST'
end = '2019 May 13 04:00:00 JST'
chname = 'K1:PEM-SEIS_EXV_GND_X_OUT_DQ'
# -------------------------------------

# fetch data
data = TimeSeries.fetch(chname,start,end,host='k1nds0',port=8088,verbose=True)
print('fetch done')

# calc spectrum
fftlength = 2**9
sg = data.spectrogram2(fftlength=fftlength,
                       overlap=fftlength/2,
                       nproc=2,
                       window='hanning') ** (1/2.)
print('fft done')
# percentile
median = sg.percentile(50)
low = sg.percentile(5)
high = sg.percentile(95)
print('percentile done')

# plot TimeSeries
plot = data.plot()
plot.savefig('./img_timeseries.png')
plot.close()

# plot Spectrum
plot = Plot()
ax = plot.gca(xscale='log', xlim=(1e-3, 200), xlabel='Frequency [Hz]',
              yscale='log',# ylim=(3e-24, 2e-20),
              ylabel=r'Ground Velocity [um/sec/\rtHz]')
ax.plot_mmm(median, low, high, color='gwpy:ligo-hanford')
ax.set_title('No title',fontsize=16)
plot.savefig('./img_asd.png')

# write data
low.write('data1_exv_x_5pct.hdf5',format='hdf5',overwrite=True)
median.write('data1_exv_x_50pct.hdf5',format='hdf5',overwrite=True)
high.write('data1_exv_x_95pct.hdf5',format='hdf5',overwrite=True)
