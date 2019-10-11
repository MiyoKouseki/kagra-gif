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


# 1. Choose sensor to read the suspension response
read_sensor = 'seis_diff' #seis, oplev, gif, seis_diff
nominal = False

# 2. Choose plotting options
plot_req    = False
plot_noctrl = False
plot_gif = True
sc = False


# ------------------------------------------------------------
#  Input  : ???
#  Output : ???
# ------------------------------------------------------------
fftlen = 2**10
ovlp = fftlen/2   
start = 'Sep 28 2019 10:00:00 JST' # w/o SC 
end   = 'Sep 28 2019 13:30:00 JST' # w/o SC

if nominal:
    if read_sensor=='seis':
        gnd_vel = seismodel.kagra_seis('H',99)
        tm_oplev = None
        freq = gnd_vel.frequencies.value
        omega = 2.0*np.pi*freq
        gnd  = gnd_vel/(2.0*np.pi*freq)
        df = gnd.df.value
    else:
        raise KeyError('No nominal value of "{}"'.format(read_sensor))
elif not nominal and read_sensor=='seis_diff':
    print('Reading data')    
    print('- Input  : Ground differential with seismometer')
    gnd_vel = seismodel.kagra_seis_now(start,end,axis='L_diff',fftlen=fftlen,
                                       ovlp=ovlp,verbose=False)
    df = gnd_vel.df.value
    gnd_vel = gnd_vel.crop(df,8+df)
    freq = gnd_vel.frequencies.value
    omega = 2.0*np.pi*freq
    gnd  = gnd_vel/(2.0*np.pi*freq)
    df = gnd.df.value
    print('- Output : Xarm cavity locking with AOM')
    kwargs= {'host':'10.68.10.121','port':8088,'verbose':False}
    data = TimeSeries.fetch('K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16',start,end,**kwargs)
    xarm = data.asd(fftlength=fftlen,overlap=ovlp)
    c = 299792458 # m/sec
    lam = 1064e-9 # m 
    output = xarm*3000.0/(c/lam)*1e6
    
    
elif not nominal and read_sensor=='gif':
    print('Reading data')    
    print('- Input  : Ground differential')
    gnd_vel = seismodel.kagra_seis_now(start,end,axis='GIF',fftlen=fftlen,
                                       ovlp=ovlp,verbose=False)
    gnd_vel = gnd_vel.crop(df,8+df)
    gnd  = gnd_vel
    print('- Output : Xarm cavity locking with AOM')
    kwargs= {'host':'10.68.10.121','port':8088,'verbose':False}
    data = TimeSeries.fetch('K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16',start,end,**kwargs)
    xarm = data.asd(fftlength=fftlen,overlap=ovlp)
    c = 299792458 # m/sec
    lam = 1064e-9 # m 
    output = xarm*3000.0/(c/lam)*1e6
    
elif not nominal and read_sensor=='oplev':
    print('Reading data')    
    print('- Input  : Ground at the EXV')    
    gnd_vel = seismodel.kagra_seis_now(start,end,axis='X',fftlen=fftlen,
                                       ovlp=ovlp,verbose=False)
    df = gnd_vel.df.value
    gnd_vel = gnd_vel.crop(df,8+df)
    freq = gnd_vel.frequencies.value
    omega = 2.0*np.pi*freq
    gnd  = gnd_vel#/(2.0*np.pi*freq)
    df = gnd.df.value
    print('- Output : Oplev at ETMX')
    kwargs= {'host':'10.68.10.121','port':8088,'verbose':False}
    data = TimeSeries.fetch('K1:VIS-ETMX_TM_DAMP_L_IN1_DQ',start,end,**kwargs)    
    output = data.asd(fftlength=fftlen,overlap=ovlp)
    
    
# ------------------------------------------------------------    
# Sensor Noise
# ------------------------------------------------------------
# LVDT
nlvdt = nlvdt.interpolate(df).crop(df,8+df)
# Seismometer
nseis = ntr120(trillium='120QA',psd='ASD',unit='disp')*1e6


# ------------------------------------------------------------
# Suspension Response
# ------------------------------------------------------------
ff_factor = 1.
sc_factor = 1.

if read_sensor=='oplev':
    target = 'OpLev_TML'    
else:
    target = 'dispTML'            
if read_sensor=='gif':
    target = 'dispTML' # Assuming CMRR=0

