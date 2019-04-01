from control import matlab, bode
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from gwpy.frequencyseries import FrequencySeries
from utils import times,rms

def rms(asd,df):
    psd = asd**2
    rms = np.sqrt(np.cumsum(psd[::-1])[::-1]*df)
    return rms

def wrap(phases):
    '''
    phases :  float
        phase of degree.
    '''
    phases = np.deg2rad(phases)
    phases = ( phases + np.pi) % (2 * np.pi ) - np.pi
    phases = np.rad2deg(phases)
    return phases



# Inverted Pendulum
if True:
    f0 = 0.1 #[Hz]
    w0 = f0*(2.0*np.pi) # [rad Hz]
    Q = 2 # []
    Pa = matlab.tf([1],[1,w0/Q,w0**2] )#*700
    integ = matlab.tf([1],[1,0] )
    Ps = matlab.tf([w0/Q,w0**2],[1,w0/Q,w0**2])
if False:
    Ps = matlab.tf(*matlab.zpk2tf(
        [-0.01960354 -0.97998085j, -0.01960354 +0.97998085j, -0.01250354 -2.50067649j,
        -0.01250354 +2.50067649j, -0.02158274 -4.31649435j, -0.02158274 +4.31649435j,
        -0.06620907 -5.29631139j, -0.06620907 +5.29631139j, -0.10000737 -5.99960852j,
        -0.10000737 +5.99960852j, -0.03990608 -6.3848482j,  -0.03990608 +6.3848482j,
        -0.15808494 -7.90266611j, -0.15808494 +7.90266611j, -0.14137167 -8.48112199j,
        -0.14137167 +8.48112199j, -3.38325363-43.85197895j, -3.38325363+43.85197895j], 
        [-0.03023783-0.48285941j, -0.03023783+0.48285941j, -0.02739469-1.36946042j,
        -0.02739469+1.36946042j, -0.01747511-2.79596285j, -0.01747511+2.79596285j,
        -0.02280796-4.56153551j, -0.02280796+4.56153551j, -0.05943893-5.34917374j,
        -0.05943893+5.34917374j, -0.10136872-6.08127858j, -0.10136872+6.08127858j,
        -0.04618141-6.46523275j, -0.04618141+6.46523275j, -0.21441370-8.57386735j,
        -0.21441370+8.57386735j, -0.19949113-7.97715131j, -0.19949113+7.97715131j],
        3.64e-4))
    Pa = Ps#*700
    
mag_Pa,phase_Pa,omega_Pa = bode(Pa,np.logspace(-4,4,1e5),label='Pa',Plot=False)
mag_Ps,phase_Ps,omega_Ps = bode(Ps,np.logspace(-4,4,1e5),label='Ps',Plot=False)
mag_integ,phase_integ,omega_integ = bode(integ,np.logspace(-4,4,1e5),label='integ',Plot=False)


# Blend
if True:
    fb=0.1
    wb=fb*(2.0*np.pi)
    lowpass = matlab.tf([35*wb**4,21*wb**5,7*wb**6,wb**7],
                        [1,7*wb**1,21*wb**2,35*wb**3,35*wb**4,21*wb**5,7*wb**6,wb**7])
    highpass = matlab.tf([1,7*wb,21*wb**2,35*wb**3,0,0,0,0],
                        [1,7*wb**1,21*wb**2,35*wb**3,35*wb**4,21*wb**5,7*wb**6,wb**7])
    sumoftwo = lowpass+highpass
    mag_lowpass,phase_lowpass,omega_lowpass = bode(lowpass,np.logspace(-4,4,1e5),label='lowpass',Plot=False)
    mag_highpass,phase_highpass,omega_highpass = bode(highpass,np.logspace(-4,4,1e5),label='highpass',Plot=False)
    mag_sumoftwo,phase_sumoftwo,omega_sumoftwo = bode(sumoftwo,np.logspace(-4,4,1e5),label='sumoftwo',Plot=False)
    phase_lowpass = wrap(phase_lowpass)
    phase_highpass = wrap(phase_highpass)



