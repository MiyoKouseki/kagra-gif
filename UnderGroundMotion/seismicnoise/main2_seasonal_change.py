
import numpy as np
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import from_gps,tconvert

from lib.iofunc import fname_hdf5_longasd
import matplotlib.pyplot as plt
from miyopy.utils.trillium import Trillium



def _percentile(axis,pctl=50,unit='um/sec',**kwargs):
    suffix = '_{0}_{1}'.format(start,end)
    fname = fname_hdf5_longasd(axis,pctl,suffix=suffix,prefix='./tmp')
    _asd = FrequencySeries.read(fname)**0.5
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
    if axis in ['H','Horizontal']:        
        x = _percentile('X',**kwargs)
        y = _percentile('Y',**kwargs)
        return  (x**2 + y**2)**0.5
    elif axis in ['Z','Vertical','UD']:
        axis = 'Z'
        return _percentile(axis,**kwargs)    
    elif axis in ['X','Y']:
        return _percentile(axis,**kwargs)
    else:
        raise ValueError('!!!')

def peterson_noise_model(unit='um/sec'):
    '''
    Return 
    
    '''
    from obspy.signal.spectral_estimation import get_nhnm, get_nlnm    
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

    

jobs = 8
tlen = 2**25
bins = tlen/jobs
segments = zip(range(1211817600     ,1245372032+1,bins),
               range(1211817600+bins,1245372032+1,bins))


tr120 = Trillium('120QA')
v2vel = tr120.v2vel    

unit = 'um'

import matplotlib.cm as cm
for axis in ['Vertical','Horizontal']:
    fig,ax = plt.subplots(1,1,figsize=(8,8))    
    fname_img = './tmp/LongTerm_{0}.png'.format(axis[0])
    for i,(start,end) in enumerate(segments):
        tlen = end - start
        bins = tlen/8
        jan01 = tconvert('Jan 01 2019 00:00:00 JST')
        jun01 = tconvert('Jun 01 2018 00:00:00 JST')
        halfofyear = float(jan01-jun01)
        #
        pctl = 50
        data = percentile(axis,pctl=pctl,unit=unit)
        _start,_end = str(from_gps(start)).split(' ')[0], str(from_gps(end)).split(' ')[0]
        val = abs(float(abs(start-jan01)/halfofyear) -1 )
        ax.plot(data,label='{0} - {1}'.format(_start,_end),
                color=cm.viridis(val),linewidth=2)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlim(1e-2,8)
    nlnm,nhnm = peterson_noise_model(unit=unit)    
    ax.loglog(nlnm[0],nlnm[1],'k--')
    ax.loglog(nhnm[0],nhnm[1],'k--',label='Peterson Low and High Noise Models')
    ax.set_xlabel('Frequency [Hz]')
    if unit=='um/sec':
        ax.set_ylim(1e-4,20)    
        ax.set_ylabel('Velocity [um/sec/rtHz]')        
    elif unit=='um':
        ax.set_ylim(5e-6,20)
        ax.set_ylabel('Displacement [um/rtHz]')
    plt.title('{0}th Percentile of {1} Motion'.format(pctl,axis),fontsize=25)
    plt.legend(ncol=2,loc='lower center',fontsize=13)
    plt.savefig(fname_img)
    plt.close()
#
#
for i,(start,end) in enumerate(segments):
    fig,ax = plt.subplots(1,1,figsize=(8,8))
    fname_img = './tmp/LongTerm_{0}_{1}.png'.format(start,end)
    for axis in ['Vertical','Horizontal']:
        data = {}        
        for pctl in [10,50,90]:
            data[pctl] = percentile(axis,pctl=pctl,unit=unit)
        ax.plot_mmm(data[50],data[10],data[90],label=axis)    
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylim(1e-4,20)
    ax.set_xlim(1e-2,8)
    nlnm,nhnm = peterson_noise_model(unit=unit)    
    ax.loglog(nlnm[0],nlnm[1],'k--')
    ax.loglog(nhnm[0],nhnm[1],'k--',label='Peterson Low and High Noise Models')    
    print fname_img
    start,end = str(from_gps(start)).split(' ')[0],str(from_gps(end)).split(' ')[0]    
    plt.title('{0}/{1} : {2} - {3}'.format(i+1,jobs,start,end),fontsize=30)
    plt.legend()
    ax.set_xlabel('Frequency [Hz]')    
    if unit=='um/sec':
        ax.set_ylim(1e-5,20)
        ax.set_ylabel('Velocity [um/sec/rtHz]')        
    elif unit=='um':
        ax.set_ylim(5e-6,20)
        ax.set_ylabel('Displacement [um/rtHz]')    
    plt.savefig(fname_img)
    plt.close()

