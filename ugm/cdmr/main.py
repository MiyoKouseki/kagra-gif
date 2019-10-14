import sys
sys.path.insert(0,'../../miyopy')

import numpy as np
from scipy.special import jv
import matplotlib
matplotlib.use('Agg')

from astropy import units as u
from lalframe.utils import frtools

from gwpy.plot import Plot
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert,from_gps
from miyopy.utils.trillium import Trillium

fname_gwf_tr120 = lambda x: './{id}/TR120s_Xaxis.gwf'.format(id=x)
fname_gwf_gif = lambda x: './{id}/Xaxis_strain.gwf'.format(id=x)

kwargs = {'pad':np.nan,'nproc':2,'verbose':False,'format':'gwf.lalframe'}
c2v = (20.0/2**15)*u.V/u.ct
tr120q = Trillium('120QA')
tr240 = Trillium('240')
v2vel_120 = tr120q.v2vel
v2vel_240 = tr240.v2vel
amp = 10**(30./20.)
unit = 'm'
if unit == 'm':
    integ=True
use_gif = False
    
fftlen = 2**8
overlap = fftlen/2
    
def check_channel_name(chnames):
    if any(map(lambda x:'TEST' in x, chnames)): # IXV_TEST
        exv  = list(filter(lambda x:'EXV'in x,chnames))[0]
        ixv = list(filter(lambda x:'IXV'in x and not 'TEST'in x,chnames))[0]
        ixv2 = list(filter(lambda x:'IXV'in x and 'TEST'in x,chnames))[0]
        eyv = None
    else:
        exv  = list(filter(lambda x:'EXV'in x,chnames))[0]
        ixv = list(filter(lambda x:'IXV'in x,chnames))[0]
        ixv2 = None
        eyv = list(filter(lambda x:'EYV'in x,chnames))[0]       
    return exv,ixv,ixv2,eyv

def check_data(data,chname):
    try:
        data = data[chname]*c2v/amp
    except:
        data = None
    return data

def asd(data,integ=True):
    try:
        data = data.asd(fftlength=fftlen,overlap=overlap)
        data = v2vel_120(data)
        if integ:
            freq = data.frequencies.value
            data = data/(2.0*np.pi*freq)
    except:
        data = None
    return data


