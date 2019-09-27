#
#! coding: utf-8
import os
import numpy as np
from scipy.io import loadmat
from scipy.signal import zpk2tf
import matplotlib.pyplot as plt

from control import matlab

from gwpy.frequencyseries import FrequencySeries
from gwpy.timeseries import TimeSeries

from miyopy import seismodel
from miyopy.utils.trillium import selfnoise as ntr120
from miyopy.utils.lvdt import noise as nlvdt
from miyopy.utils.susmodel import TypeA
from miyopy.utils.pycontrol import tf


nominal     = True
use_oplev   = False
use_arm     = True
plot_req    = False
plot_noctrl = False
sc = False

# Actual oltf
prefix = './etmx/190903/'
fname_mag = 'oltf.0'
fname_pha = 'oltf.1'
_freq,mag = np.loadtxt(prefix+fname_mag,unpack=True)
_freq,pha = np.loadtxt(prefix+fname_pha,unpack=True)
oltf0 = FrequencySeries(mag*np.exp(1j*np.deg2rad(pha)),frequencies=_freq)



# ------------------------------------------------------------
# IFO Requirement
# ------------------------------------------------------------
prefix = '../requirement/JGW-T1809214-v1/BRSE/'
fname_brse = 'DisplacementNoiseRequirement.dat'
_freq, _,ETMX_brse,_,_,_,_,_,_ = np.loadtxt(prefix+fname_brse,dtype=np.float32,
                                       delimiter=',',unpack=True)
req_brse = ETMX_brse*1e6
req_brse = FrequencySeries(req_brse,frequencies=_freq)
prefix = '../requirement/JGW-T1809214-v1/DRSE/'
fname_drse = 'DisplacementNoiseRequirement.dat'
_freq, _,ETMX_drse,_,_,_,_,_,_ = np.loadtxt(prefix+fname_drse,dtype=np.float32,
                                       delimiter=',',unpack=True)
req_drse = ETMX_drse*1e6
req_drse = FrequencySeries(req_drse,frequencies=_freq)

print req_brse.f0, req_brse.df,req_brse.frequencies.value[-1]
req_brse = req_brse.crop(1.0,20.0)
print req_brse.f0, req_brse.df,req_brse.frequencies.value[-1]

# ------------------------------------------------------------
# Seismic Noise
# ------------------------------------------------------------
if nominal:    
    gnd_vel = seismodel.kagra_seis('H',99)
    tm_oplev = None
    freq = gnd_vel.frequencies.value
    omega = 2.0*np.pi*freq
    gnd  = gnd_vel/(2.0*np.pi*freq)
    df = gnd.df.value    
else:    
    start = 'Sep 03 2019 11:50:00 JST' # w/ SC 
    end   = 'Sep 03 2019 12:20:00 JST' # w/ SC
    start = 'Sep 03 2019 12:45:00 JST' # w/o SC 
    end   = 'Sep 03 2019 13:15:00 JST' # w/o SC
    start = 'Sep 04 2019 06:00:00 JST' # w/o SC 
    end   = 'Sep 04 2019 07:30:00 JST' # w/o SC
    if sc: # SC
        start = 'Sep 17 2019 05:39:00 JST' # 
        end   = 'Sep 17 2019 05:49:00 JST' #
    else: # No SC
        start = 'Sep 17 2019 05:26:00 JST' # 
        end   = 'Sep 17 2019 05:36:00 JST' #        
    gnd_vel = seismodel.kagra_seis_now(start,end,axis='L',fftlen=2**6,ovlp=2**5)
    gnd_vel = FrequencySeries(gnd_vel.value,frequencies=gnd_vel.frequencies.value)#*1.4
    #gnd_vel.name='gnd_vel'
    #gnd_vel.write('gnd_vel_without_SC.hdf5')
    df = gnd_vel.df.value
    gnd_vel = gnd_vel.crop(df,16+df)
    freq = gnd_vel.frequencies.value
    omega = 2.0*np.pi*freq
    gnd  = gnd_vel#/(2.0*np.pi*freq)
    df = gnd.df.value    
    # OpLev Signal (as the out of loop sensor)
    kwargs = {'host':'10.68.10.121','port':8088}
    data = TimeSeries.fetch('K1:VIS-ETMX_TM_DAMP_L_IN1_DQ',start,end,**kwargs)
    tm_oplev = data.asd(fftlength=2**6,overlap=2**5)
    #tm_oplev.name = 'aom'
    #tm_oplev.write('aom_with_SC.hdf5')
    c = 299792458 # m/sec
    lam = 1064e-9 # m 
    tm_oplev = tm_oplev*3000.0/(c/lam)*1e6
    if use_arm:
        data = TimeSeries.fetch('K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16',start,end,**kwargs)
        xarm = data.asd(fftlength=2**6,overlap=2**5)
        #xarm.name = 'aom'
        #xarm.write('aom_with_SC.hdf5')
        c = 299792458 # m/sec
        lam = 1064e-9 # m 
        xarm = xarm*3000.0/(c/lam)*1e6
        
    #print data
