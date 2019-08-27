#
#! coding: utf-8
import os 
from scipy import signal
import numpy as np
from control import matlab
import matplotlib.pyplot as plt
import control

from gwpy.frequencyseries import FrequencySeries

import seismodel
from vismodel import TypeA
from vismodel.filt import servo,servo2,servo3,servo4

# Utils
def tf(sys,omega):
    print ('calc sys.freqresp')
    #sus = control.ss2tf(sys)
    #mag, phase, omega = sys.freqresp(omega)
    mag, phase, omega = control.matlab.bode(sys,omega)
    mag = np.squeeze(mag)
    phase = np.squeeze(phase)
    G = mag*np.exp(1j*phase)
    freq = omega/(2.0*np.pi)
    print('calc sys.freqresp. Convert FreqSeries')
    hoge = FrequencySeries(G,frequencies=freq)
    return hoge


# Seismic Noise
gnd_vel = seismodel.kagra_seis('H',90)
freq = gnd_vel.frequencies.value
omega = 2.0*np.pi*freq
gnd  = gnd_vel/(2.0*np.pi*freq)

# Read Servo
prefix = os.getcwd() + '/vismodel/SuspensionControlModel/script/typeA/'
matfile = prefix + 'servo/servoIPL.mat'
import scipy
from scipy.signal import zpk2tf
mat_dict = scipy.io.loadmat(matfile,struct_as_record=False)
servoIPL = mat_dict['servoIPL_st'][0][0]
z = servoIPL.Z[0][0][:,0]
p = servoIPL.P[0][0][:,0]
k = servoIPL.K[0][0]
servo = matlab.tf(*zpk2tf(z,p,k))


# No Control Response
print ('Read TypeA response')
matfile = prefix + 'linmod/noctrl.mat'
noctrl = TypeA(matfile=matfile,actual=False)
H_gnd2tm_noctrl = noctrl.siso('controlmodel/accGndL','controlmodel/dispTML')
H_gnd2ip_noctrl = noctrl.siso('controlmodel/accGndL','controlmodel/GEO_IPL')
P_ip2ip_noctrl = noctrl.siso('controlmodel/noiseActIPL','controlmodel/LVDT_IPL')


# IPdcDamp Control Response
print ('Read TypeA response')
matfile = prefix + 'linmod/ipdcdamp.mat'
ipdcdamp = TypeA(matfile=matfile,actual=False)
H_gnd2tm_ipdcdamp = ipdcdamp.siso('controlmodel/accGndL','controlmodel/dispTML')
H_gnd2ip_ipdcdamp = ipdcdamp.siso('controlmodel/accGndL','controlmodel/GEO_IPL')
matfile = prefix + 'linmod/ipdcdamp_oltf.mat'
ipdcdamp_oltf = TypeA(matfile=matfile,actual=False)
oltf = ipdcdamp_oltf.siso('controlmodel/injIPL','controlmodel/pre_fbIPLmon')



# ---------------------------------------------
# FreqResp
print ('Calc Freq. Response')
H_gnd2tm_noctrl = tf(H_gnd2tm_noctrl,omega)*(1j*omega)**2
H_gnd2tm_ipdcdamp = tf(H_gnd2tm_ipdcdamp,omega)*(1j*omega)**2
H_gnd2ip_noctrl = tf(H_gnd2ip_noctrl,omega)*(1j*omega)**1
H_gnd2ip_ipdcdamp = tf(H_gnd2ip_ipdcdamp,omega)*(1j*omega)**1
servo = tf(servo,omega)
oltf = tf(oltf,omega)
P_ip2ip_noctrl = tf(P_ip2ip_noctrl,omega)


