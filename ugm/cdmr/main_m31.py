import sys
sys.path.insert(0,'../../miyopy')

import traceback
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

from gwpy.plot import Plot
import matplotlib.pyplot as plt


fname_gwf_tr120 = lambda x: './{id}/TR120s_Xaxis.gwf'.format(id=x)
fname_gwf_gif = lambda x: './{id}/Xaxis_strain.gwf'.format(id=x)
fname_img_asd = './{dname}/ASD_{dname}.png'
fname_img_cdmr = './{dname}/CDMR_{dname}.png'

kwargs = {'pad':np.nan,'nproc':4,'verbose':False,'format':'gwf.lalframe'}
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
    if 'GND_EW' in chnames[0]:
        # 'K1:PEM-SEIS_EXV_GND_EW_IN1_DQ'
        exv_x = list(filter(lambda x:'EXV_GND_EW'in x,chnames))[0]
        ixv_x = list(filter(lambda x:'IXV_GND_EW'in x,chnames))[0]
        ixv_y = list(filter(lambda x:'IXV_GND_NS'in x,chnames))[0]
        eyv_y = list(filter(lambda x:'EYV_GND_NS'in x,chnames))[0]       
    elif 'GND_TR120Q_X' in chnames[0]:
        # 'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ'
        exv_x = list(filter(lambda x:'EXV_GND_TR120Q_X'in x,chnames))[0]
        ixv_x = list(filter(lambda x:'IXV_GND_TR120Q_X'in x,chnames))[0]
        ixv_y = list(filter(lambda x:'IXV_GND_TR120Q_Y'in x,chnames))[0]
        eyv_y = list(filter(lambda x:'EYV_GND_TR120Q_Y'in x,chnames))[0]       
    elif 'EXV_SEIS_WE' in chnames[0]:
        # 'K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ'
        exv_x = list(filter(lambda x:'EXV_SEIS_WE'in x,chnames))[0]
        ixv_x = list(filter(lambda x:'IXV_SEIS_WE'in x,chnames))[0]
        ixv_y = list(filter(lambda x:'IXV_SEIS_NS'in x,chnames))[0]
        eyv_y = list(filter(lambda x:'EYV_SEIS_NS'in x,chnames))[0]       
    elif 'EX1_SEIS_WE' in chnames[0]:
        # 'K1:PEM-EX1_SEIS_WE_SENSINF_IN1_DQ'
        exv_x = list(filter(lambda x:'EX1_SEIS_WE'in x,chnames))[0]
        ixv_x = list(filter(lambda x:'IX1_SEIS_WE'in x,chnames))[0]
        ixv_y = list(filter(lambda x:'IX1_SEIS_NS'in x,chnames))[0]
        eyv_y = list(filter(lambda x:'EY1_SEIS_NS'in x,chnames))[0]       
    return exv_x,ixv_x,ixv_y,eyv_y

def check_data(data,chname):
    try:
        data = data[chname]*c2v/amp
    except:
        print(traceback.format_exc())
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
        print(traceback.format_exc())
        data = None
    return data