# ------------------------------------------------------------    
# Feedback Sensor Noise
# ------------------------------------------------------------
# LVDT
nlvdt = nlvdt.interpolate(df).crop(df,16+df)

# Seismometer
nseis = ntr120(trillium='120QA',psd='ASD',unit='disp')*1e6

# ------------------------------------------------------------
# Servo Filter
# ------------------------------------------------------------
# Read servo filter from .mat file. 
prefix = os.getcwd() + '/SuspensionControlModel/script/typeA/'
matfile = prefix + 'servo/servoIPL.mat'
#print matfile
mat_dict = loadmat(matfile,struct_as_record=False)
servoIPL = mat_dict['servoIPL_st'][0][0]
z = servoIPL.Z[0][0][:,0]
p = servoIPL.P[0][0][:,0]
k = servoIPL.K[0][0]
servo = matlab.tf(*zpk2tf(z,p,k))


# ------------------------------------------------------------
# Suspension Response
# ------------------------------------------------------------
# No Control Response
if use_oplev:
    ofl_sensor = 'OpLev_TML'    
else:
    ofl_sensor = 'dispTML'
if not use_oplev and use_arm:
    ofl_sensor = 'dispTML'    
    
print ('Read No Control Response')
matfile = prefix + 'linmod/noctrl.mat'
noctrl = TypeA(matfile=matfile,actual=False)
H_gnd2tm_noctrl = noctrl.siso('accGndL',ofl_sensor)
P_ip2ip_noctrl = noctrl.siso('noiseActIPL','LVDT_IPL')
# IP Controled Response
print ('Read IP Controled Response')
matfile = prefix + 'linmod/ipdcdamp.mat'
ipdcdamp = TypeA(matfile=matfile,actual=False)
H_gndsus2tm = ipdcdamp.siso('accGndL',ofl_sensor) # 1. Suspension Contrib.
H_gndsens2tm = ipdcdamp.siso('dispGndL_err',ofl_sensor) # 2. Sensor Contrib.
H_nlvdt2tm = ipdcdamp.siso('noiseLVDT_IPL',ofl_sensor) # (Must Same as 2.)
# OLTF when IP controled
matfile = prefix + 'linmod/ipdcdamp_oltf.mat'
ipdcdamp_oltf = TypeA(matfile=matfile,actual=False)
oltf = ipdcdamp_oltf.siso('injIPL','pre_fbIPLmon')

# ------------------------------------------------------------
#
#                          Plot 
# 
# ------------------------------------------------------------
if use_oplev:
    sensor_name = 'TML Oplev'
else:
    sensor_name = 'TML'
if not use_oplev and use_arm:
    sensor_name = 'ARM'
    
# Frequency Response
# ------------------------------------------------------------
print('calc transferfunction')
H_gnd2tm_noctrl = tf(H_gnd2tm_noctrl,omega)*(1j*omega)**2
#H_gnd2tm_noctrl.name = 'gnd2tm_noctrl'
#H_gnd2tm_noctrl.write('./noctrl.hdf5')
#exit()
ff_factor = 1.
if sc:
    #sc_factor = 1./5
    sc_factor = 1./10
else:
    sc_factor = 1.
H_gndsus2tm = tf(H_gndsus2tm,omega)*(1j*omega)**2*ff_factor
H_gndsens2tm = tf(H_gndsens2tm,omega)*sc_factor
H_nlvdt2tm = tf(H_nlvdt2tm,omega)


# ------------------------------------------------------------
# Noisebudget of TM motion
# ------------------------------------------------------------
print ('Plot Noisebudget of TM motion')
total = np.sqrt( \
        (gnd*(H_gndsus2tm + H_gndsens2tm))**2 \
        )
fig,ax = plt.subplots(1,1,figsize=(8,8))
ax.set_title('ETMX {0} Motion'.format(sensor_name))
ax.loglog(gnd,label='Seismic Noise',color='black',linewidth=2,alpha=1,zorder=1)
#ax.loglog(gnd.rms(),color='black',linestyle='dashdot',linewidth=2,zorder=1)
total.name='total'
if sc:
    pass
    #total.abs().write('total_wsc.hdf5')
else:
    pass
    #total.abs().write('total_wosc.hdf5')    
ax.loglog(total.abs(),label='Sum',color='r',linewidth=3,alpha=0.8,zorder=1)
ax.loglog(total.abs().rms(),color='r',linewidth=2,linestyle='dashdot',zorder=1)
ax.loglog((gnd*H_gndsus2tm).abs(),'--',label='Seismic Noise (Suspension Contrib.)',linewidth=2)
ax.loglog((gnd*H_gndsens2tm).abs(),'--',label='Seismic Noise (Sensor Contrib.)',linewidth=2)
#ax.loglog((nlvdt*H_nlvdt2tm).abs(),'--',label='Sensor Noise',linewidth=2)
if use_oplev:
    ax.loglog(tm_oplev,label='TM oplev',color='m',linewidth=3,zorder=1)
if use_arm and not nominal:
    ax.loglog(xarm,label='xarm',color='m',linewidth=3,zorder=1)    