# ---------------------------------------------
print ('Plot Disp')
fig,ax = plt.subplots(1,1,figsize=(8,8))
ax.set_title('TML Motion')
ax.loglog(gnd,label='Ground',color='gray',linewidth=3)
ax.loglog(gnd.rms(),color='gray',linestyle='--',linewidth=3)
ax.loglog(gnd*H_gnd2tm_noctrl.abs(),label='No Control',color='k',linewidth=3)
ax.loglog((gnd*H_gnd2tm_noctrl.abs()).rms(),color='k',linestyle='--',linewidth=3)
ax.loglog(gnd*H_gnd2tm_ipdcdamp.abs(),label='DCdamp on IP',color='r',linewidth=3)
ax.loglog((gnd*H_gnd2tm_ipdcdamp.abs()).rms(),color='r',linestyle='--',linewidth=3)
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Displacement [um/rtHz or um]')
ax.set_ylim(1e-3,1e1)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=20,loc='lower left')
plt.savefig('TML.png')


print ('Plot CLTF')
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('TFs from Ground to TML')
ax.loglog(H_gnd2tm_noctrl.abs(),label='No Control',color='k',linewidth=3,linestyle='--')
ax.loglog(H_gnd2tm_ipdcdamp.abs(),label='DCdamp on IP',color='r',linewidth=3)
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-4,1e1)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=20,loc='lower left')
ax2.semilogx(H_gnd2tm_noctrl.angle().rad2deg(),label='No Control',color='k',linewidth=3,linestyle='--')
ax2.semilogx(H_gnd2tm_ipdcdamp.angle().rad2deg(),label='DCdamp on IP',color='r',linewidth=3)
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_xlim(1e-2,1e1)
plt.savefig('CLTF.png')

print ('Plot CLTF, Gnd2IP')
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('TFs from Ground to IPL')
ax.loglog(H_gnd2ip_noctrl.abs(),label='No Control',color='k',linewidth=3,linestyle='--')
ax.loglog(H_gnd2ip_ipdcdamp.abs(),label='DCdamp on IP',color='r',linewidth=3)
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-4,1e1)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=20,loc='lower left')
ax2.semilogx(H_gnd2ip_noctrl.angle().rad2deg(),label='No Control',color='k',linewidth=3,linestyle='--')
ax2.semilogx(H_gnd2ip_ipdcdamp.angle().rad2deg(),label='DCdamp on IP',color='r',linewidth=3)
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_xlim(1e-2,1e1)
plt.savefig('CLTF_Gnd2IP.png')


print ('Plot CLTF')
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('TFs from Ground to TML')
ax.loglog(H_gnd2tm_noctrl.abs(),label='No Control',color='k',linewidth=3,linestyle='--')
ax.loglog(H_gnd2tm_ipdcdamp.abs(),label='DCdamp on IP',color='r',linewidth=3)
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-4,1e1)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=20,loc='lower left')
ax2.semilogx(H_gnd2tm_noctrl.angle().rad2deg(),label='No Control',color='k',linewidth=3,linestyle='--')
ax2.semilogx(H_gnd2tm_ipdcdamp.angle().rad2deg(),label='DCdamp on IP',color='r',linewidth=3)
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlim(1e-2,1e1)
plt.savefig('CLTF.png')

print ('Plot Servo')
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('Servo Filter')
ax.loglog(servo.abs(),label='IP Damp',color='r',linewidth=3,linestyle='-')
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-0,1e3)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=20,loc='lower left')
ax2.semilogx(servo.angle().rad2deg(),label='IP Damp',color='r',linewidth=3,linestyle='-')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlim(1e-2,1e1)
plt.savefig('Servo.png')


print ('Plot OLTF')
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('OLTF')
ax.loglog(oltf.abs(),label='OLTF',color='r',linewidth=3,linestyle='-')
ax.loglog(servo.abs(),label='Servo',color='b',linewidth=3,linestyle='-')
ax.loglog(P_ip2ip_noctrl.abs(),label='Pa',color='k',linewidth=3,linestyle='--')
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-4,1e2)
ax.legend(fontsize=20,loc='lower left')
ax2.semilogx(oltf.angle().rad2deg(),label='OLTF',color='r',linewidth=3,linestyle='-')
ax2.semilogx(servo.angle().rad2deg(),label='Servo',color='b',linewidth=3,linestyle='-')
ax2.semilogx(P_ip2ip_noctrl.angle().rad2deg(),label='Pa',color='k',linewidth=3,linestyle='--')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlim(1e-3,1e1)
plt.savefig('OLTF.png')


print('Done')
