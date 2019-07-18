#
#! coding: utf-8
from control import matlab
import matplotlib.pyplot as plt
import numpy as np
from gwpy.frequencyseries import FrequencySeries
from vismodel.utils import times,rms,_bode,degwrap,mybode
from vismodel.lvdt import lvdt
from vismodel.geophone import geo,geo_tf
from vismodel.ip import Ps,Pa
from vismodel.filt import blendfilter
from vismodel.filt import servo,servo2,servo3,servo4
from seismodel.trillium import tr120,tr120_u,tr120_selfnoise

# Seismic Noise
#seis = FrequencySeries.read('./seismodel/data1_ixv_x_50pct.hdf5')*1e6
print('temporal data')
seisETMX = FrequencySeries.read('./seismodel/2018Dec10_exv.hdf5')
seisITMX = FrequencySeries.read('./seismodel/2018Dec10_ixv.hdf5')
seisETMX = seisETMX.crop(1e-3,20)
seisITMX = seisETMX.crop(1e-3,20)
freq = seisETMX.frequencies.value
df = seisETMX.df.value

# Run
plot_stage_motion = True
plot_servo = True
plot_control = True
compare_disp_noise = True
plot_supersensor_noise = True
plot_ST = True

# LVDT Noise
lvdt = lvdt.crop(1e-3,20)
lvdt = lvdt.interpolate(df) #um

# GEOPHONE Noise
geo = geo.crop(1e-3,20)
geo = geo.interpolate(df) #um/sec

# Strain-meter Noise
value = np.ones(len(freq))*2e-12*3e3*1e6 # um
strain = FrequencySeries(value,frequencies=freq)

# Blend
lp,hp = blendfilter(fb=0.2,n=4,plot=True)

# Servo
servogain = 1e5
#servo = servo(f0=0.05,f1=5.0,gain=servogain) # default \/-\
#servo = servo2(f1=10.0,gain=servogain) # /-\
#servo = servo3(f0=5e-3,f1=10.0,gain=servogain) # _/-\
servo = servo4(f0=5e-3,f1=10.0,gain=servogain) # _/-\

# Sensor Correction
Csc = 1.0
err = 0.0
Csc = Csc*(1-err)

# TransferFunction
oltf = servo*Pa
exvgnd2stg = (Ps+oltf*lp*(1.0-Csc))/(1.0+oltf)
exvgnd2stg_noctr = Ps
geo2stg = oltf*hp/(1.0+oltf)
lvdt2stg = oltf*lp/(1.0+oltf)
strain2stg = oltf*lp*Csc/(1.0+oltf)
ixvgnd2stg = oltf*lp*Csc/(1.0+oltf)
s_func = 1/(1.0+oltf)*Ps
t_func = oltf/(1.0+oltf)*lp

def ctr_blend(fb=0.1):
    lp,hp = blendfilter(fb=fb,plot=False)    
    exvgnd2stg = (Ps+oltf*lp)/(1.0+oltf)
    geo2stg = oltf*hp/(1.0+oltf)
    lvdt2stg = oltf*lp/(1.0+oltf)
    ctr = exvgnd2stg #+ geo2stg + lvdt2stg
    return ctr
    
ctr = ctr_blend(0.20)
    
# Trillium120QA
tr120_selfnoise = tr120_selfnoise*1e6
       
#
# Plot
#
mag_Pa,phase_Pa = mybode(Pa,freq=freq,Plot=False)
mag_Ps,phase_Ps = mybode(Ps,freq=freq,Plot=False)
mag_lp,phase_lp = mybode(lp,freq=freq,Plot=False)
mag_hp,phase_hp = mybode(hp,freq=freq,Plot=False)
mag_oltf,phase_oltf = mybode(oltf,freq=freq,Plot=False)
mag_ctr,phase_ctr = mybode(ctr,freq=freq,Plot=False)
mag_s,phase_s = mybode(s_func,freq=freq,Plot=False)
mag_t,phase_t = mybode(t_func,freq=freq,Plot=False)
mag_exvgnd2stg,phase_exvgnd2stg = mybode(exvgnd2stg,freq=freq,Plot=False)
mag_exvgnd2stg_noctr,phase_exvgnd2stg_noctr = mybode(exvgnd2stg_noctr,freq=freq,Plot=False)
mag_ixvgnd2stg,phase_ixvgnd2stg = mybode(ixvgnd2stg,freq=freq,Plot=False)
mag_geo2stg,phase_geo2stg = mybode(geo2stg,freq=freq,Plot=False)
mag_lvdt2stg,phase_lvdt2stg = mybode(lvdt2stg,freq=freq,Plot=False)
mag_strain2stg,phase_strain2stg = mybode(strain2stg,freq=freq,Plot=False)
mag_servo,phase_servo = mybode(servo,freq=freq,Plot=False)
mag_tr120,phase_tr120 = mybode(tr120,freq=freq,Plot=False)
mag_tr120_u,phase_tr120_u = mybode(tr120_u,freq=freq,Plot=False)
mag_geo,phase_geo = mybode(geo_tf,freq=freq,Plot=False)
mag_integ,phase_integ = mybode(matlab.tf([1],[1,0]),freq=freq,Plot=False)    

