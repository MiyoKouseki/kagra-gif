#
#! coding: utf-8
import os 
from scipy import signal
import numpy as np
from control import matlab
import matplotlib.pyplot as plt
import control

from gwpy.frequencyseries import FrequencySeries
from gwpy.timeseries import TimeSeries

from miyopy import seismodel
from susmodel import TypeA
from filt import servo,servo2,servo3,servo4
from lvdt import lvdt
from geophone import geo,geo_tf
from miyopy.utils.trillium import selfnoise as ntr120

# Utils
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
#gnd_vel = seismodel.kagra_seis('H',90)
start = 'Sep 03 2019 11:50:00 JST' # w/ SC 
end   = 'Sep 03 2019 12:20:00 JST' # w/ SC
#start = 'Sep 03 2019 12:45:00 JST' # w/o SC 
#end   = 'Sep 03 2019 13:15:00 JST' # w/o SC
gnd_vel = seismodel.kagra_seis_now(start,end,axis='X')
#gnd_vel.write('tmp.hdf5',format='hdf5')
tm_oplev = TimeSeries.fetch('K1:VIS-ETMX_TM_DAMP_L_IN1_DQ',start,end,host='10.68.10.121',port=8088)
tm_oplev = tm_oplev.asd(fftlength=2**8,overlap=2**7)
#tm_oplev.write('tmp_tmoplev.hdf5')
#tm_oplev = FrequencySeries.read('tmp_tmoplev.hdf5')
#gnd_vel = FrequencySeries.read('tmp.hdf5')
gnd_vel = FrequencySeries(gnd_vel.value,frequencies=gnd_vel.frequencies.value)
#gnd_vel.write('tmp.hdf5')
df = gnd_vel.df.value
gnd_vel = gnd_vel.crop(df,16+df)
#
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
prefix = os.getcwd() + '/SuspensionControlModel/script/typeA/'
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
H_gnd2tm_noctrl = noctrl.siso('accGndL','OpLev_TML')
#H_gnd2tm_noctrl = noctrl.siso('accGndL','dispIML')
#H_gnd2ip_noctrl = noctrl.siso('accGndL','GEO_IPL')
P_ip2ip_noctrl = noctrl.siso('noiseActIPL','LVDT_IPL')


# IPdcDamp Control Response
print ('Read TypeA response')
matfile = prefix + 'linmod/ipdcdamp.mat'
ipdcdamp = TypeA(matfile=matfile,actual=False)
H_gnderr2tm = ipdcdamp.siso('accGndL','OpLev_TML')
H_gndfb2tm = ipdcdamp.siso('dispGndL_err','OpLev_TML')
H_nlvdt2tm = ipdcdamp.siso('noiseLVDT_IPL','OpLev_TML')
sens = ipdcdamp.siso('noiseActIPL','actIPLmon') # 1/(1+G)
comp = ipdcdamp.siso('injIPL','pre_fbIPLmon') # G/(1+G)
matfile = prefix + 'linmod/ipdcdamp_oltf.mat'
ipdcdamp_oltf = TypeA(matfile=matfile,actual=False)
oltf = ipdcdamp_oltf.siso('injIPL','pre_fbIPLmon')

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
ax.set_title('OpLev TML Motion')
ax.loglog(tm_oplev,label='TM oplev',color='m',linewidth=2,alpha=1,zorder=10)
ax.loglog(gnd,label='Seismic Noise',color='black',linewidth=2,alpha=1,zorder=1)
ax.loglog(gnd.rms(),color='black',linestyle='dashdot',linewidth=2,zorder=1)
#ax.loglog((gnd*H_gnd2tm_noctrl).abs(),label='No Control',color='gray',linewidth=2)
#ax.loglog((gnd*H_gnd2tm_noctrl).abs().rms(),color='gray',linewidth=2,linestyle='--')
ax.loglog(total.abs(),label='Sum',color='r',linewidth=6,alpha=0.8,zorder=1)
ax.loglog(total.abs().rms(),color='r',linewidth=2,linestyle='dashdot',zorder=1)
ax.loglog((gnd*H_gnderr2tm).abs(),'--',label='Seismic Noise (Suspension Contrib.)',linewidth=2)
ax.loglog((gnd*H_gndfb2tm).abs(),'--',label='Seismic Noise (Sensor Contrib.)',linewidth=2)
#ax.loglog((nlvdt*H_nlvdt2tm).abs(),'--',label='Sensor Noise',linewidth=2)
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Displacement [um/rtHz or um]')
ax.set_ylim(1e-3,3e1)
ax.set_xlim(1e-2,2e0)
ax.legend(fontsize=15,loc='lower left')
plt.savefig('./etmx/img/OpLev_TML.png')
plt.close()




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
plt.savefig('./etmx/img/Noise.png')
plt.close()