if __name__ == '__main__':
    # Parse arguments
    import argparse 
    parser = argparse.ArgumentParser(description='description')
    parser.add_argument('dataname',help='data name which you want to calculate')
    args = parser.parse_args()
    dataname = args.dataname

    # Read timeseries data of Trillium120
    from Kozapy.utils import filelist
    from lib.channel import get_seis_chname
    m31 = True
    if m31:
        start = tconvert('May31 2019 00:00:00')
        end = start + 2**13
        fname = filelist(start,end)
        chname = get_seis_chname(start,end,place='EXV')
        print(chname)
    else:
        fname = fname_gwf_tr120(dataname)
        chname = frtools.get_channels(fname)        
    try:
        data = TimeSeriesDict.read(fname,chname,**kwargs)
    except:
        print(fname)
        raise ValueError('!')

    exv,ixv,ixv2,eyv = check_channel_name(chname)
    exv = check_data(data,exv)
    ixv = check_data(data,ixv)
    ixv2 = check_data(data,ixv2)
    eyv = check_data(data,eyv)
    if ixv2 != None:
        d12 = ixv-ixv2
        c12 = ixv+ixv2
    d31 = exv-ixv
    c31 = exv+ixv
    t0 = exv.t0.value
    fs = exv.sample_rate.value
    nlen = exv.times.shape[0]
    tlen = nlen/fs
    ave = tlen/overlap

    # Read GIF
    if use_gif:
        fname = fname_gwf_gif(dataname)
        chname = frtools.get_channels(fname)[0]
        gif = TimeSeries.read(fname,chname,**kwargs)
        gif = gif.asd(fftlength=fftlen,overlap=overlap)*3000
    
    # ASD
    exv = asd(exv)
    ixv = asd(ixv)
    ixv2 = asd(ixv2)
    eyv = asd(eyv)
    if ixv2 != None:    
        d12 = asd(d12)
        c12 = asd(c12)
        cdmr12 = c12/d12        
    d31 = asd(d31,integ=integ)
    c31 = asd(c31,integ=integ)
    cdmr31 = c31/d31
    freq = exv.frequencies.value
    bw = exv.df.value

    
    # Read Noise
    _adcnoise = 2e-6*u.V*np.ones(len(freq)) # [V/rtHz]
    _adcnoise2 = np.sqrt((10/2**15)**2/12/(214/2))*u.V*np.ones(len(freq)) # [V/rtHz]
    _ampnoise = 6e-7*u.V*np.ones(len(freq)) # [V/rtHz]
    _aanoise = 7e-8*u.V*np.ones(len(freq)) # [V/rtHz]       
    _adcnoise = FrequencySeries(_adcnoise, frequencies=freq)
    _adcnoise2 = FrequencySeries(_adcnoise2, frequencies=freq)
    _ampnoise = FrequencySeries(_ampnoise, frequencies=freq)
    _aanoise = FrequencySeries(_aanoise, frequencies=freq)        
    adcnoise = v2vel_120(_adcnoise)/amp
    ampnoise = v2vel_120(_ampnoise)/amp # 
    aanoise = v2vel_120(_aanoise)/amp   
    selfnoise_120q = tr120q.selfnoise(unit=unit)
    selfnoise_240 = tr240.selfnoise(unit=unit)
    # 
    # Plot 
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 10), xlabel='Frequency [Hz]',
                  yscale='log', ylim=(1e-12, 1e-4),
                  ylabel=r'Velocity [{0}/\rtHz]'.format(unit))
    #ax.loglog(x1500,label='x1500 (ref. GIF data)')    
    ax.loglog(selfnoise_120q,'k--',label='Self Noise 120Q',linewidth=1,alpha=0.7)
    #ax.loglog(selfnoise_240,'m--',label='Self Noise 240',linewidth=1,alpha=0.7)
    #ax.loglog(adcnoise,'r--',label='ADC Noise',linewidth=1,alpha=0.7)
    #ax.loglog(ampnoise,'g--',label='Amp Noise',linewidth=1,alpha=0.7)
    #ax.loglog(aanoise,'b--',label='AA Noise',linewidth=1,alpha=0.7)
    ax.loglog(exv,'k-',label='EXV')
    ax.loglog(ixv,label='IXV1')
    ax.set_xlim(1e-2,10)
    #ax.loglog(ixv2,label='IXV2')
    #ax.loglog(d12,label='IXV1-IXV2')
    #ax.loglog(strain,label='StrainMeter')
    ax.legend(fontsize=8,loc='lower left')    
    ax.set_title('Seismometer, {dname}'.format(dname=dataname.replace('_','')),
                 fontsize=16)
    plot.savefig('./{dname}/ASD_{dname}_X.png'.format(dname=dataname))
    plot.close()
    print('save ./{dname}/ASD_{dname}_X.png'.format(dname=dataname))
    #
    # Plot 
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 10), xlabel='Frequency [Hz]',
                  yscale='log', ylim=(1e-12, 1e-4),
                  ylabel=r'Velocity [{0}/\rtHz]'.format(unit))
    ax.loglog(selfnoise_120q,'k--',label='Self Noise 120Q',linewidth=1,alpha=0.7)
    ax.loglog(exv,'k-',label='EXV')
    ax.loglog(ixv,label='IXV1')
    ax.set_xlim(1e-2,10)
    if ixv2 != None:    
        ax.loglog(ixv2,label='IXV2')
        ax.loglog(d12,label='IXV1-IXV2')
    ax.legend(fontsize=8,loc='lower left')    
    ax.set_title('Seismometer, {dname}'.format(dname=dataname.replace('_','')),
                 fontsize=16)
    plot.savefig('./{dname}/ASD_DIFFNOISE_{dname}_X.png'.format(dname=dataname))
    plot.close()
    print('save ./{dname}/ASD_DIFFNOISE_{dname}_X.png'.format(dname=dataname))
    #    
    #
    #
    #
    #
    f = np.logspace(-3,2,1e4)
    w = 2.0*np.pi*f
    L = 3000.0 # m
    c_p = 5500.0 # m/sec
    c_r = 3000.0 # m/sec
    cdmr_p = lambda w,c: np.sqrt((1.0+np.cos(L*w/c))/(1.0-np.cos(L*w/c)))
    cdmr_r = lambda w,c: np.sqrt((1.0+jv(0,2*L*w/c))/(1.0-jv(0,2*L*w/c)))
    from gwpy.plot import Plot
    import matplotlib.pyplot as plt
    fig, (ax0,ax1) = plt.subplots(2,1,figsize=(8,6),sharex=True)
    plt.subplots_adjust(hspace=0.1)
    ax0.set_ylabel(r'Velocity [m/sec/\rtHz]',fontsize=15)
    ax0.set_ylim(1e-9, 5e-6)
    #ax0.loglog(gif,'g',label='GIF')    
    ax0.loglog(d31,'r',label='IXV1-EXV')
    ax0.loglog(c31,'k',label='IXV1+IXV3')
    ax0.loglog(selfnoise_120q*np.sqrt(2.0),'k--',label='Selfnoise')
    ax0.set_yticks([1e-9,1e-8,1e-7,1e-6])
    ax0.tick_params(which='minor',color='black',axis='y')
    #ax0.set_yticklabels([1e-10,1e-9,1e-8,1e-7,1e-6],style="sci")
    ax0.legend(fontsize=10,loc='upper right')        
    ax1.loglog(cdmr31,'k',label='Measurement',zorder=1)
    ax1.loglog(f,cdmr_r(w,c_r),'r--',label='Uniform Rayleigh waves model (3000 m/sec)')
    ax1.loglog(f,cdmr_p(w,c_p),'b--',label='Single Primary wave model (5500 m/sec)')
    ax1.loglog(f,np.ones(10000),'g--',label='No correlation model',zorder=2)
    ax1.text(11, 0.1, 'START : {0}'.format(t0), rotation=90,ha='left',va='bottom')
    ax1.text(13, 0.1, 'BW : {0:2.2e}, Window : hanning, AVE : {1}'.format(bw,ave),
             rotation=90,ha='left',va='bottom')        
    ax1.legend(fontsize=10,loc='upper right')
    ax1.set_ylim(1e-1, 1e3)
    ax1.set_xlabel('Frequency [Hz]')        
    ax1.set_ylabel(r'CDMR',fontsize=15)
    ax1.set_xlim(1e-2, 10)
    ax0.set_title('Seismometers, {dname}'.format(dname=dataname.replace('_','')),
                  fontsize=20)
    plt.savefig('./{dname}/CDMR_{dname}_X.png'.format(dname=dataname))
    plt.close()
    print('save ./{dname}/CDMR_{dname}_X.png'.format(dname=dataname))
