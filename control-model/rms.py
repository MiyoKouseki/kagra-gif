#
from gwpy.frequencyseries import FrequencySeries
from gwpy.plot import Plot 
seis = FrequencySeries.read('Xaxis_ixv1_50pct.hdf5')**2.0
plot = Plot()
ax = plot.gca(xscale='log', #xlim=(10, 1500),
              xlabel='Frequency [Hz]',
              yscale='log', #ylim=(3e-24, 2e-20),
              #ylabel=r'seismic noise [m/sec/\rtHz]')
              ylabel=r'seismic noise [m/sec/\rtHz]')
seis_rms = seis[::-1].cumsum()[::-1]*seis.f0#**1.0/2.0
_seis_rms = seis.rms()
print seis[::-1]
print seis
ax.plot(seis)
#ax.plot(seis_rms)
ax.plot(_seis_rms)
plot.savefig('rms.png')
