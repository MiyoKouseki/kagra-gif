import matplotlib.pyplot as plt
from gwpy.frequencyseries import FrequencySeries
from gwpy.spectrogram import Spectrogram
from miyopy.utils.trillium import Trillium
from obspy.signal.spectral_estimation import get_nhnm, get_nlnm

lt, ldb = get_nlnm()
ht, hdb = get_nhnm()
lfreq, lacc = 1./lt, 10**(ldb/20)*1e6
hfreq, hacc = 1./ht, 10**(hdb/20)*1e6
lfreq, lvel = lfreq, lacc/lfreq
hfreq, hvel = hfreq, hacc/hfreq

x = Spectrogram.read('./data/ASD_LongTerm_X.hdf5')
y = Spectrogram.read('./data/ASD_LongTerm_Y.hdf5')
z = Spectrogram.read('./data/ASD_LongTerm_Z.hdf5')


tr120 = Trillium('120QA')
v2vel = tr120.v2vel

x_median = v2vel(x.percentile(50))*1202.5
x_low = v2vel(x.percentile(5))*1202.5
x_high = v2vel(x.percentile(95))*1202.5

y_median = v2vel(y.percentile(50))*1202.5
y_low = v2vel(y.percentile(5))*1202.5
y_high = v2vel(y.percentile(95))*1202.5

h_median = (x_median**2 + y_median**2)**(1./2)
h_low = (x_low**2 + y_low**2)**(1./2)
h_high = (x_high**2 + y_high**2)**(1./2)

v_median = v2vel(z.percentile(50))*1202.5
v_low = v2vel(z.percentile(5))*1202.5
v_high = v2vel(z.percentile(95))*1202.5

median = (h_median**2 + v_median**2)**(1./2)
low = (h_low**2 + v_low**2)**(1./2)
high = (h_high**2 + v_high**2)**(1./2)


fig, ax = plt.subplots(1,1,figsize=(9,7))
#ax.plot_mmm(h_median,h_low,h_high,label='Horizontal')
#ax.plot_mmm(v_median,v_low,v_high,label='Vertical')
ax.plot_mmm(median,low,high,label='KAGRA')
ax.loglog(lfreq,lvel,'k--',label='NLNM')
ax.loglog(hfreq,hvel,'k--',label='NHNM')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Velocity [um/sec/rtHz]')
ax.set_xlim(1e-2,8)
ax.set_ylim(1e-4,100)
ax.legend(fontsize=15)
plt.suptitle('Seismic noise of KAGRA',fontsize=30)
plt.savefig('hoge.png')
plt.close()
