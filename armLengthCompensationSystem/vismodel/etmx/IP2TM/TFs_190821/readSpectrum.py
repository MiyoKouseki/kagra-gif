from control import matlab
import control
from scipy.signal import zpk2tf
from dttpy.dttdata import DttData
import numpy as np
import cmath
def zpq2zpk(fq,omega=True):
    '''
    Convert from non-complex pole or zero to complex ones.
    '''
    f0 = np.array(fq[0])
    if omega:
        f0 = f0/(2.0*np.pi)    
    q = np.array(fq[1])
    w0 = 2.0*np.pi*f0
    if not q==1.0/2.0:
        _p = (-1*w0)/(2.0*q)*(1.0+cmath.sqrt((1.0-2*q)*(1.0+2*q)))
        _m = (-1*w0)/(2.0*q)*(1.0-cmath.sqrt((1.0-2*q)*(1.0+2*q))) 
        return [_p,_m] # [rad Hz]
    else:
        return [-1*w0,np.nan] # [rad Hz]
    
d = DttData('IP_Lexc_wo_control.xml')
print dir(d)
print d.getAllSpectrumName()
chnameA = 'K1:VIS-ETMX_IP_TEST_L_EXC'
chnameB = 'K1:VIS-ETMX_TM_DAMP_L_IN1'
f,asd = d.getASD(chnameA,ref=False)
f,coh,coh_deg = d.getCoherence(chnameB,chnameA,ref=False)
f,mag,deg = d.getTF(chnameB,chnameA)

zeros = np.array([[0.0,10],
                  [0.162,1],
                  [0.66,150],
                  [0.792,200],
                  ])
poles = np.array([[0.04,1],
                  [0.125,4], # 1st, OK 
                  [0.165,0.8], # ?
                  [0.238,1.5], # ?
                  [0.440,7],  # 2nd, OK
                  [0.637,150], # OK
                  [0.735,30], # OK
                  [0.815,150], # OK
                  [0.98,120],
                  [1.015,40],
                  ])
z = np.array(map(zpq2zpk,zeros)).flatten()
p = np.array(map(zpq2zpk,poles)).flatten()
print z
k = [-5.0e-6]
sys = matlab.tf(*zpk2tf(z,p,k))
print sys
fit_mag,fit_phase,omega = control.bode(sys,Plot=False,deg=False,Hz=True,omega=np.logspace(-2,2,1e4))
wrap = lambda phases: ( phases + np.pi) % (2 * np.pi ) - np.pi
fit_phase = np.rad2deg(wrap(fit_phase))
freq = omega#/(2.0*np.pi)
import matplotlib.pyplot as plt
fig, ax = plt.subplots(3,1,sharex=True,figsize=(6,6))
ax[0].loglog(f,mag,label='IP2TM')
ax[0].loglog(freq,fit_mag,label='FIT')
ax[0].set_xlim(5e-3,2e0)
ax[0].set_ylim(3e-5,1)
ax[1].semilogx(f,deg,label='IP2TM')
ax[1].semilogx(freq,fit_phase,label='FIT')
ax[1].set_ylim(-180,180)
ax[1].set_yticks(range(-180,181,90))
# ax[1].semilogx(f,np.rad2deg(np.unwrap(np.deg2rad(deg))),label='IP2TM')
# ax[1].semilogx(freq,np.rad2deg(np.unwrap(np.deg2rad(fit_phase))),label='FIT')
# ax[1].set_ylim(-1080,-0)
# ax[1].set_yticks(range(-1260,1,180))
ax[2].semilogx(f,coh,label='IP2TM')
ax[1].set_xlim(5e-3,2e0)
ax[2].set_xlim(5e-3,2e0)
ax[2].set_ylim(0,1)
ax[0].legend(loc='upper left')
ax[1].legend(loc='upper right')
ax[2].legend(loc='upper left')
plt.savefig('hoge.png')
plt.close()