# Projection
seisETMX = seisETMX/mag_tr120_u*mag_integ
seisITMX = seisITMX/mag_tr120_u*mag_integ
geo = geo/mag_geo*mag_integ
noctr = seisETMX*mag_Ps
ctr_seisETMX_noctrl = seisETMX*mag_exvgnd2stg_noctr
ctr_seisETMX = seisETMX*mag_exvgnd2stg
ctr_seisITMX = seisITMX*mag_ixvgnd2stg
ctr_lvdt = lvdt*mag_lvdt2stg 
ctr_geo = geo*mag_geo2stg
ctr_strain = strain*mag_strain2stg
#
ctr_seisETMX.override_unit('m')
ctr_seisITMX.override_unit('m')
ctr_geo.override_unit('m')
ctr_lvdt.override_unit('m')
ctr_strain.override_unit('m')
ctr = np.sqrt(ctr_seisETMX**2 + ctr_geo**2 + ctr_lvdt**2 + ctr_strain**2 + ctr_seisITMX**2)
ctr_itmx = np.sqrt(ctr_geo**2 + ctr_lvdt**2 + ctr_seisITMX**2)
ctr_spsncr = np.sqrt(ctr_geo**2 + ctr_lvdt**2)
#
supersensor = np.sqrt((lvdt*mag_lp)**2 + (geo*mag_hp)**2)
    
if plot_stage_motion:
    #
    # ETMX
    #
    fig ,ax0 = plt.subplots(1,1,figsize=(12,7))
    plt.title('Expected performance of the ETMX pre-isolator stage',fontsize=25)
    ax0.loglog(ctr.crop(0.08) ,'k',label='Stage motion',linewidth=5,zorder=0)
    ax0.loglog(ctr ,'k--',linewidth=5,alpha=0.2)
    ax0.loglog(ctr_seisETMX.crop(0.08) ,'orange',label='1. Ground motion @ ETMX',linewidth=2)
    ax0.loglog(ctr_seisETMX,'orange',linestyle='--',linewidth=2,alpha=0.2)    
    ax0.loglog(ctr_seisITMX.crop(0.08) ,'b',label='2. Ground motion @ ITMX',linewidth=2)
    ax0.loglog(ctr_seisITMX,'b',linestyle='--',linewidth=2,alpha=0.2)
    ax0.loglog(ctr_strain,'g',label='3. Strainmeter noise (Laser Freq. noise)',linewidth=2)
    ax0.loglog(ctr_spsncr,'r',label='4. Supersensor noise',linewidth=3)
    #ax0.loglog(ctr_seisETMX_noctrl,'gray',label='Ref. No control',linewidth=2,zorder=0)
    ax0.set_xlim(5e-3,2e0)
    ax0.set_ylim(1e-5,2e0)
    ax0.set_xlabel('Frequency [Hz]',fontsize=25)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=25)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left',fontsize=20)
    ax0.text(2.1, 1e-6, 'START : {0}'.format('Dec 10 2018 00:00:00 UTC'), rotation=90,ha='left',va='bottom')
    ax0.text(2.3, 1e-6, 'BW : 1.95e-03, Window : hanning, AVE : 8', rotation=90,ha='left',va='bottom')
    plt.savefig('./results/img_stage_motion_ETMX.png')
    print('plot ./results/img_stage_motion_ETMX.png')

