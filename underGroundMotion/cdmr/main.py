import sys
sys.path.insert(0,'../../miyopy')

import numpy as np
from scipy.special import jv
import matplotlib
matplotlib.use('Agg')

from astropy import units as u

from gwpy.plot import Plot
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert
from lalframe.utils import frtools

from miyopy.utils.trillium import Trillium

def read(fname):    
    try:     
        data = FrequencySeries.read(fname,format='hdf5')
    except IOError as ioe:
        print(ioe)
        exit()
    else:
        pass
    
    return data


import argparse 
parser = argparse.ArgumentParser(description='description')
parser.add_argument('dataname',nargs='*', help='data name which you want to calculate')
parser.add_argument('-specgram', action='store_true', help='If given, plot specgram')
args = parser.parse_args()
datanames = args.dataname
specgram = args.specgram

_t0 = {'chname3_1':'Dec 02 2018 11:00:00',
      'chname3_2':'Jan 01 2019 04:00:00',
      'chname3_3':'Jan 02 2019 00:00:00',
      'chname4_1':'May 31 2019 00:00:00',
      'chname4_2':'Jun 2 2019 00:00:00',
      'chname4_3':'Jun 4 2019 00:00:00'}
    

print(datanames)
for dataname in datanames:
    hdf5_fmt = './{dataname}/Xaxis_{sensor}_50pct.hdf5'.replace("{dataname}",dataname)
    hdf5_fmt_csd = './{dataname}/{name}.hdf5'.replace("{dataname}",dataname)
    t0 = _t0[dataname]

    if specgram:
        gwf_fmt = './{dataname}/X.gwf'.replace("{dataname}",dataname)
        chname = frtools.get_channels(gwf_fmt)
        
        data = TimeSeriesDict.read('./{dataname}/X.gwf'.format(dataname=dataname),
                                   chname,
                                   format='gwf.lalframe',
                                   pad=np.nan,
                                   nproc=2,
                                   verbose=True)
        
        # Override unit of data from count to voltage.
        c2v = (10.0/2**15)*u.V/u.ct # [1]
        print data   
        exit()
    
    # Load FrequencySeries from saved hdf5 files.
    if True:
        exv0 = read(hdf5_fmt.format(sensor='exv'))
        ixv1 = read(hdf5_fmt.format(sensor='ixv1'))
        ixv2 = read(hdf5_fmt.format(sensor='ixv2'))
        d12 = read(hdf5_fmt.format(sensor='diff12'))*2
        c12 = read(hdf5_fmt.format(sensor='comm12'))*2
        d13 = read(hdf5_fmt.format(sensor='diff13'))*2   
        c13 = read(hdf5_fmt.format(sensor='comm13'))*2
        csd12 = read(hdf5_fmt_csd.format(name='CSD12'))
        csd13 = read(hdf5_fmt_csd.format(name='CSD13'))
        #ixv1 = ixv1.crop(ixv1.df.value*2)
        #ixv2 = ixv1.crop(ixv2.df.value*2)
        #exv0 = ixv1.crop(exv0.df.value*2)
        print ixv1.shape
        print csd12.shape
        coh12 = csd12/ixv1/ixv2
        coh13 = csd13/ixv1/exv0
        #x1500 = read(hdf5_fmt.format(sensor='x1500'))
        #strain = read(hdf5_fmt.format(sensor='strain'))*3000
        cdmr = c13/d13
        #strain = strain*550.0/strain.frequencies.value
        # ??????????????????????????????????????????????????????????????
        #strain = strain#*3000 # ???????????????????????????
        # ??????????????????????????????????????????????????????????????
        ave = int(2**6*2)
        bw = exv0.df       

    # Calcrate several noises
    if True:
        ref = exv0        
        _adcnoise = 2e-6*u.V*np.ones(len(ref)) # [V/rtHz]
        _adcnoise2 = np.sqrt((10/2**15)**2/12/(214/2))*u.V*np.ones(len(ref)) # [V/rtHz]
        _ampnoise = 6e-7*u.V*np.ones(len(ref)) # [V/rtHz]
        _aanoise = 7e-8*u.V*np.ones(len(ref)) # [V/rtHz]       
        _adcnoise = FrequencySeries(_adcnoise, frequencies=ref.frequencies)
        _adcnoise2 = FrequencySeries(_adcnoise2, frequencies=ref.frequencies)
        _ampnoise = FrequencySeries(_ampnoise, frequencies=ref.frequencies)
        _aanoise = FrequencySeries(_aanoise, frequencies=ref.frequencies)        
        amp = 10**(30/20.)
        tr120q = Trillium('120QA')
        tr240 = Trillium('240')
        v2vel = tr120q.v2vel
        v2vel = tr240.v2vel    
        adcnoise = v2vel(_adcnoise)/amp
        ampnoise = v2vel(_ampnoise)/amp # 
        aanoise = v2vel(_aanoise)/amp   
        selfnoise_120q = tr120q.selfnoise()
        selfnoise_240 = tr240.selfnoise()

    # Plot
    if True:
        from gwpy.plot import Plot
        plot = Plot()
        ax = plot.gca(xscale='log', xlim=(1e-3, 10), xlabel='Frequency [Hz]',
                    yscale='log', ylim=(1e-12, 1e-4),
                    ylabel=r'Velocity [m/sec/\rtHz]'
                    )    
        #ax.loglog(x1500,label='x1500 (ref. GIF data)')    
        ax.loglog(selfnoise_120q,'k--',label='Self Noise 120Q',linewidth=1,alpha=0.7)
        ax.loglog(selfnoise_240,'m--',label='Self Noise 240',linewidth=1,alpha=0.7)
        ax.loglog(adcnoise,'r--',label='ADC Noise',linewidth=1,alpha=0.7)
        ax.loglog(ampnoise,'g--',label='Amp Noise',linewidth=1,alpha=0.7)
        ax.loglog(aanoise,'b--',label='AA Noise',linewidth=1,alpha=0.7)        
        ax.loglog(exv0,'k-',label='EXV')    
        ax.loglog(ixv1,label='IXV1')
        #ax.loglog(ixv2,label='IXV2')
        #ax.loglog(d12,label='IXV1-IXV2')
        #ax.loglog(strain,label='StrainMeter')
        #ImportError: No module named gwpy.plot

        ax.legend(fontsize=8,loc='lower left')    
        ax.set_title('Seismometer, {dname}'.format(dname=dataname.replace('_','')),fontsize=16)
        plot.savefig('./{dname}/ASD_{dname}_X.png'.format(dname=dataname))
        plot.close()
        print('save ./{dname}/ASD_{dname}_X.png'.format(dname=dataname))

