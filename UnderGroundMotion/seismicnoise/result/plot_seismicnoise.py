import numpy as np
import matplotlib.pyplot as plt
from gwpy.frequencyseries import FrequencySeries
from gwpy.spectrogram import Spectrogram
from miyopy.utils.trillium import Trillium
from obspy.signal.spectral_estimation import get_nhnm, get_nlnm
from gwpy.types.array2d import Array2D


def peterson_noise_model(unit='um/sec'):
    '''
    Return 
    
    '''
    lt, ldb = get_nlnm()
    ht, hdb = get_nhnm()
    lfreq, lacc = 1./lt, 10**(ldb/20)*1e6
    hfreq, hacc = 1./ht, 10**(hdb/20)*1e6
        
    if unit == 'um/sec':
        lfreq, lvel = lfreq, lacc/(2.0*np.pi*lfreq)
        hfreq, hvel = hfreq, hacc/(2.0*np.pi*hfreq)
        return [[lfreq,lvel],[hfreq,hvel]]        
    elif unit == 'um':
        lfreq, ldisp = lfreq, lacc/(2.0*np.pi*lfreq)**2
        hfreq, hdisp = hfreq, hacc/(2.0*np.pi*hfreq)**2     
        return [[lfreq,ldisp],[hfreq,hdisp]]
    else:
        raise ValueError(unit)

    
def _percentile(axis,pctl=50,unit='um/sec',**kwargs):
    _asd = FrequencySeries.read('./LongTerm_{0}_{1}.hdf5'.format(axis,pctl))**0.5
    amp = 10**(30.0/20.0)
    c2v = 20.0/2**15    
    _asd = v2vel(_asd)*c2v/amp*1e6
    if unit=='um':
        asd = _asd/(2.0*np.pi*_asd.frequencies.value)
        asd.write('./LongTerm_{0}_{1}_DISP.txt'.format(axis,pctl),format='txt')        
    elif unit=='um/sec':
        asd = _asd
        asd.write('./LongTerm_{0}_{1}_VELO.txt'.format(axis,pctl),format='txt')
    else:
        raise ValueError('!!1')
    return asd


def percentile(axis,**kwargs):
    if axis == 'H':
        x = _percentile('X',**kwargs)
        y = _percentile('Y',**kwargs)
        return  (x**2 + y**2)**0.5        
    elif axis in ['X','Y','Z']:
        return _percentile(axis,**kwargs)
    else:
        raise ValueError('!!!')


if __name__ == '__main__':
    unit = 'um/sec'
    #
    tr120 = Trillium('120QA')
    v2vel = tr120.v2vel    
    #
    h50 = percentile('H',pctl=50,unit=unit)
    h10 = percentile('H',pctl=10,unit=unit)
    h90 = percentile('H',pctl=90,unit=unit)
    z50 = percentile('Z',pctl=50,unit=unit)
    z10 = percentile('Z',pctl=10,unit=unit)
    z90 = percentile('Z',pctl=90,unit=unit)
    nlnm,nhnm = peterson_noise_model(unit=unit)
    selfnoise = tr120.selfnoise(unit=unit.replace('um','m'))*1e6
    #
    fig, ax = plt.subplots(1,1,figsize=(9,7))
    ax.plot_mmm(h50,h10,h90,label='Horizontal (10,50,90 percentile)',color='blue')
    ax.plot_mmm(z50,z10,z90,label='Vertical (10,50,90 percentile)',color='red')
    ax.loglog(selfnoise,'g--',label='Selfnoise of Seismometer',alpha=1.0)
    ax.loglog(nlnm[0],nlnm[1],'k--')
    ax.loglog(nhnm[0],nhnm[1],'k--',label='Peterson Low and High Noise Models')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_xlim(1e-2,8)
    if unit=='um/sec':
        ax.set_ylim(1e-5,20)
        ax.set_ylabel('Velocity [um/sec/rtHz]')        
    elif unit=='um':
        ax.set_ylim(5e-6,20)
        ax.set_ylabel('Displacement [um/rtHz]')
    ax.legend(fontsize=15,loc='lower left')
    plt.suptitle('Seismic Noise of KAGRA',fontsize=40)
    plt.savefig('seismicnoise.png')
    plt.close()
