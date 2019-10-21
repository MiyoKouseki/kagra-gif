import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import matplotlib.pyplot as plt
from gwpy.frequencyseries import FrequencySeries
from gwpy.spectrogram import Spectrogram
from miyopy.utils.trillium import Trillium
from gwpy.types.array2d import Array2D

tr120 = Trillium('120QA')
v2vel = tr120.v2vel    

#------------------------------------------------------------
def peterson_noise_model(unit='um/sec'):
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

    
def _percentile(axis,pctl=50,unit='um/sec',suffix='',_dir='',**kwargs):
    suffix = '1211817600_1245372032'
    fname = './data2/{3}/{0}_{1}_{2}.hdf5'.format(axis,pctl,suffix,_dir)
    _asd = FrequencySeries.read(fname)**0.5
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
    elif axis == 'V':
        return _percentile('Z',**kwargs)
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



def hoge(fname=None,unit='um/sec',**kwargs):
    #
    plot_selfnoise = kwargs.pop('plot_selfnoise',True)
    peterson = kwargs.pop('peterson',True)
    prefix,suffix = fname.split('_compare_')
    path = prefix.split('_')
    dof,suffix = suffix[:-4].split('_with_')        
    dof = dof.split('_vs_')
    option = suffix.split('_')
    dof = list(set(dof))    
    if not len(set(dof)&set(['X','Y','Z','H','V'])):
        path = [path[0]+'_'+_dof for _dof in dof]
        dof = list(filter(lambda x:x in ['X','Y','Z','H','V'], option))
        option  = list(set(option)^set(dof))

    data =  [huge(_dof,_dir=_path,**kwargs) for _dof in dof for _path in path]
    label =  ['{0} {1}'.format(_path,_dof) for _dof in dof for _path in path]
    nlnm,nhnm = peterson_noise_model(unit=unit)
    selfnoise = tr120.selfnoise(unit=unit.replace('um','m'))*1e6
    #
    fig, ax = plt.subplots(1,1,figsize=(10,8))
    colors = ['b','r']
    for _data,_color,_label in zip(data,colors,label):
        asd01,asd10,asd50,asd90,asd99,asdmean = _data
        if '90' in option:
            ax.plot_mmm(asd50,asd10,asd90,color=_color,alpha=0.3,label=_label)
        if '99' in option:
            ax.plot_mmm(asd50,asd01,asd99,color=_color,zorder=0,alpha=0.1)
            
    if plot_selfnoise:
        ax.loglog(selfnoise,'g--',label='Selfnoise of Seismometer',alpha=1.0)
    if peterson:
        ax.loglog(nlnm[0],nlnm[1],'--',color='gray')
        ax.loglog(nhnm[0],nhnm[1],'--',label='Peterson Low and High Noise Models',
                color='gray')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Frequency [Hz]',fontsize=20)
    ax.set_xlim(1e-2,10)
    if unit=='um/sec':
        ax.set_ylim(1e-5,10)
        ax.set_ylabel('Velocity [um/sec/rtHz]',fontsize=20)
    elif unit=='um':
        ax.set_ylim(1e-6,1e2)
        ax.set_yticks(np.logspace(-6,2,9))
        ax.set_ylabel('Displacement [um/rtHz, or um]',fontsize=20)
    ax.legend(fontsize=18,loc='lower left')
    ax.grid(b=True,which='major', axis='both',linestyle='-')
    ax.grid(b=True,which='minor', axis='both',linestyle='--')
    plt.suptitle(fname[:-4],fontsize=40)
    print('./results/'+fname)
    plt.savefig('./results/'+fname)
    plt.close()

if __name__ == '__main__':
    hoge(fname='IXVDIFF_EXVDIFF_compare_X_vs_X_with_90.png')
    hoge(fname='IXVDIFF_IXV_IXVTEST_compare_X_vs_X_with_90.png')
    hoge(fname='IXVDIFF_IXV_IXVTEST_compare_V_vs_V_with_90.png')
    hoge(fname='EXV_compare_V_vs_H_with_90.png')
    hoge(fname='EXV_compare_V_with_90_99.png')
    hoge(fname='EXV_compare_H_with_90_99.png')
    hoge(fname='EXV_compare_day_vs_night_with_H_90.png')
    hoge(fname='EXV_compare_day_vs_night_with_V_90.png')
    hoge(fname='EXV_compare_spring_vs_winter_with_H_90.png')
    hoge(fname='EXV_compare_spring_vs_winter_with_V_90.png')    
    hoge(fname='EXV_compare_spring_vs_summer_with_H_90.png')
    hoge(fname='EXV_compare_spring_vs_summer_with_V_90.png')    
    hoge(fname='EXV_compare_spring_vs_autumn_with_H_90.png')
    hoge(fname='EXV_compare_spring_vs_autumn_with_V_90.png')    