if plot_noctrl:
    ax.loglog((gnd*H_gnd2tm_noctrl).abs(),label='No Control',color='gray',linewidth=2)
    ax.loglog((gnd*H_gnd2tm_noctrl).abs().rms(),color='gray',linewidth=2,linestyle='--')
if plot_req:
    ax.loglog(req_brse,label='BRSE Requirement',linewidth=2,alpha=1,zorder=1)
    ax.loglog(req_drse,label='DRSE Requirement',linewidth=2,alpha=1,zorder=1)
    ax.set_ylim(1e-24,3e1)
    ax.set_xlim(5e-3,5e1)    
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Displacement [um/rtHz or um]')
ax.set_ylim(1e-5,2e1)
ax.set_xlim(4e-2,1e1)
ax.legend(fontsize=15,loc='lower left')
plt.savefig('./etmx/img/TML.png')
plt.close()


# ------------------------------------------------------------
# Closed Loop
# ------------------------------------------------------------
print ('Plot CLTF, Gnd2TM')
from matplotlib.gridspec import GridSpec
fig = plt.figure(figsize=(8,8))
gs = GridSpec(2, 1, height_ratios=[3, 1])
ax2 = fig.add_subplot(gs[1])
ax = fig.add_subplot(gs[0],sharex=ax2)
ax.set_title('Ground to {0}'.format(sensor_name))
ax.loglog(H_gnd2tm_noctrl.abs(),label='No Control',color='k',linewidth=2,linestyle='-')
ax.loglog((H_gndsens2tm+H_gndsus2tm).abs(),label='Total',color='r',linewidth=6)
ax.loglog(H_gndsus2tm.abs(),label='Ps/(1+G) (Suspension Contrib.)',color='b',linewidth=2,linestyle='--')
ax.loglog(H_gndsens2tm.abs(),label='G/(1+G) (Sensor Contrib.)',color='g',linewidth=2,linestyle='--')
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-3,3e1)
ax.legend(fontsize=15,loc='lower left')
ax2.semilogx(H_gnd2tm_noctrl.angle().rad2deg(),label='No Control',color='k',linewidth=2,linestyle='-')
ax2.semilogx((H_gndsens2tm+H_gndsus2tm).angle().rad2deg(),label='Total',color='r',linewidth=6)
ax2.semilogx(H_gndsus2tm.angle().rad2deg(),color='b',linewidth=2,linestyle='--')
ax2.semilogx(H_gndsens2tm.angle().rad2deg(),color='g',linewidth=2,linestyle='--')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlim(4e-2,1e1)
plt.savefig('./etmx/img/CLTF.png')
plt.close()


# ------------------------------------------------------------
# OLTF
# ------------------------------------------------------------
_omega = 2.0*np.pi*np.logspace(-4,3,1001)
servo = tf(servo,_omega)
oltf = tf(oltf,_omega)
P_ip2ip_noctrl = tf(P_ip2ip_noctrl,_omega)

print ('Plot OLTF')
plot_ipresponse = False
fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8),sharex=True)
ax.set_title('OLTF')
ax.loglog(oltf.abs(),label='OLTF (Simulation)',color='r',linewidth=2,linestyle='-')
ax.loglog(oltf0.abs(),label='OLTF0 (Actual)',color='g',linewidth=2,linestyle='-')
ax.loglog(servo.abs(),label='Servo',color='b',linewidth=2,linestyle='-')
ax.set_ylabel('Magnitude')
ax.set_ylim(1e-2,2e2)
ax.legend(fontsize=15,loc='upper left')
ax2.semilogx(oltf.angle().rad2deg(),label='OLTF',color='r',linewidth=2,linestyle='-')
ax2.semilogx(oltf0.angle().rad2deg(),label='OLTF0',color='g',linewidth=2,linestyle='-')
ax2.semilogx(servo.angle().rad2deg(),label='Servo',color='b',linewidth=2,linestyle='-')
if plot_ipresponse:
    ax.loglog(P_ip2ip_noctrl.abs()*2e2,label='Pa (Normalized)',color='k',
              linewidth=2,linestyle='--')
    ax2.semilogx(P_ip2ip_noctrl.angle().rad2deg(),color='k',linewidth=2,linestyle='--')
ax2.set_ylabel('Phase [Deg.]')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlim(1e-4,1e2)
plt.savefig('./etmx/img/OLTF.png')
plt.close()

print('Done')

# ------------------------------------------------------------
print ('Plot Sensor Noise')
fig,ax = plt.subplots(1,1,figsize=(8,8))
ax.set_title('Noise')
ax.loglog(gnd,label='Ground',color='black',linewidth=2,alpha=1,zorder=1)
ax.loglog(nseis,'--',label='Seismometer Noise',linewidth=2)
ax.loglog(nlvdt,'--',label='LVDT Noise',linewidth=2)
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Displacement [um/rtHz or um]')
ax.set_ylim(1e-6,1e1)
ax.set_xlim(1e-2,1e1)
ax.legend(fontsize=15,loc='lower left')
plt.savefig('./etmx/img/Noise.png')
plt.close()
