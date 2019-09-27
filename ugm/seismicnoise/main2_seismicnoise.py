import numpy as np
import matplotlib.pyplot as plt
from gwpy.frequencyseries import FrequencySeries
from gwpy.spectrogram import Spectrogram
from miyopy.utils.trillium import Trillium
from obspy.signal.spectral_estimation import get_nhnm, get_nlnm
from gwpy.types.array2d import Array2D

tr120 = Trillium('120QA')
v2vel = tr120.v2vel    


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

    
def _percentile(axis,pctl=50,unit='um/sec',suffix='',**kwargs):
    _asd = FrequencySeries.read('./data2/LongTerm_{0}_{1}_{2}.hdf5'.format(axis,pctl,suffix))**0.5
    amp = 10**(30.0/20.0)
    c2v = 20.0/2**15    
    _asd = v2vel(_asd)*c2v/amp*1e6
    if unit=='um':
        asd = _asd/(2.0*np.pi*_asd.frequencies.value)
        #asd.write('./LongTerm_{0}_{1}_DISP.txt'.format(axis,pctl),format='txt')        
    elif unit=='um/sec':
        asd = _asd
        #asd.write('./LongTerm_{0}_{1}_VELO.txt'.format(axis,pctl),format='txt')
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


def hoge(suffix='',plot_v=False,plot_99=True,unit='um',susresp=False,peterson=True,plot_selfnoise=True):
    #
    #suffix = '1211817600_1245372032' # 1 year
    #suffix = '1228594816_1232789120' # 12/11-
    if susresp:
        sus = FrequencySeries.read('./noctrl.hdf5').abs()
    else:
        sus = 1
    h50 = percentile('H',pctl=50,unit=unit,suffix=suffix)
    h50 = sus*h50
    h50_rms = h50.rms()    
    h01 = percentile('H',pctl=1,unit=unit,suffix=suffix)
    h01 = sus*h01    
    h99 = percentile('H',pctl=99,unit=unit,suffix=suffix)
    h99 = sus*h99
    h99_rms = h99.rms()
    h10 = percentile('H',pctl=10,unit=unit,suffix=suffix)
    h10 = sus*h10    
    h90 = percentile('H',pctl=90,unit=unit,suffix=suffix)
    h90 = sus*h90    
    h90_rms = h90.rms()    
    z50 = percentile('Z',pctl=50,unit=unit,suffix=suffix)
    z01 = percentile('Z',pctl=1,unit=unit,suffix=suffix)
    z99 = percentile('Z',pctl=99,unit=unit,suffix=suffix)
    nlnm,nhnm = peterson_noise_model(unit=unit)
    selfnoise = tr120.selfnoise(unit=unit.replace('um','m'))*1e6
    #
    fig, ax = plt.subplots(1,1,figsize=(7.5,10))
    ax.plot_mmm(h50,h10,h90,label='Horizontal (10,50,90 percentile)',color='b')
    if plot_99:
        ax.plot_mmm(h50,h01,h99,label='Horizontal (1,50,99 percentile)',color='r',
                    zorder=0)
    ax.plot(h50_rms,'k--',zorder=3) 
    #ax.plot(h90_rms,'b--',zorder=3)   
    ax.plot(h99_rms,'r--',zorder=3)
    #ax.hlines(1e3,1e-2,3e-2,'k',linewidth=3)    
    #ax.hlines(3.9e0,1e-2,3e-2,'k',linewidth=3)
    #ax.hlines(1.7e-1,1e-2,3e-2,'k',linewidth=3)
    #ax.hlines(1.8e-2,1e-2,3e-2,'k',linewidth=3)
    if plot_v:        
        ax.plot_mmm(z50,z01,z99,label='Vertical (1,50,99 percentile)',color='b')
    if plot_selfnoise:
        ax.loglog(selfnoise,'g--',label='Selfnoise of Seismometer',alpha=1.0)
    if peterson:
        ax.loglog(nlnm[0],nlnm[1],'--',color='gray')
        ax.loglog(nhnm[0],nhnm[1],'--',label='Peterson Low and High Noise Models',
                color='gray')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Frequency [Hz]',fontsize=25)
    ax.set_xlim(2e-2,8)
    if unit=='um/sec':
        ax.set_ylim(1e-5,20)
        ax.set_ylabel('Velocity [um/sec/rtHz]')        
    elif unit=='um':
        ax.set_ylim(5e-6,2e3)
        ax.set_ylabel('Displacement [um/rtHz, or um]',fontsize=25)
    ax.legend(fontsize=18,loc='lower left')
    plt.suptitle('Seismic Noise of KAGRA',fontsize=40)
    fname = './results/seismicnoise_{0}.png'.format(suffix)
    print fname
    plt.savefig(fname)
    plt.close()

if __name__ == '__main__':    
    import os
    files = os.listdir('./data2')
    files = filter(lambda x:'X_99_' in x, files)
    suffix_list = map(lambda x: x.split('_99_')[1][:-5], files)
    suffix_list = filter(lambda x: '1211817600_1245372032' in x,suffix_list) # 1year
    for suffix in suffix_list:
        # for axis in ['X','Y','Z']:
        #     #for axis in ['X']:            
        #     for pctl in [1,10,50,90,99]:
        #         data = percentile(axis,pctl=pctl,unit='um/sec',suffix=suffix)
        #         fname = './LongTerm_{Axis}_{Percentile}_VELO.txt'.format( \
        #             Axis=axis,Percentile=pctl)
        #         data.write(fname)
        #         plt.loglog(data)
        # plt.savefig('hoge.png')
        # plt.close()
        hoge(suffix=suffix,plot_v=False,plot_99=True,unit='um')