#
    f = np.logspace(-3,2,1e4)
    w = 2.0*np.pi*f
    L = 3000.0 # m
    c_p = 5500.0 # m/sec
    cdmr_p = lambda w,c: np.sqrt((1.0+np.cos(L*w/c))/(1.0-np.cos(L*w/c)))
    cdmr_ps = lambda w,c: np.sqrt((1.0+jv(0,2*L*w/c))/(1.0-jv(0,2*L*w/c)))

    
    if True:
        from gwpy.plot import Plot
        import matplotlib.pyplot as plt
        fig, (ax0,ax1) = plt.subplots(2,1,figsize=(8,6),sharex=True)
        plt.subplots_adjust(hspace=0.1)
        ax0.set_ylabel(r'Velocity [m/sec/\rtHz]',fontsize=15)
        ax0.set_xlim(1e-3, 10)        
        ax0.set_ylim(1e-10, 5e-6)
        ax0.loglog(d13,'r',label='IXV1-EXV')
        ax0.loglog(c13,'k',label='IXV1+IXV3')
        ax0.set_yticks([1e-10,1e-9,1e-8,1e-7,1e-6])
        ax0.tick_params(which='minor',color='black',axis='y')
        #ax0.set_yticklabels([1e-10,1e-9,1e-8,1e-7,1e-6],style="sci")
        ax0.legend(fontsize=10,loc='upper right')        
        ax1.loglog(cdmr,'k',label='Measurement',zorder=1)
        ax1.loglog(f,cdmr_ps(w,c_p),'r--',label='Body waves model (5500 m/sec)')
        ax1.loglog(f,cdmr_p(w,c_p),'b--',label='Body wave model (5500 m/sec)')
        ax1.loglog(f,np.ones(10000),'g--',label='No correlation model',zorder=2)
        ax1.text(11, 0.1, 'START : {0}'.format(t0), rotation=90,ha='left',va='bottom')
        ax1.text(13, 0.1, 'BW : {0:2.2e}, Window : hanning, AVE : {1}'.format(bw,ave),
                 rotation=90,ha='left',va='bottom')        
        ax1.legend(fontsize=10,loc='upper right')
        ax1.set_ylim(1e-1, 1e3)
        ax1.set_xlabel('Frequency [Hz]')        
        ax1.set_ylabel(r'CDMR',fontsize=15)
        ax1.set_xlim(1e-3, 10)        
        ax0.set_title('Seismometers, {dname}'.format(dname=dataname.replace('_','')),
                    fontsize=20)
        plt.savefig('./{dname}/CDMR_{dname}_X.png'.format(dname=dataname))
        plt.close()
        print('save ./{dname}/CDMR_{dname}_X.png'.format(dname=dataname))        

    if True:
        # --------------
        # SPAC
        # --------------
        from gwpy.plot import Plot
        fig, ax = plt.subplots(1,1)
        #ax.plot(np.real(coh12),label='csd12')
        #ax.plot(np.real(coh12),label='csd12')
        ax.legend(fontsize=8,loc='lower left')    
        ax.set_title('SPAC, {dname}'.format(dname=dataname.replace('_','')),fontsize=16)
        plt.savefig('./{dname}/SPAC_{dname}_X.png'.format(dname=dataname))
        plt.close()
        print('save ./{dname}/SPAC_{dname}_X.png'.format(dname=dataname))
       
        
