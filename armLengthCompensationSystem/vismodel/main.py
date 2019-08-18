import numpy as np
import matplotlib.pyplot as plt
from etmx import Gain, pole_QFK, zero_QFK
from etmx import qfk_mag,qfk

data = np.loadtxt('./etmx/tfmodel.txt')
freq = data[:,0]
mag = data[:,1]
phase = data[:,2]
param = np.r_[Gain,pole_QFK.flatten(),zero_QFK.flatten()]
_freq = np.logspace(-2,2,1e6)
h = qfk(_freq,*param)
_mag,_phase = np.abs(h),np.rad2deg(np.angle(h))


fig , [ax0,ax1] = plt.subplots(2,1)
ax0.loglog(freq,mag,'ko',markersize=1,label='ETMX L (Measured)')
ax0.loglog(_freq,_mag,'r',linewidth=1,label='ETMX L (Fit)')
ax0.set_ylabel('Magnitude')
ax1.semilogx(freq,phase,'ko',markersize=1)
ax1.semilogx(_freq,_phase,'r',linewidth=1)
ax1.set_ylim(-180,180,90)
ax1.set_yticks(np.arange(-180,181,90))
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Phase [Deg.]')
ax0.legend()
plt.savefig('./TF_ETMX.png')



