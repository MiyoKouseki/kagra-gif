import numpy as np
import matplotlib.pyplot as plt
from gwpy.frequencyseries import FrequencySeries
from gwpy.spectrogram import Spectrogram
from miyopy.utils.trillium import Trillium
from gwpy.types.array2d import Array2D

tr120 = Trillium('120QA')
v2vel = tr120.v2vel    

#------------------------------------------------------------
def peterson_noise_model(unit='um'):
    ''' Return spectral density of the new seismic model of 
    Peterson using Obspy package.

    This function just converts spectral density as a 
    function of frequencies from a function of period and 
    also changes unit of the spectral acording to given 
    option.
    
    Parameters
    ----------
    unit : `str`, optional
        default is um.

    Returns
    -------
    val : list of `list`
        return the low noise model and the high noise model.

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

    
def _percentile(axis,pctl=50,unit='um',suffix='',_dir='LongTerm_gauss',**kwargs):
    _asd = FrequencySeries.read('./data2/{3}/LongTerm_{0}_{1}_{2}.hdf5'.format(axis,pctl,suffix,_dir))**0.5
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

def mean(axis,**kwargs):
    if axis == 'H':
        x = _mean('X',**kwargs)
        y = _mean('Y',**kwargs)
        return  (x**2 + y**2)**0.5        
    elif axis in ['X','Y','Z']:
        return _mean(axis,**kwargs)
    else:
        raise ValueError('!!!')

    
def huge(axis,**kwargs):
    h01 = percentile(axis,pctl=1 ,**kwargs)
    h10 = percentile(axis,pctl=10,**kwargs)
    h50 = percentile(axis,pctl=50,**kwargs)
    h90 = percentile(axis,pctl=90,**kwargs)
    h99 = percentile(axis,pctl=99,**kwargs)
    h   = percentile(axis,pctl='mean',**kwargs)
    return h01,h10,h50,h90,h99,h
    
def hoge(plot_v=False,plot_99=False,unit='um',peterson=True,plot_selfnoise=True,plot_rms=False,plot_h=False,fname_suffix='',day=False,night=False,season=False,**kwargs):
    #
    kwargs['unit'] = unit
    kwargs['suffix'] = '1211817600_1245372032'
    h01,h10,h50,h90,h99,h             = huge('H',_dir='LongTerm_gauss',**kwargs)
    z01,z10,z50,z90,z99,z             = huge('Z',_dir='LongTerm_gauss',**kwargs)
    h01_n,h10_n,h50_n,h90_n,h99_n,h_n = huge('H',_dir='LongTerm_gauss_night',**kwargs)
    z01_n,z10_n,z50_n,z90_n,z99_n,z_n = huge('Z',_dir='LongTerm_gauss_night',**kwargs)
    h01_d,h10_d,h50_d,h90_d,h99_d,h_d = huge('H',_dir='LongTerm_gauss_day',**kwargs)
    z01_d,z10_d,z50_d,z90_d,z99_d,z_d = huge('Z',_dir='LongTerm_gauss_day',**kwargs)
    h01_1,h10_1,h50_1,h90_1,h99_1,h_1 = huge('H',_dir='LongTerm_gauss_spring',**kwargs)
    z01_1,z10_1,z50_1,z90_1,z99_1,z_1 = huge('Z',_dir='LongTerm_gauss_spring',**kwargs)
    h01_2,h10_2,h50_2,h90_2,h99_2,h_2 = huge('H',_dir='LongTerm_gauss_summer',**kwargs)
    z01_2,z10_2,z50_2,z90_2,z99_2,z_2 = huge('Z',_dir='LongTerm_gauss_summer',**kwargs)
    h01_3,h10_3,h50_3,h90_3,h99_3,h_3 = huge('H',_dir='LongTerm_gauss_autumn',**kwargs)
    z01_3,z10_3,z50_3,z90_3,z99_3,z_3 = huge('Z',_dir='LongTerm_gauss_autumn',**kwargs)
    h01_4,h10_4,h50_4,h90_4,h99_4,h_4 = huge('H',_dir='LongTerm_gauss_winter',**kwargs)
    z01_4,z10_4,z50_4,z90_4,z99_4,z_4 = huge('Z',_dir='LongTerm_gauss_winter',**kwargs)
    #
    nlnm,nhnm = peterson_noise_model(unit=unit)
    selfnoise = tr120.selfnoise(unit=unit.replace('um','m'))*1e6
    #
    fig, ax = plt.subplots(1,1,figsize=(10,8))

    if plot_h:
        if plot_v:
            color = 'b'
        else:
            plt.suptitle('Horizontal Seismic Noise',fontsize=40)                      
            color = 'b'
        if (not night ) and (not day) and (not season):
            ax.plot_mmm(h50,h10,h90,label='Horizontal (10,50,90 percentile)',
                        color=color,alpha=0.3)
            if plot_99:
                ax.plot_mmm(h50,h01,h99,label='Horizontal (1,50,99 percentile)',
                            color=color,zorder=0,alpha=0.1)
        if season:
            ax.plot_mmm(h50_1,h10_1,h90_1,zorder=0,alpha=0.2,label='Spring',color='b')
            #ax.plot_mmm(h50_2,h10_2,h90_2,zorder=0,alpha=0.2,label='Summer')
            #ax.plot_mmm(h50_3,h10_3,h90_3,zorder=0,alpha=0.2,label='Autumn')
            ax.plot_mmm(h50_4,h10_4,h90_4,zorder=0,alpha=0.2,label='Winter',color='r') 
            plt.suptitle('Spring vs. Winter (Horizontal)',fontsize=40)      
        if night:
            ax.plot_mmm(h50_n,h10_n,h90_n,label='Night (10,50,90 percentile)',
                        color='b',alpha=0.3)
        if day:
            plt.suptitle('Night vs. Day (Horizontal)',fontsize=40)                
            ax.plot_mmm(h50_d,h10_d,h90_d,label='Day (10,50,90 percentile)',
                        color='r',alpha=0.3)            
        if plot_rms:
            ax.plot(h50_rms,'k--',zorder=3) 
            ax.plot(h99_rms,'r--',zorder=3)        
    if plot_v:
        if plot_h:
            color = 'r'
            plt.suptitle('Horizontal vs. Vertical',fontsize=40)            
        else:
            plt.suptitle('Vertical Seismic Noise',fontsize=40)            
            color = 'r'
        if (not night) and (not day) and (not season):
            ax.plot_mmm(z50,z10,z90,label='Vertical (10,50,90 percentile)',
                        color=color,alpha=0.3)
            if plot_99:                
                ax.plot_mmm(z50,z01,z99,label='Vertical (1,50,99 percentile)',
                            color=color,alpha=0.1)
        if season:
            ax.plot_mmm(z50_1,z10_1,z90_1,zorder=0,alpha=0.2,label='Spring',color='b')
            #ax.plot_mmm(z50_2,z10_2,z90_2,zorder=0,alpha=0.2,label='Summer')
            #ax.plot_mmm(z50_3,z10_3,z90_3,zorder=0,alpha=0.2,label='Autumn')
            ax.plot_mmm(z50_4,z10_4,z90_4,zorder=0,alpha=0.2,label='Winter',color='r') 
            plt.suptitle('Spring vs. Winter (Vertical)',fontsize=40)            
        if night:
            ax.plot_mmm(z50_n,z10_n,z90_n,label='Night (10,50,90 percentile)',
                        color='b',alpha=0.3)
        if day:
            plt.suptitle('Night vs. Day (Vertical)',fontsize=40)                        
            ax.plot_mmm(z50_d,z10_d,z90_d,label='Day (10,50,90 percentile)',
                        color='r',alpha=0.3)            
            
    if plot_selfnoise:
        ax.loglog(selfnoise,'g--',label='Selfnoise of Seismometer',alpha=1.0)
    if peterson:
        ax.loglog(nlnm[0],nlnm[1],'--',color='gray')
        ax.loglog(nhnm[0],nhnm[1],'--',label='Peterson Low and High Noise Models',
                color='gray')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Frequency [Hz]',fontsize=25)
    ax.set_xlim(1e-2,10)
    if unit=='um/sec':
        ax.set_ylim(1e-5,10)
        ax.set_ylabel('Velocity [um/sec/rtHz]')        
    elif unit=='um':
        ax.set_ylim(1e-6,1e2)
        ax.set_yticks(np.logspace(-6,2,9))
        ax.set_ylabel('Displacement [um/rtHz, or um]',fontsize=25)
    ax.legend(fontsize=18,loc='lower left')
    ax.grid(b=True,which='major', axis='both',linestyle='-')
    ax.grid(b=True,which='minor', axis='both',linestyle='--')    
    fname = './results/seismicnoise_{0}.png'.format(fname_suffix)
    print(fname)
    plt.savefig(fname)
    plt.close()

if __name__ == '__main__':    
    import os
    files = os.listdir('./data2/LongTerm_gauss')
    files = filter(lambda x:'X_99_' in x, files)
    suffix_list = map(lambda x: x.split('_99_')[1][:-5], files)
    suffix_list = filter(lambda x: '1211817600_1245372032' in x,suffix_list) # 1year
    for suffix in suffix_list:
        hoge(plot_v=True, plot_h=True, plot_99=False,fname_suffix='all_compare_v_vs_h')
        hoge(plot_v=True, plot_h=False,plot_99=True, fname_suffix='all_v_99')
        hoge(plot_v=False,plot_h=True, plot_99=True, fname_suffix='all_h_99')
        hoge(plot_h=True, day=True,night=True,fname_suffix='h_compare_day_vs_night')
        hoge(plot_v=True, day=True,night=True,fname_suffix='v_compare_day_vs_night')
        hoge(plot_h=True, season=True,fname_suffix='h_compare_season')
        hoge(plot_v=True, season=True,fname_suffix='v_compare_season')
