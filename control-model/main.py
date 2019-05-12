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
from vismodel.filt import servo,servo2,servo3
from seismodel.trillium import tr120,tr120_u,tr120_selfnoise

# Seismic Noise
print('Need fetch data!')
exit()
seis = FrequencySeries.read('./seismodel/data1_ixv_x_50pct.hdf5')*1e6
seis = seis.crop(1e-3,20)
freq = seis.frequencies.value
df = seis.df.value

# LVDT Noise
lvdt = lvdt.crop(1e-3,20)
lvdt = lvdt.interpolate(df) #um

# GEOPHONE Noise
geo = geo.crop(1e-3,20)
geo = geo.interpolate(df) #um/sec

# Strain-meter Noise
value = np.ones(len(freq))*5e-8*1e6 # um
strain = FrequencySeries(value,frequencies=freq)

# Inverted Pendulum

# Blend
lp,hp = blendfilter(fb=0.3,n=3,plot=True)
lp_50m,hp_50m = blendfilter(fb=0.05,n=4,plot=False)
lp_80m,hp_80m = blendfilter(fb=0.08,n=4,plot=False)
lp_100m,hp_100m = blendfilter(fb=0.10,n=4,plot=False)

# Servo
servogain = 5e3
#servo = servo(f0=0.05,f1=5.0,gain=servogain) # default
#servo = servo2(f0=0.05,f1=3.0,gain=servogain) #
servo = servo3(f0=5e-3,f1=5.0,gain=servogain) #

# Closed Loop
oltf = servo*Pa
gnd2stg = (Ps+oltf*lp)/(1.0+oltf)
geo2stg = oltf*hp/(1.0+oltf)
lvdt2stg = oltf*lp/(1.0+oltf)

def ctr_blend(fb=0.1):
    lp,hp = blendfilter(fb=fb,plot=False)    
    gnd2stg = (Ps+oltf*lp)/(1.0+oltf)
    geo2stg = oltf*hp/(1.0+oltf)
    lvdt2stg = oltf*lp/(1.0+oltf)
    ctr = gnd2stg #+ geo2stg + lvdt2stg
    return ctr
    
ctr = ctr_blend(0.10)
ctr200m = ctr_blend(0.20)
ctr100m = ctr_blend(0.10)
ctr80m = ctr_blend(0.08)
ctr50m = ctr_blend(0.05)

    
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
mag_ctr200m,phase_ctr200m = mybode(ctr200m,freq=freq,Plot=False)
mag_ctr100m,phase_ctr100m = mybode(ctr100m,freq=freq,Plot=False)
mag_ctr80m,phase_ctr80m = mybode(ctr80m,freq=freq,Plot=False)
mag_ctr50m,phase_ctr50m = mybode(ctr50m,freq=freq,Plot=False)
mag_gnd2stg,phase_gnd2stg = mybode(gnd2stg,freq=freq,Plot=False)
mag_geo2stg,phase_geo2stg = mybode(geo2stg,freq=freq,Plot=False)
mag_lvdt2stg,phase_lvdt2stg = mybode(lvdt2stg,freq=freq,Plot=False)
mag_servo,phase_servo = mybode(servo,freq=freq,Plot=False)
mag_tr120,phase_tr120 = mybode(tr120,freq=freq,Plot=False)
mag_tr120_u,phase_tr120_u = mybode(tr120_u,freq=freq,Plot=False)
mag_geo,phase_geo = mybode(geo_tf,freq=freq,Plot=False)
mag_integ,phase_integ = mybode(matlab.tf([1],[1,0]),freq=freq,Plot=False)    


# Projection
seis = seis/mag_tr120_u*mag_integ
geo = geo/mag_geo*mag_integ
noctr = seis*mag_Ps
ctr_seis = seis*mag_gnd2stg
ctr_lvdt = lvdt*mag_lvdt2stg 
ctr_geo = geo*mag_geo2stg
ctr_seis.override_unit('m')
ctr_geo.override_unit('m')
ctr_lvdt.override_unit('m')
ctr = ctr_seis + ctr_geo + ctr_lvdt
ctr_spsncr = ctr_geo + ctr_lvdt
#
ctr100m = seis*mag_ctr100m
ctr80m = seis*mag_ctr80m
ctr50m = seis*mag_ctr50m
#
supersensor = lvdt*mag_lp + geo*mag_hp

# Run
plot_stage_motion = True
plot_servo = True
plot_control = False
compare_blending_filter = False
compare_disp_noise = True
plot_supersensor_noise = True
    
if plot_stage_motion:
    df = 1e-2
    fig ,ax0 = plt.subplots(1,1,figsize=(7,6))
    plt.title('Stage motion of the Pre-Isolator')
    ax0.loglog(ctr ,'k',label='Stage motion',linewidth=5,zorder=1)
    ax0.loglog(ctr_spsncr,'r',label='Supersensor noise contrib.',linewidth=1)
    ax0.loglog(ctr_seis ,'g',label='Seismic noise contrb.',linewidth=1)    
    ax0.loglog(seis ,'k',label='Seismic noise',alpha=0.7,linewidth=1)
    ax0.text(1,0.07,'Strain-meter Noise Model',fontsize=10,
             bbox=dict(facecolor='wheat', edgecolor='k', boxstyle='round'))
    ax0.loglog(strain,'k--',alpha=0.5,linewidth=2,zorder=0)    
    ax0.set_xlim(1e-3,2e1)
    ax0.set_ylim(1e-5,5e0)
    ax0.set_xlabel('Frequency [Hz]',fontsize=15)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=15)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')    
    plt.savefig('img_stage_motion.png')


