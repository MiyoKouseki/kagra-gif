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


def plot_band_histgram(sg,low,high,scale=0.9,loc=0):    
    useism_band = sg.crop_frequencies(low,high).mean(axis=1) # um/rtHz
    fig, ax = plt.subplots(1,1,figsize=(7,7))
    plt.title('Between {0:3.2f} - {1:3.2f} Hz '.format(low,high))
    hist,bins = np.histogram(useism_band,density=True,bins=150,range=(0.01,10))
    ax.step(bins[:-1],hist,where='post',color='k')
    ax.set_ylim(0,1)
    ax.set_xlabel('Horizontal motion [um/rtHz]')
    #ax.set_xscale('log')
    ax.set_xlim(1e-2,10e0)
    if True:
        from scipy.stats import rayleigh
        x = np.linspace(0,10,10000)
        #sigma = 0.9
        #kitaichi = sigma*np.sqrt(np.pi/2.0)
        #scale = sigma
        ax.plot(x,rayleigh.pdf(x,scale=scale,loc=loc))
    ax.set_ylabel('Counts')    
    ax2 = ax.twinx()
    ax2.set_ylabel('Cumulative Probability')
    ax2.plot(bins[:-1],np.cumsum(hist)/np.float(np.sum(hist)),'k--',linewidth=2)
    ax2.set_ylim(0,1)
    ax2.set_yticks([0,0.1,0.5,0.9,1.0])
    ax2.axhline(y=0.10, color='k', linestyle=':')
    ax2.axhline(y=0.50, color='k', linestyle=':')
    ax2.axhline(y=0.90, color='k', linestyle=':')
    plt.savefig('./tmp/histgram_{0:02.2f}_{1:02.2f}.png'.format(low,high))


def percentile(sg_in1,pctl,unit='um'):    
    amp = 10**(30.0/20.0)
    c2v = 20.0/2**15    
    _asd = v2vel(sg_in1.percentile(pctl))*c2v/amp*1e6
    asd = _asd/(2.0*np.pi*_asd.frequencies.value)
    return asd

if False:
    print('Read spectrogram')
    x = Spectrogram.read('./tmp/SG_LongTerm_X.hdf5')
    y = Spectrogram.read('./tmp/SG_LongTerm_Y.hdf5')
    z = Spectrogram.read('./tmp/SG_LongTerm_Z.hdf5')
    h = (x**2+y**2)**(0.5)
    h.name = 'Horizontal'
    h.channel = 'Horizontal'
    h.write('./tmp/SG_LongTerm_H.hdf5',format='hdf5',overwrite=True)
else:
    h = Spectrogram.read('./tmp/SG_LongTerm_H.hdf5',format='hdf5')


if True:
    h = h.ratio('median')    
    #h = h.crop_frequencies(0.1,0.2)
    plot = h.plot(norm='log', vmin=.1, vmax=10, cmap='Spectral_r',epoch=h.t0)
    ax = plot.gca()
    ax.set_yscale('log')
    ax.set_ylim(1e-2, 10)
    ax.colorbar(label='Relative amplitude')
    plot.savefig('./tmp/spectrogram.png')

    
if True:
    low,high = 0.10,0.30
    plot_band_histgram(h,low,high,scale=0.85,loc=0.1)
    low,high = 0.03,0.10
    plot_band_histgram(h,low,high,scale=0.67,loc=0.2)
