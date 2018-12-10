import numpy as np
from dttpy.dttpy.dttdata import DttData
d = DttData('./181207/xarm_seis_x.xml')
#d = DttData('./181208/xarm_seis_x.xml')


ch1 = 'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ'
ch2 = 'K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ'
ch3 = 'K1:PEM-EXV_GND_TR120Q_X_OUT_DQ'

f1,asd1 = d.getASD(ch1,ref=False) # um/s/rtHz
f2,asd2 = d.getASD(ch2,ref=False) # um/s/rtHz
f3,asd3 = d.getASD(ch3,ref=False) # um/s/rtHz

f12,csd12,deg12 = d.getCSD(ch1,ch2,ref=False)
f13,csd13,deg13 = d.getCSD(ch1,ch3,ref=False)

f12,coh12,deg12 = d.getCoherence(ch1,ch2,ref=False)
f13,coh13,deg13 = d.getCoherence(ch1,ch3,ref=False)

from miyopy.utils.trillium import tf120QA,selfnoise
vel2v = 1202.5
vel2v_tf = tf120QA(f1)

noise = asd1/vel2v*vel2v_tf*(1.0-coh12)

asd1 = asd1*vel2v/vel2v_tf
asd2 = asd2*vel2v/vel2v_tf
asd3 = asd3*vel2v/vel2v_tf
noise = asd1*vel2v/vel2v_tf*(1.0-coh12)

f,selfnoise = selfnoise(trillium='120QA',psd='ASD',unit='velo')

# plot asd
import matplotlib.pyplot as plt
fig, ax0 = plt.subplots(1,1,figsize=(12, 6), dpi=80)
ax0.loglog(f,selfnoise*1e6,label='noise',linewidth=3,color='k')
ax0.loglog(f1,asd1,label='ch1')
ax0.loglog(f2,asd2,label='ch2')
ax0.loglog(f1,noise,label='noise')
ax0.legend(fontsize=10)
#ax0.set_ylim(1e-5,2)
ax0.set_xlim(4e-4,1e2)
ax0.set_ylabel('ASD [um/sec/rtHz]',fontsize=20)
ax0.set_xlabel('Frequency [Hz]',fontsize=20)
ax0.grid(b=True, which='major', color='gray', linestyle='-')
ax0.grid(b=True, which='minor', color='gray', linestyle=':')
plt.savefig('ASD_seis_noise.png')
plt.close()













#exit()

# plot tf
import matplotlib.pyplot as plt
fig, ax0 = plt.subplots(1,1,figsize=(12, 6), dpi=80)
ax0.loglog(f1,vel2v_tf,label='Trillium120QA')
ax0.legend(fontsize=10)
ax0.set_ylim(1e0,2e3)
ax0.set_xlim(4e-3,1e2)
ax0.set_ylabel('Cohnitude [V/m/sec]',fontsize=20)
ax0.set_xlabel('Frequency [Hz]',fontsize=20)
ax0.grid(b=True, which='major', color='gray', linestyle='-')
ax0.grid(b=True, which='minor', color='gray', linestyle=':')
plt.savefig('TransferFunction.png')
plt.close()


# plot asd
import matplotlib.pyplot as plt
fig, ax0 = plt.subplots(1,1,figsize=(12, 6), dpi=80)
ax0.loglog(f1,asd1,label='ch1')
ax0.loglog(f2,asd2,label='ch2')
ax0.loglog(f3,asd3,label='ch3')
ax0.legend(fontsize=10)
ax0.set_ylim(1e-5,2)
ax0.set_xlim(4e-3,1e2)
ax0.set_ylabel('ASD [um/sec/rtHz]',fontsize=20)
ax0.set_xlabel('Frequency [Hz]',fontsize=20)
ax0.grid(b=True, which='major', color='gray', linestyle='-')
ax0.grid(b=True, which='minor', color='gray', linestyle=':')
plt.savefig('ASD_seis.png')
plt.close()


# plot coherence
import matplotlib.pyplot as plt
fig, (ax0,ax1) = plt.subplots(2,1,figsize=(12, 6), dpi=80)
ax0.semilogx(f13,coh13,label='/'.join(['ch3','ch1']))
ax0.semilogx(f12,coh12,label='/'.join(['ch2','ch1']))
ax0.legend(fontsize=10)
ax0.grid(b=True, which='major', color='gray', linestyle='-')
ax0.grid(b=True, which='minor', color='gray', linestyle=':')
ax0.set_ylim(0,1)
ax0.set_ylabel('Coherence',fontsize=20)
ax0.set_xlim(4e-3,1e2)
ax1.semilogx(f13,deg13,label='/'.join(['ch3','ch1']))
ax1.semilogx(f12,deg12,label='/'.join(['ch2','ch1']))
ax1.grid(b=True, which='major', color='gray', linestyle='-')
ax1.grid(b=True, which='minor', color='gray', linestyle=':')
ax1.legend(fontsize=10)
ax1.set_ylim(-180,180)
ax1.set_xlim(4e-3,1e2)
ax1.set_yticks(range(-180,181,90))
ax1.set_ylabel('Phase [deg]',fontsize=20)
ax1.set_xlabel('Frequency [Hz]',fontsize=20)
plt.savefig('Coherence.png')
plt.close()
