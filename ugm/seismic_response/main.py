#
#
import numpy as np
import matplotlib.pyplot as plt

import argparse
parser = argparse.ArgumentParser(description='This script is ...')
parser.add_argument('tfs')
args = parser.parse_args()

start = 'Sep 06 00:30 JST'
end = 'Sep 06 01:30 JST'

f = np.logspace(-3,1,int(1e5))
w = 2.*np.pi*f

v = 5000.0
phi3000 = w*3000.0/(v)
phi1500 = w*1500.0/(v)

def tf_strain(tau,s):
    return (1-np.exp(-tau*s))*(v/s)

def tf_disp(tau,s): #dL/u
    return (1-np.exp(-tau*s))


s = 1j*w


tfs = ['gif2xarm','strain2gif','disp2gif']

_tf = tfs[0]
_tf = args.tfs

fig,ax = plt.subplots(2,1,figsize=(6,5),sharex=True)

if _tf=='gif2xarm':
    title=r'$G_{\Delta{L_{GIF}} \rightarrow \Delta{L_{XARM}}}$'
    label=None
    H = tf_disp(3000.0/v,s)/tf_disp(1500.0/v,s)    
    ax[0].loglog(f,np.abs(H),color='k')
    ax[1].semilogx(f,np.rad2deg(np.angle(H)),color='k')    
    ax[0].set_ylim(1e-3,1e1)
    fname = 'img_dLGIF2dLXARM.png'
elif _tf=='strain2gif':
    H1 = tf_strain(1500.0/v,s)
    ax[0].loglog(f,np.abs(H1),color='k',label='L=1500')
    ax[1].semilogx(f,np.rad2deg(np.angle(H1)),color='k')
    H2 = tf_strain(3000.0/v,s)
    ax[0].loglog(f,np.abs(H2),color='k',linestyle='--',label='L=3000')
    ax[1].semilogx(f,np.rad2deg(np.angle(H2)),color='k',linestyle='--')
    title=r'$G_{\epsilon \rightarrow \Delta{L}}$'    
    ax[0].legend()    
    ax[0].set_ylim(1e0,1e4)
    ax[0].legend()
    fname = 'img_strain2dL.png'
    ax[0].set_ylabel('Magnitude [m]',fontsize=10)    
elif _tf=='disp2gif':
    H1 = tf_disp(1500.0/v,s)
    ax[0].loglog(f,np.abs(H1),color='k',label='L=1500')
    ax[1].semilogx(f,np.rad2deg(np.angle(H1)),color='k')
    H2 = tf_disp(3000.0/v,s)
    ax[0].loglog(f,np.abs(H2),color='k',linestyle='--',label='L=3000')
    ax[1].semilogx(f,np.rad2deg(np.angle(H2)),color='k',linestyle='--')
    ax[0].legend()
    title=r'$G_{u \rightarrow \Delta{L}}$'
    label='G1500'
    ax[0].set_ylim(1e-3,1e1)
    fname = 'img_disp2dL.png'
    ax[0].set_ylabel('Magnitude',fontsize=10)    
else:
    raise ValueError('No Name')


#ax[0].set_title(title)
plt.suptitle(title,fontsize=20)
ax[1].set_yticks(range(-180,181,90))
ax[1].set_ylim(-180,180)
ax[1].set_xlim(1e-3,1e1)
ax[0].grid(linestyle='-', which='major', axis='both')
ax[0].grid(linestyle='--', which='minor', axis='both')
ax[1].grid(linestyle='-', which='major', axis='both')
ax[1].grid(linestyle='--', which='minor', axis='both')
ax[0].yaxis.set_label_coords(-0.1,0.5)
ax[1].yaxis.set_label_coords(-0.1,0.5)
ax[1].set_ylabel('Phase [Deg.]',fontsize=10)
ax[1].set_xlabel('Frequency [Hz]',fontsize=10)
plt.savefig(fname)
print(fname)
plt.close()
