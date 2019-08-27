import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from gwpy.frequencyseries import FrequencySeries

def act_lim(fmax,width,mass):
    vel = np.sqrt(2*fmax*width/mass) # kinetic energy
    return vel.decompose()

if __name__ == '__main__':
    # Ground Velocity  
    finess = 50                   #[m] Green Finess
    width = 532e-9*u.m/(2*finess) #[m] Green PDH Linewidth
    fmax = 1.5e-4*u.N             #[N] Max force on IM
    mass = (22.8 + 20.5)*u.kg     #[kg] Mass of (Mirror + IM)
    req_vel = act_lim(fmax,width,mass)
    #print 'Required Ground Velocity : {0:2.1e}'.format(vel)
    #
    req_vel = req_vel.value*1e6    
    x_10 = FrequencySeries.read('./LongTermSeismicNoise/LongTerm_X_10_VELO.txt') # um/sec/rtHz
    x_50 = FrequencySeries.read('./LongTermSeismicNoise/LongTerm_X_50_VELO.txt') # um/sec/rtHz
    x_90 = FrequencySeries.read('./LongTermSeismicNoise/LongTerm_X_90_VELO.txt') # um/sec/rtHz
    w = 2.0*np.pi*x_10.frequencies.value
    x_10 = x_10/w
    x_50 = x_50/w
    x_90 = x_90/w
    x_10 = x_10*np.sqrt(2)
    x_50 = x_50*np.sqrt(2)
    x_90 = x_90*np.sqrt(2)
    x_rms_10 = x_10.rms()
    x_rms_50 = x_50.rms()
    x_rms_90 = x_90.rms()    
    fig,ax = plt.subplots(1,1,figsize=(10,10))
    range_pi = 300
    range_mn = 3
    range_tm = 0.3
    ax.hlines(range_pi,1e-2,10,linestyle='--',linewidth=2)
    ax.text(1,range_pi*1.2,'Actuator Range (PI)',fontsize=20,ha='left')
    ax.hlines(range_mn,1e-2,10,linestyle='--',linewidth=2)
    ax.text(1,range_mn*1.2,'Actuator Range (MN)',fontsize=20,ha='left')
    ax.hlines(range_tm,1e-2,10,linestyle='--',linewidth=2)
    ax.text(1,range_tm*1.2,'Actuator Range (TM)',fontsize=20,ha='left')
    ax.plot_mmm(x_50,x_10,x_90,label='Relative Ground Motion (10th,50th,90th)',color='k')
    ax.plot_mmm(x_rms_50,x_rms_10,x_rms_90,label='RMS (10th,50th,90th)',color='k',linestyle='--')
    ax.set_yscale('log')
    ax.set_ylim(1e-6,1e3)
    ax.set_xscale('log')
    ax.set_xlim(3e-2,10)
    ax.set_ylabel('Displacement [um/rtHz] or RMS [um]',fontsize=25)
    ax.set_xlabel('Frequency [Hz]',fontsize=25)
    ax.legend(fontsize=20,loc='lower left')
    plt.savefig('./results/RequiredGroundVelocity.png')
    plt.close()

    