print('Loading Suspension Models')    
print('No Control Model')
prefix = '/Users/miyo/Dropbox/Git/SuspensionModel/model/typeA/'
matfile = prefix + 'linmod/noctrl.mat'
noctrl = TypeA(matfile=matfile,actual=False)
H_gnd2tm_noctrl = noctrl.siso('accGndL',target)
P_ip2ip_noctrl = noctrl.siso('noiseActIPL','LVDT_IPL')
print('- Calc TF: gnd -> {0}'.format(target))
H_gnd2tm_noctrl = tf(H_gnd2tm_noctrl,omega)*(1j*omega)**2

print('IP DCdamp Model')
matfile = prefix + 'linmod/ipdcdamp.mat'
ipdcdamp = TypeA(matfile=matfile,actual=False)
H_gndsus2tm = ipdcdamp.siso('accGndL',target) # 1. Suspension Contrib.
H_gndsens2tm = ipdcdamp.siso('dispGndL_err',target) # 2. Sensor Contrib.
H_nlvdt2tm = ipdcdamp.siso('noiseLVDT_IPL',target) # (Must Same as 2.)
print('- Calc TF: gnd -> {0} (suspension contrib.)'.format(target))
H_gndsus2tm  = tf(H_gndsus2tm,omega)*(1j*omega)**2*ff_factor
print('- Calc TF: gnd -> {0} (sensor contrib.)'.format(target))
H_gndsens2tm = tf(H_gndsens2tm,omega)*sc_factor
print('- Calc TF: lvdt noise -> {0} (same as sensor contrib.)'.format(target))
H_nlvdt2tm = tf(H_nlvdt2tm,omega)







# ------------------------------------------------------------
#
#                          Plot 
# 
# ------------------------------------------------------------
if read_sensor=='oplev':    
    sensor_name = 'TML Oplev'
else:
    sensor_name = 'TML'
if read_sensor=='gif':        
    sensor_name = 'ARM'


# ------------------------------------------------------------
# Noisebudget of TM motion
# ------------------------------------------------------------
print('Plot Noisebudget of TM motion')
total = np.sqrt( \
        (gnd*(H_gndsus2tm + H_gndsens2tm))**2 \
        )
        
fig,ax = plt.subplots(1,1,figsize=(8,8))
ax.set_title('ETMX {0} Motion'.format(sensor_name))
ax.loglog(gnd,label='Seismic Noise',color='black',linewidth=2,alpha=1,zorder=1)
ax.loglog(gnd.rms(),color='black',linestyle='dashdot',linewidth=2,zorder=1)
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
ax.set_ylim(1e-5,2e1)
ax.set_xlim(1e-3,1e1)
#ax.loglog((nlvdt*H_nlvdt2tm).abs(),'--',label='Sensor Noise',linewidth=2)
if read_sensor=='oplev':        
    ax.loglog(output,label='TM oplev',color='m',linewidth=3,zorder=1)
    ax.loglog(output.rms(),color='m',linewidth=3,zorder=1,linestyle='dashdot')
if read_sensor=='gif':
    ax.loglog(output,label='Xarm',color='m',linewidth=3,zorder=1)
    ax.loglog(output.rms(),color='m',linewidth=3,zorder=1,linestyle='dashdot')
if read_sensor=='seis_diff':
    ax.loglog(output,label='Xarm',color='m',linewidth=3,zorder=1)
    ax.loglog(output.rms(),color='m',linewidth=3,zorder=1,linestyle='dashdot')        
if plot_noctrl:
    ax.loglog((gnd*H_gnd2tm_noctrl).abs(),label='No Control',color='gray',linewidth=2)
    ax.loglog((gnd*H_gnd2tm_noctrl).abs().rms(),color='gray',linewidth=2,linestyle='--')
if plot_req:
    print('!')
    print(req_brse)
    ax.loglog(_freq,req_brse,label='BRSE Requirement',linewidth=2,alpha=1,zorder=1)
    ax.loglog(_freq,req_drse,label='DRSE Requirement',linewidth=2,alpha=1,zorder=1)
    ax.set_ylim(1e-17,3e1)
    ax.set_xlim(5e-3,1e4)
if plot_gif:
    ref = seismodel.kagra_seis_now(start,end,axis='GIF',fftlen=fftlen,
                                       ovlp=ovlp,verbose=False)
    ax.loglog(ref,label='GIF',color='g',linewidth=3,zorder=0)
    
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Displacement [um/rtHz or um]')
ax.legend(fontsize=15,loc='lower left')
plt.savefig('./tmp.png')
plt.close()