if __name__ == '__main__':
    ''' Calculate the CDMR of the X arm and the Y arm.
    '''
    # Parse arguments
    import argparse 
    parser = argparse.ArgumentParser(description='description')
    parser.add_argument('dataname',help='data name which you want to calculate')
    args = parser.parse_args()
    dataname = args.dataname

    # Read timeseries data of Trillium120
    from Kozapy.utils import filelist
    from lib.channel import get_seis_chname
    hoge = {
        'cd3_1':'Dec02 2018 11:00:00',
        'cd3_2':'Jan01 2019 04:00:00',
        'cd3_3':'Jan02 2019 00:00:00',
        'cd3_4':'May31 2019 00:00:00',
        'cd3_5':'Jun02 2019 04:00:00',
        #'cd{a}_{b}':'a+2/b 2019 00:00:00'
    }
    for i in range(4,9,1):
        for j in range(1,32,1):
            hoge['cd{0:02d}_{1:02d}'.format(i,j)] =  \
            '{0:02d}/{1:02d} 2019 00:00:00 JST'.format(i+2,j)
            hoge['cd{0:02d}_{1:02d}d'.format(i,j)] =  \
            '{0:02d}/{1:02d} 2019 12:00:00 JST'.format(i+2,j)
    #
    start = tconvert(hoge[dataname])
    end = start + 2**13
    fname = filelist(start,end)
    chname = get_seis_chname(start,end,place='EXV',axis='X')
    chname += get_seis_chname(start,end,place='IXV',axis='X')
    chname += get_seis_chname(start,end,place='IXV',axis='Y')
    chname += get_seis_chname(start,end,place='EYV',axis='Y')
    try:
        #data = TimeSeriesDict.read(fname,chname,start=start,end=end,**kwargs)        
        data = TimeSeriesDict.read(fname,chname,**kwargs)        
        data = data.crop(start,end)
    except:
        print(traceback.format_exc())
        raise ValueError('!')

    exv_x,ixv_x,ixv_y,eyv_y = check_channel_name(chname)
    exv_x = check_data(data,exv_x)
    ixv_x = check_data(data,ixv_x)
    ixv_y = check_data(data,ixv_y)
    eyv_y = check_data(data,eyv_y)
    d_x = exv_x-ixv_x
    c_x = exv_x+ixv_x
    d_y = eyv_y-ixv_y
    c_y = eyv_y+ixv_y
    #
    t0 = from_gps(exv_x.t0.value)
    fs = exv_x.sample_rate.value
    nlen = exv_x.times.shape[0]
    tlen = nlen/fs
    ave = tlen/overlap
    
    # ASD
    exv_x = asd(exv_x)
    ixv_x = asd(ixv_x)
    ixv_y = asd(ixv_y)
    eyv_y = asd(eyv_y)
    d_x = asd(d_x,integ=integ)
    c_x = asd(c_x,integ=integ)
    cdmr_x = c_x/d_x
    d_y = asd(d_y,integ=integ)
    c_y = asd(c_y,integ=integ)
    cdmr_y = c_y/d_y
    #
    freq = exv_x.frequencies.value
    bw = exv_x.df.value
    
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
    ax.loglog(exv_x,'k-',label='EXV')
    ax.loglog(ixv_x,label='IXV1')
    ax.set_xlim(1e-2,10)
    ax.set_ylim(1e-12,5e-5)
    #ax.loglog(ixv2,label='IXV2')
    #ax.loglog(d12,label='IXV1-IXV2')
    #ax.loglog(strain,label='StrainMeter')
    ax.legend(fontsize=8,loc='lower left')    
    ax.set_title('Seismometer, {dname}'.format(dname=dataname.replace('_','')),
                 fontsize=16)
    plot.savefig(fname_img_asd.format(dname=dataname))
    plot.close()
    print(fname_img_asd.format(dname=dataname))
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
    fig, (ax0,ax1) = plt.subplots(2,1,figsize=(8,6),sharex=True)
    plt.subplots_adjust(hspace=0.1)
    ax0.set_ylabel(r'Velocity [m/sec/\rtHz]',fontsize=15)
    ax0.set_ylim(1e-9,5e-5)
    #ax0.loglog(gif,'g',label='GIF')    
    ax0.loglog(d_x,'r',label='X arm diff.')
    ax0.loglog(c_x,'r--',label='Xarm comm.')
    ax0.loglog(d_y,'b',label='Y arm diff/')
    ax0.loglog(c_y,'b--',label='Y arm comm.')
    ax0.loglog(selfnoise_120q*np.sqrt(2.0),'k--',label='Selfnoise')
    ax0.set_yticks([1e-9,1e-8,1e-7,1e-6,1e-5])
    ax0.tick_params(which='minor',color='black',axis='y')
    #ax0.set_yticklabels([1e-10,1e-9,1e-8,1e-7,1e-6],style="sci")
    ax0.legend(fontsize=10,loc='upper right')        
    ax1.loglog(cdmr_x,'r',label='Xarm',zorder=1)
    ax1.loglog(cdmr_y,'b',label='Yarm',zorder=1)
    ax1.loglog(f,cdmr_r(w,c_r),'m--',label='Uniform Rayleigh waves model (3000 m/sec)')
    ax1.loglog(f,cdmr_p(w,c_p),'g--',label='Single Primary wave model (5500 m/sec)')
    ax1.loglog(f,np.ones(10000),'g--',label='No correlation model',zorder=2)
    ax1.text(11, 0.1, 'START : {0}'.format(t0), rotation=90,ha='left',va='bottom')
    ax1.text(13, 0.1, 'BW : {0:2.2e}, Window : hanning, AVE : {1}'.format(bw,ave),
             rotation=90,ha='left',va='bottom')        
    ax1.legend(fontsize=10,loc='upper right')
    ax1.set_ylim(1e-1, 1e2)
    ax1.set_xlabel('Frequency [Hz]')        
    ax1.set_ylabel(r'CDMR',fontsize=15)
    ax1.set_xlim(1e-2, 10)
    ax0.set_title('Seismometers, {dname}'.format(dname=dataname.replace('_','')),
                  fontsize=20)
    plt.savefig(fname_img_cdmr.format(dname=dataname))
    plt.close()
    print(fname_img_cdmr.format(dname=dataname))
    print('Done')