if plot_stage_motion:
    #
    # ITMX
    #
    fig ,ax0 = plt.subplots(1,1,figsize=(7,6))
    plt.title('Stage motion of the ITMX pre-isolator')
    ax0.loglog(ctr ,'k',label='Stage motion',linewidth=5,zorder=1)
    ax0.loglog(ctr.rms(df=df) ,'k--',label='Stage motion (RMS)',linewidth=3,zorder=1)
    ax0.loglog(ctr_seisITMX ,'b',label='2. Ground noise @ ITMX',linewidth=2)
    ax0.loglog(ctr_spsncr,'r',label='4. Supersensor noise',linewidth=2)
    ax0.set_xlim(1e-3,2e1)
    ax0.set_ylim(1e-5,5e0)
    ax0.set_xlabel('Frequency [Hz]',fontsize=15)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=15)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')
    ax0.text(21, 1e-5, 'START : {0}'.format('Dec 10 2018 00:00:00 UTC'), rotation=90,ha='left',va='bottom')
    ax0.text(26, 1e-5, 'BW : 1.95e-03, Window : hanning, AVE : 8', rotation=90,ha='left',va='bottom')
    plt.savefig('./results/img_stage_motion_ITMX.png')
    print('plot ./results/img_stage_motion_ITMX.png')    

if plot_stage_motion:
    #
    # CAVITY
    #
    fig ,ax0 = plt.subplots(1,1,figsize=(7,6))
    plt.title('Stage motion of the X arm cavity')
    ax0.loglog(ctr_seisETMX ,'g',label='1. Length displacement noise ',linewidth=2)
    ax0.loglog(ctr ,'k',label='Stage motion',linewidth=5,zorder=1)
    ax0.loglog(ctr.rms(df=df) ,'k--',label='Stage motion (RMS)',linewidth=3,zorder=1)
    ax0.loglog(0,0,'b',label='2. Ground noise Arm',linewidth=2)
    ax0.loglog(ctr_strain,'y',label='3. Strainmeter noise (Preliminary)',linewidth=2) 
    ax0.loglog(ctr_spsncr,'r',label='4. Supersensor noise',linewidth=2)
    ax0.set_xlim(1e-3,2e1)
    ax0.set_ylim(1e-5,5e0)
    ax0.set_xlabel('Frequency [Hz]',fontsize=15)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=15)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')
    ax0.text(21, 1e-5, 'START : {0}'.format('Dec 10 2018 00:00:00 UTC'), rotation=90,ha='left',va='bottom')
    ax0.text(26, 1e-5, 'BW : 1.95e-03, Window : hanning, AVE : 8', rotation=90,ha='left',va='bottom')
    plt.savefig('./results/img_stage_motion.png')
    print('plot ./results/img_stage_motion.png')    
    

if plot_servo:
    fig ,[ax0,ax1] = plt.subplots(2,1,figsize=(10,9),dpi=100)
    ax0.loglog(mag_Ps,'k-',label='Ground Response',alpha=0.7)
    scale = 1e0
    ax0.loglog(mag_oltf/scale,'g-',label='OpenLoop',alpha=0.7)
    ax0.loglog(mag_servo/scale,'b-',label='Servo',alpha=0.7,linewidth=3)
    ax0.set_xlim(1e-3,2e1)
    ax0.set_ylim(1e-3,1e3)
    ax0.set_yticks([1e-3,1e-2,1e-1,1e0,1e1,1e2])
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left',fontsize=15)
    ax0.set_ylabel('Magnitude ')
    ax1.semilogx(phase_Ps,'k-',label='Ps',alpha=0.7)
    ax1.semilogx(phase_oltf,'g-',alpha=0.7)
    ax1.semilogx(phase_servo,'b-',alpha=0.7,linewidth=3)
    ax1.set_ylim(-180,180)
    ax1.set_yticks(np.arange(-180,181,90))
    ax1.set_xlim(1e-3,2e1)
    ax1.set_xlabel('Frequency [Hz]')
    ax1.set_ylabel('Phase [degree]')
    ax1.grid(b=True, which='major', color='gray', linestyle=':')
    ax1.grid(b=True, which='minor', color='gray', linestyle=':')
    plt.savefig('./results/img_servo.png')
    print './results/img_servo.png'


