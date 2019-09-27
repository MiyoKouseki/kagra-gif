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
from vismodel.lvdt import lvdt
from vismodel.geophone import geo,geo_tf
from miyopy.utils.trillium import selfnoise as ntr120

# Utils
from control import matlab
def tf(sys,omega):
    print ('calc sys.freqresp')
    mag, phase, omega = control.matlab.bode(sys,omega,Plot=False)
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
df = gnd.df.value


# Sensor Noise
nlvdt = lvdt.interpolate(df).crop(df,16+df)
f,ntr120 = ntr120(trillium='120QA',psd='ASD',unit='disp')
ntr120 = FrequencySeries(ntr120,frequencies=f)*1e6
#_omega = geo.frequencies.value*(2.0*np.pi)
#tf_geo = tf(geo_tf,_omega)
#ngeo = (geo/(tf_geo*(1j*_omega))).abs()

# Servo
prefix = os.getcwd() + '/vismodel/SuspensionControlModel/script/typeA/'
matfile = prefix + 'servo/servoBFL.mat'
import scipy
from scipy.signal import zpk2tf
mat_dict = scipy.io.loadmat(matfile,struct_as_record=False)
servoBFL = mat_dict['servoBFL_st'][0][0]
z = servoBFL.Z[0][0][:,0]
p = servoBFL.P[0][0][:,0]
k = servoBFL.K[0][0]
servo = matlab.tf(*zpk2tf(z,p,k))


# No Control Response
print ('Read TypeA response')
matfile = prefix + 'linmod/noctrl.mat'
noctrl = TypeA(matfile=matfile,actual=False)
H_gnd2tm_noctrl = noctrl.siso('accGndL','dispTML')
P_bf2bf_noctrl = noctrl.siso('noiseActBFL','LVDT_BFL')



# Ipdcbfdamp Control Response
print ('Read TypeA response')
matfile = prefix + 'linmod/ipdcbfdamp.mat'
ipdcbfdamp = TypeA(matfile=matfile,actual=False)
H_gnderr2tm = ipdcbfdamp.siso('accGndL','dispTML')
H_gndfb2tm = ipdcbfdamp.siso('dispGndL_err','dispTML')
H_nlvdt2tm = ipdcbfdamp.siso('noiseLVDT_BFL','dispTML')
sens = ipdcbfdamp.siso('noiseActBFL','actBFLmon') # 1/(1+G)
comp = ipdcbfdamp.siso('injBFL','pre_fbBFLmon') # G/(1+G)
matfile = prefix + 'linmod/ipdcbfdamp_oltf.mat'
ipdcbfdamp_oltf = TypeA(matfile=matfile,actual=False)
oltf = ipdcbfdamp_oltf.siso('injBFL','pre_fbBFLmon')
# ----
# zeta = 0.4 #0.2
# theta = np.arctan(np.sqrt(1-zeta**2)/zeta)
# tan = np.sqrt(1-zeta**2)/zeta
# Tn = 60 #sec
# bw = 3*Tn/zeta
# print np.rad2deg(theta),bw
# plt.figure(figsize=(7,7))
# poles,zeros = control.pzmap(H_gnd2tm_noctrl,Plot=False,grid=False)
# #poles,zeros = control.pzmap(H_gnderr2tm+H_gndfb2tm,Plot=False,grid=False)
# #plt.plot(poles.real,poles.imag,'o',label='Pole')
# #plt.plot(zeros.real,zeros.imag,'x',label='Zero')
# plt.loglog(np.abs(poles.real),np.abs(poles.imag),'o',label='Pole')
# plt.loglog(np.abs(zeros.real),np.abs(zeros.imag),'x',label='Zero')
# re = np.logspace(-3,3,1000)
# plt.loglog(re,re*tan,'k')
# plt.vlines(3.0/Tn,1e-3,1e3,'k')
# plt.xlim(1e-5,1e3)
# plt.ylim(1e-5,1e3)
# plt.xlabel('Re')
# plt.ylabel('Im')
# plt.legend(fontsize=20)
# plt.savefig('hoge.png')
# plt.close()
# exit()
# ----

# ---------------------------------------------
# Frequency Response
# ---------------------------------------------
print ('Calc Freq. Response')
H_gnd2tm_noctrl = tf(H_gnd2tm_noctrl,omega)*(1j*omega)**2
H_gnderr2tm = tf(H_gnderr2tm,omega)*(1j*omega)**2
H_gndfb2tm = tf(H_gndfb2tm,omega)
#H_gnd2ip_noctrl = tf(H_gnd2ip_noctrl,omega)*(1j*omega)**1
H_nlvdt2tm = tf(H_nlvdt2tm,omega)
sens = tf(sens,omega)
comp = tf(comp,omega)



