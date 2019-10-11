import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from gwpy.frequencyseries import FrequencySeries

def act_lim(fmax,width,mass):
    vel = np.sqrt(2*fmax*width/mass) # kinetic energy
    return vel.decompose()

if __name__ == '__main__':
    axis = 'Y'
    asd_10 = FrequencySeries.read('./LongTermSeismicNoise/LongTerm_{0}_10_VELO.txt'.format(axis)) # um/sec/rtHz
    asd_50 = FrequencySeries.read('./LongTermSeismicNoise/LongTerm_{0}_50_VELO.txt'.format(axis)) # um/sec/rtHz
    asd_90 = FrequencySeries.read('./LongTermSeismicNoise/LongTerm_{0}_90_VELO.txt'.format(axis)) # um/sec/rtHz
    fig,ax = plt.subplots(1,1,figsize=(10,10))

    df = asd_10.df.value
    blrms = lambda asd,l,h : np.sqrt((asd**2).crop(l,h).sum()*df*1.5) 
    for asd,name in zip([asd_50,asd_90],['50','90']):
        print '--- {1} {0}th'.format(name,axis)
        for l,h in zip([0.03,0.10,0.30,1.0,3.0,10.0],[0.10,0.30,1.0,3.0,10.0]):
            a = blrms(asd,l,h)
            print '{0:5.2f} - {1:5.2f} Hz : {2:3.1e} um/sec'.format(l,h, a)
            ax.hlines(a,l,h,linestyle='--',linewidth=2,color='red')
    ax.plot_mmm(asd_50,asd_10,asd_90,label='Ground Motion (10th,50th,90th)',color='k')
    
    rms_10 = asd_10.rms()
    rms_50 = asd_50.rms()
    rms_90 = asd_90.rms()        
    ax.plot_mmm(rms_50,rms_10,rms_90,label='RMS (10th,50th,90th)',color='k',linestyle='--')
    ax.set_title(axis)
    ax.set_yscale('log')
    ax.set_ylim(1e-4,1e1)
    ax.set_xscale('log')
    ax.set_xlim(3e-2,10)
    ax.set_ylabel('Displacement [um/sec/rtHz] or RMS [um/sec]',fontsize=25)
    ax.set_xlabel('Frequency [Hz]',fontsize=25)
    ax.legend(fontsize=20,loc='lower left')
    plt.savefig('./results/threshold_{0}.png'.format(axis))
    plt.close()

    
