from control import matlab
import control
from scipy.signal import zpk2tf
from dttpy.dttdata import DttData
import numpy as np
import cmath

# -----------------
import scipy.io
import scipy
from control import matlab,tf
import control
if control.__version__ != '0.8.2':
    print control.__version__ + '!= 0.8.2'
    exit()
from control import StateSpace
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Read linearized model as ABCD matrix
mat_dict = scipy.io.loadmat("../SuspensionControlModel/script/typeA/linmod/noctrl.mat")
st = mat_dict['linss']
A,B,C,D,statename,outputname,inputname,operpoint,ts = st[0][0]
ss = control.matlab.ss(A, B, C, D)
inputname = np.asarray([i[0][0] for i in inputname])
outputname = np.asarray([i[0][0] for i in outputname])
#print filter(lambda x:'TM' in x,outputname)
# read as SISO
start = 'controlmodel/noiseActIPL'
#start = 'controlmodel/accGndL'
end = 'controlmodel/dispTML'
end = 'controlmodel/OpLev_TML'
idx_from = np.where(inputname==start)[0][0]
idx_to = np.where(outputname==end)[0][0]
print 'From :',idx_from,inputname[idx_from]
print 'To   :',idx_to,outputname[idx_to]
out = ss.returnScipySignalLTI()
ss = out[idx_to][idx_from]
ss_siso = control.ss(ss.A,ss.B,ss.C,ss.D)

# Plot
wrap = lambda phases : ( phases + np.pi) % (2 * np.pi ) - np.pi
f = np.logspace(-3,1,1001)
mag, phase,w = matlab.bode(ss_siso,f*2.0*np.pi,Plot=False)
# -----------------

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
wrap = lambda phases: ( phases + np.pi) % (2 * np.pi ) - np.pi    
    
f,mag = np.loadtxt('./TFs_IP2/190821/IPL2TML.mag',unpack=True)
f,deg = np.loadtxt('./TFs_IP2/190821/IPL2TML.deg',unpack=True)
f,coh = np.loadtxt('./TFs_IP2/190821/IPL2TML.coh',unpack=True)
deg = np.rad2deg(wrap((np.unwrap(np.deg2rad(deg))-np.pi)))
# 
zeros = np.array([[0.0,10],
                  [0.130,1], # !!
                  [0.66,150],
                  [0.792,200],
                  ])
poles = np.array([[0.000,1],
                  [0.075,10],   # 1st,
                  [0.130,1],    # !!
                  [0.211,50],   # 
                  [0.445,150],  # 2nd, OK
                  [0.637,150],  # OK
                  [0.735,150],  # OK
                  [0.815,200],  # OK
                  [0.98,120],   #
                  [1.015,40],
                  [1.2,40],
                  ])
z = np.array(map(zpq2zpk,zeros)).flatten()
p = np.array(map(zpq2zpk,poles)).flatten()
k = [-4.0e-6]
sys = matlab.tf(*zpk2tf(z,p,k))
sys = sys*-1
fit_mag,fit_phase,omega = control.bode(sys,Plot=False,deg=False,Hz=True,omega=np.logspace(-2,2,1e4))
des_mag,des_phase,omega = control.bode(ss_siso,Plot=False,deg=False,Hz=True,omega=np.logspace(-2,2,1e4))
#mag, phase,w = matlab.bode(ss_siso,f*2.0*np.pi,Plot=False)

fit_phase = np.rad2deg(wrap(fit_phase))
freq = omega#/(2.0*np.pi)
import matplotlib.pyplot as plt
fig, ax = plt.subplots(3,1,sharex=True,figsize=(6,6))
ax[0].set_title('TF from IP_L to TM_L',fontsize=15)
ax[0].loglog(f,mag,'ko',label='Measurement',markersize=2)
ax[0].loglog(freq,fit_mag,label='Fitted Model',color='red')
ax[0].loglog(freq/(2.0*np.pi),des_mag*2e1,label='Design',color='blue',alpha=0.5,linestyle='--')
ax[0].set_xlim(1e-2,1e1)
ax[0].set_ylim(3e-5,20)
ax[1].semilogx(f,deg,'ko',label='Measurement',markersize=2)
ax[1].semilogx(freq,fit_phase,label='Fitted Model',color='red')
des_phase = np.rad2deg(wrap(des_phase))
ax[1].semilogx(freq/(2.0*np.pi),des_phase,label='Design',color='blue',alpha=0.5,linestyle='--')
ax[1].set_ylim(-180,180)
ax[1].set_yticks(range(-180,181,90))
ax[1].grid(b=None, which='major', axis='both', linestyle='-')
ax[1].grid(b=None, which='minor', axis='both', linestyle=':')
ax[0].grid(b=None, which='major', axis='both', linestyle='-')
ax[0].grid(b=None, which='minor', axis='both', linestyle=':')
ax[2].semilogx(f,coh,'ko',label='Measurement',markersize=2)
ax[1].set_xlim(1e-2,1e1)
ax[2].set_xlim(1e-2,1e1)
ax[2].set_ylim(0,1)
ax[0].legend(loc='upper right')
ax[2].set_xlabel('Frequency [Hz]',fontsize=15)
ax[2].set_ylabel('Coherence',fontsize=15)
ax[1].set_ylabel('Phase [Deg.]',fontsize=15)
ax[0].set_ylabel('Magnitude',fontsize=15)
plt.savefig('img/IPL2TML.png')
plt.close()
