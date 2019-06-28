import numpy as np
import matplotlib.pyplot as plt
from gwpy.frequencyseries import FrequencySeries
from gwpy.spectrogram import Spectrogram
from miyopy.utils.trillium import Trillium
from obspy.signal.spectral_estimation import get_nhnm, get_nlnm
from gwpy.types.array2d import Array2D


tr120 = Trillium('120QA')
v2vel = tr120.v2vel    
    
lt, ldb = get_nlnm()
ht, hdb = get_nhnm()
lfreq, lacc = 1./lt, 10**(ldb/20)*1e6
hfreq, hacc = 1./ht, 10**(hdb/20)*1e6
lfreq, lvel = lfreq, lacc/(2.0*np.pi*lfreq)
hfreq, hvel = hfreq, hacc/(2.0*np.pi*hfreq)
lfreq, ldisp = lfreq, lvel/(2.0*np.pi*lfreq)
hfreq, hdisp = hfreq, hvel/(2.0*np.pi*hfreq)

def percentile(sg_in1,pctl,unit='um'):    
    amp = 10**(30.0/20.0)
    c2v = 20.0/2**15    
    _asd = v2vel(sg_in1.percentile(pctl))*c2v/amp*1e6
    asd = _asd/(2.0*np.pi*_asd.frequencies.value)
    return asd

if False:
    print('Read spectrogram')
    x = Spectrogram.read('./data2/SG_LongTerm_X.hdf5')
    y = Spectrogram.read('./data2/SG_LongTerm_Y.hdf5')
    z = Spectrogram.read('./data2/SG_LongTerm_Z.hdf5')
    h = (x**2+y**2)**(0.5)
else:
    h = Spectrogram.read('./data2/SG_LongTerm_H.hdf5',format='hdf5')
    #exit()
    
fig, ax = plt.subplots(1,1,figsize=(9,7))
ax.plot_mmm(percentile(h,50),percentile(h,10),percentile(h,90))
ax.loglog(lfreq,ldisp,'k--')
ax.loglog(hfreq,hdisp,'k--',label='Peterson Low and High Noise Models')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Displacement [um/rtHz]')
ax.set_xlim(1e-2,8)
ax.set_ylim(5e-6,20)
ax.legend(fontsize=15,loc='lower left')
import matplotlib.patches as patches
r1 = patches.Rectangle(xy=(0.03, 0.01), width=0.07, height=10, ec='#000000', fill=False)
r2 = patches.Rectangle(xy=(0.10, 0.01), width=0.2, height=10, ec='#000000', fill=False)
ax.add_patch(r1)
ax.add_patch(r2)
plt.suptitle('Seismic noise of KAGRA',fontsize=40)
plt.savefig('seismicnoise.png')
plt.close()
