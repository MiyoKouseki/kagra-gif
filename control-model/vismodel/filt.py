from scipy import signal
import numpy as np
from control import matlab
import matplotlib.pyplot as plt
from utils import mybode,degwrap

def servo(f0=0.1,f1=5,gain=5e3):
    w0 = 2.0*np.pi*f0
    w1 = 2.0*np.pi*f1
    num,den = signal.zpk2tf([-w0,-w0],[0,-w1],[gain])
    servo = matlab.tf(num,den)
    return servo

def servo2(f0=0.1,f1=5,gain=5e3):
    w0 = 2.0*np.pi*f0
    w1 = 2.0*np.pi*f1
    num,den = signal.zpk2tf([-w0,-w0],[0,-w1,-w1],[gain])
    servo = matlab.tf(num,den)
    return servo

def servo3(f0=0.1,f1=5,gain=5e3):
    w0 = 2.0*np.pi*f0    
    w1 = 2.0*np.pi*f1
    num,den = signal.zpk2tf([-w0],[-w1,-w1],[gain])
    servo = matlab.tf(num,den)
    return servo



def blendfilter(fb=0.1,n=4,plot=True):
    wb=fb*(2.0*np.pi)
    #wb=1
    freq = np.logspace(-3,3,1e5)
    if n==5:
        lp = matlab.tf([126*wb**5,84*wb**6,36*wb**7,9*wb**8,wb**9],
                       [1,9*wb**1,36*wb**2,84*wb**3,126*wb**4,126*wb**5,84*wb**6,36*wb**7,9*wb**8,wb**9])
        hp = matlab.tf([1,9*wb**1,36*wb**2,84*wb**3,126*wb**4,0,0,0,0,0],
                       [1,9*wb**1,36*wb**2,84*wb**3,126*wb**4,126*wb**5,84*wb**6,36*wb**7,9*wb**8,wb**9])
    elif n==4:
        lp = matlab.tf([35*wb**4,21*wb**5,7*wb**6,wb**7],
                       [1,7*wb**1,21*wb**2,35*wb**3,35*wb**4,21*wb**5,7*wb**6,wb**7])
        hp = matlab.tf([1,7*wb**1,21*wb**2,35*wb**3,0,0,0,0],
                       [1,7*wb**1,21*wb**2,35*wb**3,35*wb**4,21*wb**5,7*wb**6,wb**7])
    elif n==3:
        lp = matlab.tf([10*wb**3,5*wb**4,wb**5],
                       [1,5*wb**1,10*wb**2,10*wb**3,5*wb**4,wb**5])
        hp = matlab.tf([1,5*wb**1,10*wb**2,0,0,0],
                       [1,5*wb**1,10*wb**2,10*wb**3,5*wb**4,wb**5])                    
    else:
        lp,hp = None,None
        
    mag_lp,phase_lp = mybode(lp,freq=freq,Plot=False)
    mag_hp,phase_hp = mybode(hp,freq=freq,Plot=False)    
    
    if plot:
        fig ,[ax0,ax1] = plt.subplots(2,1,figsize=(8,8),dpi=100)
        plt.suptitle('Blending filter',fontsize=30)
        ax0.loglog(mag_lp,'k',label='lp')
        ax0.loglog(mag_hp,'k--',label='hp')
        ax0.set_xlim(1e-3,1e1)
        ax0.set_ylim(1e-4,1e1)
        ax0.set_yticks([1e-4,1e-3,1e-2,1e-1,1e0,1e1])
        ax0.grid(b=True, which='major', color='gray', linestyle=':')
        ax0.grid(b=True, which='minor', color='gray', linestyle=':')
        ax0.legend(loc='lower left')
        ax0.set_ylabel('Magnitude ')
        ax1.semilogx(phase_lp,'k',alpha=0.5)
        ax1.semilogx(phase_hp,'k--',alpha=0.5)
        ax1.set_ylim(-180,180)
        ax1.set_yticks(np.arange(-180,181,90))
        ax1.set_xlim(1e-3,1e1)
        ax1.set_xlabel('Frequency [Hz]')
        ax1.set_ylabel('Phase [degree]')
        ax1.grid(b=True, which='major', color='gray', linestyle=':')
        ax1.grid(b=True, which='minor', color='gray', linestyle=':')
        plt.savefig('img_blend.png'.format(fb))            
    return lp,hp