# servo
if True:
    f0 = 0.01
    f1 = 10.0
    w0 = 2.0*np.pi*f0
    w1 = 2.0*np.pi*f1
    num,den = signal.zpk2tf([-w0,-w0],[0,-w1],[1e4])
    servo = matlab.tf(num,den)
    oltf = servo*Pa
    seis2stage = (Ps+oltf*lowpass)/(1+servo*Pa)
    mag_oltf,phase_oltf,omega_oltf = bode(oltf,np.logspace(-4,4,1e5),label='oltf',Plot=False)
    mag_seis2stage,phase_seis2stage,omega_seis2stage = bode(seis2stage,np.logspace(-4,4,1e5),label='seis2stage',Plot=False)
    mag_servo,phase_servo,omega_servo = bode(servo,np.logspace(-4,4,1e5),label='servo',Plot=False)

    
# Trillium120QA
if True:
    Tr120 = matlab.tf(*matlab.zpk2tf([0,0,-31.63,-160.0,-350.0,-3177.0],
                                    [-0.036614+0.037059j,-0.036614-0.037059j,
                                    -32.55,-142.0,
                                    -364.0+404.0j,-364.0-404.0j,
                                    -1260.0,
                                    -4900.0+5200.0j,-4900.0-5200.0j,
                                    -7100.0+1700.0j,-7100.0-1700.0j,
                                    ],
                                    1202.5*8.31871e17)
                        )
    mag_Tr120,phase_Tr120,omega_Tr120 = bode(Tr120,np.logspace(-4,4,1e5),label='Tr120',Plot=False)
    Tr120_u = matlab.tf(*matlab.zpk2tf([0,0,-31.63,-160.0,-350.0,-3177.0],
                                       [-0.036614+0.037059j,-0.036614-0.037059j,
                                        -32.55,-142.0,
                                        -364.0+404.0j,-364.0-404.0j,
                                        -1260.0,
                                        -4900.0+5200.0j,-4900.0-5200.0j,
                                        -7100.0+1700.0j,-7100.0-1700.0j,
                                       ],
                                        8.31871e17)
                        )
    mag_Tr120_u,phase_Tr120_u,omega_Tr120_u = bode(Tr120_u,np.logspace(-4,4,1e5),label='Tr120_u',Plot=False)

    
# Seismic Noise
if True:
    #seis = FrequencySeries.read('ixv_x_median.hdf5')
    seis = FrequencySeries.read('Xaxis_ixv1_50pct.hdf5')*1e6
    freq_seis = seis.frequencies
    #omega_seis = 2.0*np.pi*freq_seis
    freq_seis,mag_seis = times(1/mag_Tr120_u, omega_Tr120_u/(2.0*np.pi),
                           seis.value, freq_seis
                            )
    freq_seis,mag_seis = times(mag_integ, omega_integ/(2.0*np.pi),
                            mag_seis, freq_seis
                            )
    freq_seis_noctr,mag_seis_noctr = times(mag_Ps, omega_Ps,
                                        mag_seis, freq_seis
                                        )
# rms
#freq_rms_seis_noctr,mag_seis_noctr = rms(mag_seis_noctr,frew_seis_noctr)

asdplot = True
if asdplot:
    df = 1e-3
    fig ,ax0 = plt.subplots(1,1)
    ax0.loglog(omega_Ps/(2.0*np.pi),mag_Ps,'k',label='Ground Response')
    ax0.loglog(omega_Ps/(2.0*np.pi),rms(mag_Ps,df),'k--',label='Ground Response (RMS)')
    ax0.loglog(omega_seis2stage/(2.0*np.pi),mag_seis2stage,'r',label='Closed Loop')
    ax0.loglog(omega_seis2stage/(2.0*np.pi),rms(mag_seis2stage,df),'r--',label='Closed Loop(RMS)')    
    #ax0.loglog(omega_lowpass/(2.0*np.pi),mag_lowpass,'b-',label='Lowpass')
    #ax0.loglog(freq_seis,mag_seis,'k-',label='Seismic noise')    
    #ax0.loglog(freq_seis_noctr,mag_seis_noctr,'r-',label='No control')
    ax0.set_xlim(1e-3,2e1)
    ax0.set_ylim(1e-4,1e1)
    ax0.set_xlabel('Frequency [Hz]',fontsize=12)
    ax0.set_ylabel('Displacement [um/rtHz]',fontsize=12)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')    
    plt.savefig('NoiseBudget_PI.png')

    