if plot_servo:
    fig ,[ax0,ax1] = plt.subplots(2,1,figsize=(10,9),dpi=100)
    ax0.loglog(mag_Ps,'k-',label='Ground Response',alpha=0.7)
    scale = 1e0
    ax0.loglog(mag_oltf/scale,'g-',label='OpenLoop',alpha=0.7)
    ax0.loglog(mag_servo/scale,'b-',label='Servo',alpha=0.7,linewidth=3)
    ax0.set_xlim(1e-3,2e1)
    ax0.set_ylim(1e-3,1e2)
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
    plt.savefig('img_servo.png')
    print 'img_servo.png'


if plot_control:
    df = 1e-2
    fig ,ax0 = plt.subplots(1,1,figsize=(7,6))
    ax0.loglog(mag_Ps,'k',label='Ground Response',linewidth=1)
    ax0.loglog(rms(mag_Ps,df),'k--',linewidth=3)
    ax0.loglog(mag_ctr200m,'r',label='Controled w/ 200 mHz blending',linewidth=1)    
    ax0.loglog(rms(mag_ctr200m,df),'r--',linewidth=1)
    ax0.set_xlim(1e-3,2e0)
    ax0.set_ylim(1e-3,1e1)
    ax0.set_xlabel('Frequency [Hz]',fontsize=12)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=12)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')    
    plt.savefig('img_control.png')
    

if compare_blending_filter:
    df = 1e-2
    fig ,ax0 = plt.subplots(1,1,figsize=(7,6))
    ax0.loglog(seis   ,'k',label='Ground motion w/o belnding',alpha=1,linewidth=3)
    ax0.loglog(ctr100m,'r',label='Blend 100 mHz ',alpha=0.7)
    ax0.loglog(ctr100m.rms(df),'r--',alpha=0.7,linewidth=2)
    ax0.loglog(ctr80m,'g',label='Blend 80 mHZ',alpha=0.7)
    ax0.loglog(ctr80m.rms(df),'g--',alpha=0.7,linewidth=2)
    ax0.loglog(ctr50m,'b',label='Blend 50 mHz',alpha=0.7)
    ax0.loglog(ctr50m.rms(df),'b--',alpha=0.7,linewidth=2)
    ax0.set_xlim(1e-3,2e0)
    ax0.set_ylim(1e-3,5e0)
    ax0.set_xlabel('Frequency [Hz]',fontsize=15)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=15)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')    
    plt.savefig('img_compare_blending_freq.png')
    
if compare_disp_noise:
    fig ,ax0 = plt.subplots(1,1,figsize=(7,6))
    ax0.loglog(seis   ,'k',label=u'Ground motion (50th pct) (tentative)',linewidth=2)
    ax0.loglog(lvdt   ,'r',label='LVDT Noise',alpha=1,linewidth=2)
    ax0.loglog(geo    ,'b',label='Geophone Noise',alpha=1,linewidth=2)
    ax0.text(1,0.07,'Strain-meter Noise Model',fontsize=10,
             bbox=dict(facecolor='wheat', edgecolor='k', boxstyle='round'))
    ax0.loglog(strain,'k--',alpha=0.5,linewidth=2,zorder=0)            
    ax0.set_xlim(1e-3,2e1)
    ax0.set_ylim(1e-6,2e0)
    ax0.set_xlabel('Frequency [Hz]',fontsize=15)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=15)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')    
    plt.savefig('img_compare_disp_noise.png')    

if plot_supersensor_noise:
    fig ,ax0 = plt.subplots(1,1,figsize=(7,6))
    plt.title('Supersensor Noise')
    ax0.loglog(ctr_spsncr,'k',label='Supersensor noise',linewidth=4,zorder=5)
    ax0.loglog(ctr_lvdt,'r',label='LVDT noise contrib.',alpha=1,linewidth=1)
    ax0.loglog(ctr_geo,'b',label='Geophone Noise contrib.',alpha=1,linewidth=1)
    ax0.text(1,0.07,'Strain-meter Noise Model',fontsize=10,
             bbox=dict(facecolor='wheat', edgecolor='k', boxstyle='round'))
    ax0.loglog(strain,'k--',alpha=0.5,linewidth=2,zorder=0)        
    ax0.loglog(seis   ,'gray',label=u'Seismic noise (50th percentile)',linewidth=2)
    ax0.set_xlim(1e-3,2e1)
    ax0.set_ylim(1e-5,5e0)
    ax0.set_xlabel('Frequency [Hz]',fontsize=15)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=15)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')    
    plt.savefig('img_supersensor_noise.png')
