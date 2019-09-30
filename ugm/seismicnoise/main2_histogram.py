import numpy as np
import matplotlib.pyplot as plt
from gwpy.frequencyseries import FrequencySeries
from gwpy.spectrogram import Spectrogram
from miyopy.utils.trillium import Trillium
from obspy.signal.spectral_estimation import get_nhnm, get_nlnm
from gwpy.types.array2d import Array2D
from gwpy.timeseries import TimeSeries
import astropy.units as u


amp = 10**(30.0/20.0)
c2v = 20.0/2**15

    
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


def _plot_band_histgram(blrms,blrms2,blrms3,scale=0.9,loc=0):
    blrms.override_unit('m/s')    
    blrms = blrms/amp*c2v/1000*1e6
    blrms2 = blrms2/amp*c2v/1000*1e6
    blrms3 = blrms3/amp*c2v/1000*1e6
    #
    hist,bins   = np.histogram(blrms ,density=True,bins=3000,range=(1e-2,10))
    hist2,bins2 = np.histogram(blrms2,density=True,bins=3000,range=(1e-2,10))
    hist3,bins3 = np.histogram(blrms3,density=True,bins=3000,range=(1e-2,10))
    #
    fig, ax = plt.subplots(1,1,figsize=(7,7))
    plt.title('BLRMS Histgram')
    ax.step(bins[:-1],hist,where='post',color='k',label='100-300mHz')
    ax.step(bins2[:-1],hist2*0.5,where='post',color='r',label='100-200mHz')
    ax.step(bins3[:-1],hist3*0.5,where='post',color='b',label='200-300mHz')
    ax.set_ylim(0,10)
    ax.set_xlabel('Horizontal motion [um/sec]')
    ax.set_xscale('log')
    ax.set_xlim(1e-2,10)
    ax.set_ylabel('Normarized Counts')
    ax.legend()
    ax2 = ax.twinx()
    ax2.set_ylabel('Cumulative Probability')
    ax2.plot(bins[:-1],np.cumsum(hist)/np.float(np.sum(hist)),'k--',linewidth=2)
    ax2.plot(bins2[:-1],np.cumsum(hist2)/np.float(np.sum(hist2)),'r--',linewidth=2)
    ax2.plot(bins3[:-1],np.cumsum(hist3)/np.float(np.sum(hist3)),'b--',linewidth=2)
    ax2.set_ylim(0,1)
    ax2.set_yticks([0,0.1,0.5,0.9,1.0])
    ax2.axhline(y=0.10, color='k', linestyle=':',zorder=0)
    ax2.axhline(y=0.50, color='k', linestyle=':',zorder=0)
    ax2.axhline(y=0.90, color='k', linestyle=':',zorder=0)
    plt.savefig('./results/histgram.png')
    plt.close()
    
def plot_band_histgram(blrms,scale=0.9,loc=0,suffix=''):
    blrms.override_unit('m/s')    
    blrms = blrms/amp*c2v/1000*1e6
    #
    #hist,bins   = np.histogram(blrms ,density=False,bins=3000,range=(1e-2,10))
    hist,bins   = np.histogram(blrms ,density=True,bins=3000,range=(1e-2,10))
    #
    fig, ax = plt.subplots(1,1,figsize=(7,7))
    plt.title('BLRMS Histgram')
    ax.step(bins[:-1],hist,where='post',color='k',label='100-300mHz')
    #ax.set_ylim(0,2500)
    ax.set_ylim(0,10)
    ax.set_xlabel('Horizontal motion [um/sec]')
    ax.set_xscale('log')
    ax.set_xlim(1e-2,10)
    #ax.set_ylabel('Normarized Counts')
    ax.set_ylabel('Counts')
    ax.legend()
    ax2 = ax.twinx()
    ax2.set_ylabel('Cumulative Probability')
    ax2.plot(bins[:-1],np.cumsum(hist)/np.float(np.sum(hist)),'k--',linewidth=2)
    ax2.set_ylim(0,1)
    ax2.set_yticks([0,0.1,0.5,0.9,1.0])
    ax2.axhline(y=0.01, color='k', linestyle=':',zorder=0)
    ax2.axhline(y=0.10, color='k', linestyle=':',zorder=0)    
    ax2.axhline(y=0.50, color='k', linestyle=':',zorder=0)
    ax2.axhline(y=0.90, color='k', linestyle=':',zorder=0)
    ax2.axhline(y=0.99, color='k', linestyle=':',zorder=0)
    fname = './results/histgram_{0}.png'.format(suffix)
    print fname
    plt.savefig(fname)
    plt.close()
    

if __name__ == '__main__':
    import os
    files = os.listdir('./data2')
    files = filter(lambda x:'X_BLRMS_100_300mHz_' in x, files)
    for fname in files:
        print fname        
        suffix = fname.split('300mHz_')[1][:-4]
        try:
            chname = 'K1:PEM-EX1_SEIS_WE_SENSINF_IN1_DQ'
            x_blrms = TimeSeries.read('./data2/'+fname,chname)
        except:
            try:
                chname = 'K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ'            
                x_blrms = TimeSeries.read('./data2/'+fname,chname)
            except:
                try:
                    chname = 'K1:PEM-EXV_GND_TR120Q_X_IN1_DQ'
                    x_blrms = TimeSeries.read('./data2/'+fname,chname)
                except:
                    chname = 'K1:PEM-SEIS_EXV_GND_EW_IN1_DQ'
                    x_blrms = TimeSeries.read('./data2/'+fname,chname)                
                    
                
        plot_band_histgram(x_blrms,suffix=suffix)
    # x_blrms = TimeSeries.read('./data2/blrms/Z_100_300mHz_1211817600_1245372032.gwf',chname)
    # x_blrms2 = TimeSeries.read('./data2/blrms/Z_100_200mHz_1211817600_1245372032.gwf',chname)
    # x_blrms3 = TimeSeries.read('./data2/blrms/Z_200_300mHz_1211817600_1245372032.gwf',chname)    
    # __plot_band_histgram(x_blrms,x_blrms2,x_blrms3)
    