# ---------------------------------------------
# Closed Loop
# ---------------------------------------------
print ('Plot CLTF, Gnd2TM')
from matplotlib.gridspec import GridSpec
fig = plt.figure(figsize=(8,8))
gs = GridSpec(2, 1, height_ratios=[3, 1])
ax2 = fig.add_subplot(gs[1])
ax = fig.add_subplot(gs[0],sharex=ax2)
#fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('Ground to OpLev TML')
#ax.hlines(y=1, xmin=1e-2, xmax=10, color='k',linewidth=2,linestyle=':')
ax.loglog(H_gnd2tm_noctrl.abs(),label='No Control',color='k',linewidth=2,linestyle='-')
ax.loglog((H_gndfb2tm+H_gnderr2tm).abs(),label='Total',color='r',linewidth=6)
ax.loglog(H_gnderr2tm.abs(),label='Ps/(1+G) (Suspension Contrib.)',color='b',linewidth=2,linestyle='--')
ax.loglog(H_gndfb2tm.abs(),label='G/(1+G) (Sensor Contrib.)',color='g',linewidth=2,linestyle='--')
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-3,3e1)
#ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=15,loc='lower left')
ax2.semilogx(H_gnd2tm_noctrl.angle().rad2deg(),label='No Control',color='k',linewidth=2,linestyle='-')
ax2.semilogx((H_gndfb2tm+H_gnderr2tm).angle().rad2deg(),label='Total',color='r',linewidth=6)
ax2.semilogx(H_gnderr2tm.angle().rad2deg(),label='ErrorPoint (for FF)',color='b',linewidth=2,linestyle='--')
ax2.semilogx(H_gndfb2tm.angle().rad2deg(),label='FeedBackPoint (for SC)',color='g',linewidth=2,linestyle='--')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
#ax2.set_xlim(1e-4,1e2)
ax2.set_xlim(1e-2,2e0)
plt.savefig('./etmx/img/CLTF.png')
plt.close()
# ---------------------------------------------
# print ('Plot CLTF, Gnd2IP')
# H_gnderr2ip = ipdcdamp.siso('accGndL','GEO_IPL')
# H_gndfb2ip = ipdcdamp.siso('dispGndL_err','GEO_IPL')
# H_gndfb2ip = tf(H_gndfb2ip,omega)/(1j*omega)
# H_gnderr2ip = tf(H_gnderr2ip,omega)
# fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
# ax.set_title('Ground to IPL')
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
_omega = 2.0*np.pi*np.logspace(-4,3,1001)
servo = tf(servo,_omega)
oltf = tf(oltf,_omega)
P_ip2ip_noctrl = tf(P_ip2ip_noctrl,_omega)
# ---------------------------------------------
print ('Plot OLTF')
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('OLTF')
#ax.hlines(y=1e0, xmin=1e-4, xmax=1e2, color='k',linewidth=2,linestyle=':')
ax.loglog(oltf.abs(),label='OLTF',color='r',linewidth=2,linestyle='-')
ax.loglog(servo.abs(),label='Servo',color='b',linewidth=2,linestyle='-')
ax.loglog(P_ip2ip_noctrl.abs()*2e2,label='Pa (Normalized)',color='k',linewidth=2,linestyle='--')
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-2,2e2)
ax.legend(fontsize=15,loc='upper left')
#ax2.hlines(y=90, xmin=1e-4, xmax=1e2, color='k',linewidth=2,linestyle=':')
#ax2.hlines(y=-150, xmin=1e-4, xmax=1e2, color='k',linewidth=2,linestyle=':')
ax2.semilogx(oltf.angle().rad2deg(),label='OLTF',color='r',linewidth=2,linestyle='-')
ax2.semilogx(servo.angle().rad2deg(),label='Servo',color='b',linewidth=2,linestyle='-')
ax2.semilogx(P_ip2ip_noctrl.angle().rad2deg(),label='Pa',color='k',linewidth=2,linestyle='--')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlim(1e-4,1e2)
plt.savefig('./etmx/img/OLTF.png')
plt.close()
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
plt.savefig('./etmx/img/SensitivityFunction.png')
plt.close()

print('Done')
