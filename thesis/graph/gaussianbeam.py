import matplotlib.pyplot as plt
import numpy as np

_z  = np.linspace(-5,5,1000)# = z/z0
_zp = np.linspace(0.1,5,1000)# = z/z0
_zm = np.linspace(-5,-0.1,1000)# = z/z0
_w = lambda _z : np.sqrt((1.0+(_z)**2)) # = w/w0
_R = lambda _z : _z*(1.0+(1.0/_z)**2)  # = R/z0
_theta = lambda _z : _z 
_gouy = lambda _z : np.arctan(_z)
fig,ax = plt.subplots(1,3,figsize=(7,3))
ax[0].plot(_z,_w(_z),color='k',label='Beam Size')
ax[0].plot(_z,_w(_z)*-1,color='k')
ax[0].spines['right'].set_visible(False)
ax[0].spines['top'].set_visible(False)
ax[0].plot(_z,_theta(_z),color='k',linestyle='--')
ax[0].set_ylim(0,4.5)
ax[0].set_yticks([0,1,2,3,4])
ax[0].set_xlim(0,2.5)
ax[0].set_xticks([0,1,2])
ax[0].set_xlabel(r'$z/z_0$',fontsize=15)
ax[0].set_ylabel(r'$w/w_0$',fontsize=15,rotation='horizontal')
ax[0].xaxis.set_tick_params(direction='in')
ax[0].yaxis.set_tick_params(direction='in')
ax[0].yaxis.set_label_coords(-0.15,0.98)
ax[1].plot(_zp,_R(_zp),color='k',linestyle='-')
ax[1].plot(_zm,_R(_zm),color='k',linestyle='-')
ax[1].set_ylim(0,4.5)
ax[1].set_yticks([0,1,2,3,4])
ax[1].set_xlim(0,2.5)
ax[1].spines['right'].set_visible(False)
ax[1].spines['top'].set_visible(False)
ax[1].plot(_z,_theta(_z),color='k',linestyle='--')
ax[1].xaxis.set_tick_params(direction='in')
ax[1].yaxis.set_tick_params(direction='in')
ax[1].set_xlabel(r'$z/z_0$',fontsize=15)
ax[1].set_ylabel(r'$R/z_0$',fontsize=15,rotation='horizontal')
ax[1].set_xticks([0,1,2])
ax[1].yaxis.set_label_coords(-0.15,0.98)
ax[2].plot(_z,_gouy(_z),color='k',linestyle='-')
ax[2].hlines(np.pi/2.0,0,5,linestyle='--')
ax[2].set_ylim(0,3)
ax[2].set_yticks([0,np.pi/4,np.pi/2])
ax[2].set_yticklabels(['0','$\pi/4$','$\pi/2$'],fontsize=10)
ax[2].set_xlim(0,2.5)
ax[2].spines['right'].set_visible(False)
ax[2].spines['top'].set_visible(False)
#ax[2].plot(_z,_theta(_z),color='k',linestyle='--')
ax[2].xaxis.set_tick_params(direction='in')
ax[2].yaxis.set_tick_params(direction='in')
ax[2].set_xlabel(r'$z/z_0$',fontsize=15)
ax[2].set_ylabel(r'$\zeta$',fontsize=15,rotation='horizontal')
ax[2].set_xticks([0,1,2])
ax[2].yaxis.set_label_coords(-0.1,0.98)
#ax[1].grid(linestyle='--')
plt.tight_layout()
plt.savefig('beamprofile.png')
plt.close()