if plot_control:
    print('plot control')
    fig ,ax0 = plt.subplots(1,1,figsize=(7,6))
    ax0.loglog(mag_Ps,'k',label='Ground Response',linewidth=1)
    ax0.loglog(rms(mag_Ps,df=1e-2),'k--',linewidth=3)
    ax0.loglog(mag_ctr,'r',label='Controled',linewidth=1)    
    ax0.loglog(rms(mag_ctr,df=1e-2),'r--',linewidth=1)
    ax0.set_xlim(1e-3,2e0)
    ax0.set_ylim(1e-3,1e1)
    ax0.set_xlabel('Frequency [Hz]',fontsize=12)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=12)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')    
    plt.savefig('./results/img_control.png')


if plot_ST:
    print('plot ST')
    fig ,[ax0,ax1] = plt.subplots(2,1,figsize=(10,9),dpi=100)
    ax0.loglog(mag_s,'g-',label='s',alpha=0.7)
    ax0.loglog(mag_t,'b-',label='t',alpha=0.7,linewidth=3)
    ax0.set_xlim(1e-3,2e2)
    ax0.set_ylim(1e-3,1e2)
    ax0.set_yticks([1e-3,1e-2,1e-1,1e0,1e1,1e2])
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left',fontsize=15)
    ax0.set_ylabel('Magnitude ')
    ax1.semilogx(phase_s,'g-',alpha=0.7)
    ax1.semilogx(phase_t,'b-',alpha=0.7,linewidth=3)
    ax1.set_ylim(-180,180)
    ax1.set_yticks(np.arange(-180,181,90))
    ax1.set_xlim(1e-3,2e2)
    ax1.set_xlabel('Frequency [Hz]')
    ax1.set_ylabel('Phase [degree]')
    ax1.grid(b=True, which='major', color='gray', linestyle=':')
    ax1.grid(b=True, which='minor', color='gray', linestyle=':')
    plt.savefig('./results/img_sensitivity.png')
    print './results/img_sensitivity.png'
    
    
if compare_disp_noise:
    fig ,ax0 = plt.subplots(1,1,figsize=(7,6))
    ax0.loglog(seisETMX   ,'k',label=u'Ground motion',linewidth=2)
    ax0.loglog(lvdt*np.sqrt(2),'r',label=r'LVDT Noise $\times{\sqrt{2}}$',alpha=1,linewidth=2)
    ax0.loglog(geo*np.sqrt(2),'b',label=r'Geophone Noise $\times{\sqrt{2}}$',alpha=1,linewidth=2)
    ax0.loglog(strain,'k--',label='Strainmeter Noise (Preliminary)',alpha=0.5,linewidth=2,zorder=0)
    ax0.set_xlim(1e-3,1e1)
    ax0.set_ylim(1e-6,1e1)
    ax0.set_xlabel('Frequency [Hz]',fontsize=15)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=15)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.text(11, 1e-6, 'START : {0}'.format('Dec 10 2018 00:00:00 UTC'), rotation=90,ha='left',va='bottom')
    ax0.text(14, 1e-6, 'BW : 1.95e-03, Window : hanning, AVE : 8', rotation=90,ha='left',va='bottom')    
    ax0.legend(loc='lower left')    
    plt.savefig('./results/img_compare_disp_noise.png')    

if plot_supersensor_noise:
    fig ,ax0 = plt.subplots(1,1,figsize=(7,6))
    plt.title('Supersensor Noise')
    ax0.loglog(ctr_spsncr,'k',label='Supersensor noise',linewidth=4,zorder=5)
    ax0.loglog(ctr_lvdt,'r',label='LVDT noise contrib.',alpha=1,linewidth=1)
    ax0.loglog(ctr_geo,'b',label='Geophone Noise contrib.',alpha=1,linewidth=1)
    ax0.text(1,0.07,'Strainmeter Noise',fontsize=10,
             bbox=dict(facecolor='wheat', edgecolor='k', boxstyle='round'))
    ax0.loglog(strain,'k--',alpha=0.5,linewidth=2,zorder=0)        
    ax0.loglog(seisETMX   ,'gray',label=u'SeisETMXmic noise (50th percentile)',linewidth=2)
    ax0.set_xlim(1e-3,2e1)
    ax0.set_ylim(1e-5,5e0)
    ax0.set_xlabel('Frequency [Hz]',fontsize=15)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=15)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')    
    plt.savefig('./results/img_supersensor_noise.png')