# ---------------------------------------------
# Displacement of TM
# ---------------------------------------------
print ('Plot Disp')
total = np.sqrt( \
        (gnd*(H_gnderr2tm + H_gndfb2tm))**2 \
      + (nlvdt*(H_nlvdt2tm))**2
        )
fig,ax = plt.subplots(1,1,figsize=(8,8))
ax.set_title('TML Motion')
ax.loglog(gnd,label='Ground',color='black',linewidth=2,alpha=1,zorder=1)
ax.loglog(gnd.rms(),color='black',linestyle='dashdot',linewidth=2,zorder=1)
ax.loglog((gnd*H_gnd2tm_noctrl).abs(),label='No Control',color='gray',linewidth=2)
ax.loglog((gnd*H_gnd2tm_noctrl).abs().rms(),color='gray',linewidth=2,linestyle='--')
ax.loglog(total.abs(),label='Sum',color='r',linewidth=6,alpha=0.8,zorder=1)
ax.loglog(total.abs().rms(),color='r',linewidth=2,linestyle='dashdot',zorder=1)
ax.loglog((gnd*H_gnderr2tm).abs(),'--',label='Seismic Noise from Suspension',linewidth=2)
ax.loglog((gnd*H_gndfb2tm).abs(),'--',label='Seismic Noise from LVDT',linewidth=2)
ax.loglog((nlvdt*H_nlvdt2tm).abs(),'--',label='Sensor Noise',linewidth=2)
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Displacement [um/rtHz or um]')
ax.set_ylim(1e-5,1e1)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=15,loc='lower left')
plt.savefig('TML.png')
# ---------------------------------------------
print ('Plot Noise')
fig,ax = plt.subplots(1,1,figsize=(8,8))
ax.set_title('Noise')
ax.loglog(gnd,label='Ground',color='black',linewidth=2,alpha=1,zorder=1)
#ax.loglog(ngeo,'--',label='Geophone Noise',linewidth=2)
ax.loglog(ntr120,'--',label='Seismometer Noise',linewidth=2)
ax.loglog(nlvdt,'--',label='LVDT Noise',linewidth=2)
#ax.loglog(nlvdt,'--',label='Corrected LVDT Noise',linewidth=2)
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Displacement [um/rtHz or um]')
ax.set_ylim(1e-6,1e1)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=15,loc='lower left')
plt.savefig('Noise.png')


# ---------------------------------------------
# Closed Loop
# ---------------------------------------------
print ('Plot CLTF, Gnd2TM')
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('Ground to TML')
ax.hlines(y=1e0, xmin=1e-4, xmax=1e1, color='k',linewidth=2,linestyle=':')
ax.loglog(H_gnd2tm_noctrl.abs(),label='No Control',color='k',linewidth=2,linestyle='-')
ax.loglog((H_gndfb2tm+H_gnderr2tm).abs(),label='Total',color='r',linewidth=6)
ax.loglog(H_gnderr2tm.abs(),label='Ps/(1+G) (from Suspension)',color='b',linewidth=2,linestyle='--')
ax.loglog(H_gndfb2tm.abs(),label='G/(1+G) (from LVDT)',color='g',linewidth=2,linestyle='--')
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-5,1e1)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=15,loc='lower left')
ax2.semilogx(H_gnd2tm_noctrl.angle().rad2deg(),label='No Control',color='k',linewidth=2,linestyle='-')
ax2.semilogx((H_gndfb2tm+H_gnderr2tm).angle().rad2deg(),label='Total',color='r',linewidth=6)
ax2.semilogx(H_gnderr2tm.angle().rad2deg(),label='ErrorPoint (for FF)',color='b',linewidth=2,linestyle='--')
ax2.semilogx(H_gndfb2tm.angle().rad2deg(),label='FeedBackPoint (for SC)',color='g',linewidth=2,linestyle='--')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlim(1e-2,1e1)
plt.savefig('CLTF.png')
# ---------------------------------------------
# print ('Plot CLTF, Gnd2IP')
# H_gnderr2ip = ipdcbfdamp.siso('accGndL','GEO_BFL')
# H_gndfb2ip = ipdcbfdamp.siso('dispGndL_err','GEO_BFL')
# H_gndfb2ip = tf(H_gndfb2ip,omega)/(1j*omega)
# H_gnderr2ip = tf(H_gnderr2ip,omega)
# fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
# ax.set_title('Ground to BFL')
# ax.loglog(H_gnd2ip_noctrl.abs(),label='No Control',color='k',linewidth=2,linestyle='--')
# ax.loglog((H_gndfb2ip+H_gnderr2ip).abs(),label='Total',color='r',linewidth=2)
# ax.loglog(H_gnderr2ip.abs(),label='ErrorPoint',color='b',linewidth=2,linestyle='--')
# ax.loglog(H_gndfb2ip.abs(),label='FeedBack',color='g',linewidth=2,linestyle='--')
# ax.set_ylabel('Magnitude')
# ax.set_ylim(1e-4,1e1)
# ax.set_xlim(1e-2,1e1)
# ax.legend(fontsize=20,loc='lower left')
# ax2.semilogx(H_gnd2ip_noctrl.angle().rad2deg(),label='No Control',color='k',linewidth=2,linestyle='--')
# ax2.semilogx((H_gndfb2ip+H_gnderr2ip).angle().rad2deg(),label='Total',color='r',linewidth=2)
# ax2.semilogx(H_gnderr2ip.angle().rad2deg(),label='ErrorPoint',color='b',linewidth=2,linestyle='--')
# ax2.semilogx(H_gndfb2ip.angle().rad2deg(),label='FeedBack',color='g',linewidth=2,linestyle='--')
# ax2.set_ylabel('Phase [Deg.]')
# ax2.set_ylim(-180,180)
# ax2.set_xlim(1e-2,1e1)
# plt.savefig('CLTF_Gnd2IP.png')