plottr120 = False
if plottr120:
    fig ,[ax0,ax1] = plt.subplots(2,1)
    ax0.loglog(omega_Tr120_u/(2.0*np.pi),mag_Tr120_u,'b-',label='Trillium120QA')
    ax0.set_xlim(1e-3,2e2)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')
    ax0.set_ylabel('Magnitude ')    
    ax1.semilogx(omega_Tr120/(2.0*np.pi),phase_Tr120,'b-')
    ax1.set_ylim(-180,180)
    ax1.set_yticks(np.arange(-180,181,90))
    ax1.set_xlim(1e-3,2e3)
    ax1.set_xlabel('Frequency [rad Hz]')
    ax1.set_ylabel('Phase [degree]')
    ax1.grid(b=True, which='major', color='gray', linestyle=':')
    ax1.grid(b=True, which='minor', color='gray', linestyle=':')
    plt.savefig('Trillium120QA.png')

plotservo = True 
if plotservo:
    fig ,[ax0,ax1] = plt.subplots(2,1,figsize=(8,8),dpi=100)
    plt.suptitle('Servo filter',fontsize=30)
    ax0.loglog(omega_Ps/(2.0*np.pi),mag_Ps,'k-',label='Ground Response',alpha=0.5)
    ax0.loglog(omega_Pa/(2.0*np.pi),mag_Pa,'k--',label='Ground Response',alpha=0.5)    
    ax0.loglog(omega_oltf/(2.0*np.pi),mag_oltf,'g-',label='OpenLoop',alpha=0.5)
    ax0.loglog(omega_servo/(2.0*np.pi),mag_servo,'b-',label='Servo',alpha=0.5)
    ax0.set_xlim(1e-3,2e1)
    ax0.set_ylim(1e-4,1e2)
    ax0.set_yticks([1e-4,1e-3,1e-2,1e-1,1e0,1e1])
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')
    ax0.set_ylabel('Magnitude ')
    ax1.semilogx(omega_Ps/(2.0*np.pi),phase_Ps,'k-',label='Ps',alpha=0.5)
    ax1.semilogx(omega_Pa/(2.0*np.pi),phase_Pa,'k--',label='Ps',alpha=0.5)        
    ax1.semilogx(omega_oltf/(2.0*np.pi),phase_oltf,'g-',alpha=0.5)
    ax1.semilogx(omega_servo/(2.0*np.pi),phase_servo,'b-',alpha=0.5)
    ax1.set_ylim(-180,180)
    ax1.set_yticks(np.arange(-180,181,90))
    ax1.set_xlim(1e-3,2e1)
    ax1.set_xlabel('Frequency [Hz]')
    ax1.set_ylabel('Phase [degree]')
    ax1.grid(b=True, which='major', color='gray', linestyle=':')
    ax1.grid(b=True, which='minor', color='gray', linestyle=':')
    plt.savefig('Servo.png')    


plotblend = True
if plotblend:
    fig ,[ax0,ax1] = plt.subplots(2,1,figsize=(8,8),dpi=100)
    plt.suptitle('Belnding filter',fontsize=30)
    ax0.loglog(omega_lowpass/(2.0*np.pi),mag_lowpass,'k',label='lowpass')
    ax0.loglog(omega_highpass/(2.0*np.pi),mag_highpass,'k--',label='highpass')
    #ax0.loglog(omega_sumoftwo/(2.0*np.pi),mag_sumoftwo,'k--',label='sumoftwo')    
    ax0.set_xlim(1e-2,1e1)
    ax0.set_ylim(1e-4,1e1)
    ax0.set_yticks([1e-4,1e-3,1e-2,1e-1,1e0,1e1])
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')
    ax0.set_ylabel('Magnitude ')
    ax1.semilogx(omega_lowpass/(2.0*np.pi),phase_lowpass,'k',alpha=0.5)
    ax1.semilogx(omega_highpass/(2.0*np.pi),phase_highpass,'k--',alpha=0.5)
    #ax1.semilogx(omega_sumoftwo/(2.0*np.pi),phase_sumoftwo,'k--',label='sumoftwo')  
    ax1.set_ylim(-180,180)
    ax1.set_yticks(np.arange(-180,181,90))
    ax1.set_xlim(1e-2,1e1)
    ax1.set_xlabel('Frequency [Hz]')
    ax1.set_ylabel('Phase [degree]')
    ax1.grid(b=True, which='major', color='gray', linestyle=':')
    ax1.grid(b=True, which='minor', color='gray', linestyle=':')
    plt.savefig('Blend.png')    
