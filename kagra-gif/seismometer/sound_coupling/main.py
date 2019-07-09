import matplotlib.pyplot as plt
import numpy as np

from dttpy.dttdata import DttData
from miyopy.utils.trillium import selfnoise,vel2vel

c2V = 10.0/2**15 # V/count
p0 = 20*1e-6 # Pa
mic_noise = 10**(17.0/20.0)*p0 # Pa
mic_maximum = 10**(135/20.0)*p0 # Pa

d = DttData('ixv_micseis_mZaxis_2nd.xml')


#d.getAllSpectrumName()
channels = ['K1:PEM-IXV_GND_TR120Q_X_OUT_DQ', # 0
            'K1:PEM-IXV_GND_TR120Q_Y_OUT_DQ', # 1
            'K1:PEM-IXV_GND_TR120Q_Z_OUT_DQ', # 2
            'K1:IOP-IX1_MADC1_TP_CH28', # 3
            ]
            #'K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ', # 4
            #'K1:PEM-IXV_GND_TR120QTEST_Y_OUT_DQ', # 5
            #'K1:PEM-IXV_GND_TR120QTEST_Z_OUT_DQ'] # 6

asd = []    
for ch in channels:
    asd += [d.getASD(ch,ref=False)]

# Z axis seismometer and Z axis Microphone
   
f, seis_z = asd[2] # um/sec/rtHz
_f, _seis_z = vel2vel(f,seis_z)
f, mic_z = asd[3] # count/rtHz
mic_z = mic_z*c2V # Pa/rtHz
f_mic_noise = np.logspace(1,3,1000)
mic_noise = np.ones(len(f_mic_noise))*mic_noise
mic_maximum = np.ones(len(f))*mic_maximum
f_,seis_noise = selfnoise(trillium='120QA',psd='ASD',unit='velo')
seis_noise = seis_noise*1e6 # um/sec/rtHz


f23,mag23,deg23 = d.getCoherence(channels[2],channels[3],ref=False)
idx = np.where(mag23>0.05)
cl = np.ones(len(f23))*0.05
f_exist = f23[idx]
coh_exist = mag23[idx]
mic_project = seis_z[idx]*coh_exist



fig, ax = plt.subplots(2,2,figsize=(15,8),sharex=True)
ax[0][0].loglog(_f, _seis_z,'k',label='Seismometer(TR-120QA)')
ax[0][0].loglog(f_, seis_noise,'k--',label='Self Noise')
ax[0][0].loglog(f_exist, mic_project,'ro',label='Project from Microphone',markersize=2)
ax[0][0].legend()
ax[0][0].set_ylabel('Ground Velocity \n[um/sec/rtHz]', fontsize=15)
ax[1][0].loglog(f, mic_z,'k',label='Microphone (ACO-7147A)')
ax[1][0].loglog(f_mic_noise, mic_noise,'k--',label='Self Noise')
ax[1][0].legend()
ax[1][0].set_ylabel('Sound Pressue \n[Pa/rtHz]', fontsize=15)
ax[1][0].set_xlabel('Frequency [Hz]', fontsize=15)
ax[0][1].semilogx(f23,mag23,'k')
ax[0][1].semilogx(f23,cl,'r--')
ax[0][1].set_ylabel('Coherence', fontsize=15)
ax[1][1].semilogx(f23,deg23,'k')
ax[1][1].set_ylim(-180,180)
ax[1][1].set_yticks(range(-180,181,90))
ax[1][1].set_ylabel('Phase [deg]', fontsize=15)
ax[1][1].set_xlabel('Frequency [Hz]', fontsize=15)
ax[0][0].set_xlim(1,200)
ax[1][0].set_xlim(1,200)
ax[1][0].set_xlim(1,200)
ax[1][1].set_xlim(1,200)
fig.savefig('ASD.png')