# ---------------------------------------------
# Servo
# ---------------------------------------------
_omega = 2.0*np.pi*np.logspace(-4,3,2002)
servo = tf(servo,_omega)
print ('Plot Servo')
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('Servo Filter')
ax.loglog(servo.abs(),label='IP Damp',color='r',linewidth=2,linestyle='-')
ax.set_ylabel('Magnitude')
#ax.set_ylim(1e-0,1e3)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=20,loc='lower left')
ax2.semilogx(servo.angle().rad2deg(),label='IP Damp',color='r',linewidth=2,linestyle='-')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlim(1e-2,1e1)
plt.savefig('Servo.png')


# ---------------------------------------------
# Open Loop
# ---------------------------------------------
oltf = tf(oltf,_omega)
P_bf2bf_noctrl = tf(P_bf2bf_noctrl,_omega)
print ('Plot OLTF')
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('OLTF')
ax.hlines(y=1e0, xmin=1e-4, xmax=1e3, color='k',linewidth=2,linestyle=':')
ax.loglog(oltf.abs(),label='OLTF',color='r',linewidth=2,linestyle='-')
ax.loglog(servo.abs(),label='Servo',color='b',linewidth=2,linestyle='-')
ax.loglog(P_bf2bf_noctrl.abs(),label='Pa',color='k',linewidth=2,linestyle='--')
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-6,1e3)
ax.legend(fontsize=20,loc='lower left')
ax2.hlines(y=-90, xmin=1e-4, xmax=1e3, color='k',linewidth=2,linestyle=':')
ax2.hlines(y=-150, xmin=1e-4, xmax=1e3, color='k',linewidth=2,linestyle=':')
ax2.semilogx(oltf.angle().rad2deg(),label='OLTF',color='r',linewidth=2,linestyle='-')
ax2.semilogx(servo.angle().rad2deg(),label='Servo',color='b',linewidth=2,linestyle='-')
ax2.semilogx(P_bf2bf_noctrl.angle().rad2deg(),label='Pa',color='k',linewidth=2,linestyle='--')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlim(1e-3,1e1)
plt.savefig('OLTF.png')
# ---------------------------------------------
print ('Plot SensitivityFunction')
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('Closed Loop')
ax.loglog((sens+comp).abs(),label='Sum',color='k',linewidth=2,linestyle='--')
ax.loglog(sens.abs(),label='1/(1+G) : Sensitivity Function',color='r',linewidth=2,linestyle='-')
ax.loglog(comp.abs(),label='G/(1+G) : Complimentary Function',color='b',linewidth=2,linestyle='-')
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-2,1e2)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=15,loc='upper left')
ax2.semilogx((sens+comp).angle().rad2deg(),label='Sum',color='k',linewidth=2,linestyle='--')
ax2.semilogx(sens.angle().rad2deg(),label='Sens',color='r',linewidth=2,linestyle='-')
ax2.semilogx(comp.angle().rad2deg(),label='Comp',color='b',linewidth=2,linestyle='-')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_xlim(1e-2,1e1)
plt.savefig('SensitivityFunction.png')


print('Done')
