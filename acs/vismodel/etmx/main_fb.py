import control
from control import matlab,tf2ss,tf
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import zpk2tf
from vismodel.ip import Ps

# Single Pendulum
f0 = 0.1
w0 = f0*2*np.pi
Q = 3

# ETMX_IP_DAMP_L, SUSMod = Pa
num,den =  zpk2tf(np.array([-0.00312+1j*-0.155969,-0.00312-1j*-0.155969,
                        -0.00199+1j*-0.397995,-0.00199-1j*-0.397995,
                        -0.003435+1j*-0.686991,-0.003435-1j*-0.686991,
                        -0.0105375+1j*-0.842934,-0.0105375-1j*-0.842934,
                        -0.0159167+1j*-0.954867,-0.0159167-1j*-0.954867,
                        -0.00635125+1j*1.01618,-0.00635125-1j*1.01618,
                        -0.0225+1j*1.34981,-0.0225-1j*1.34981,
                        -0.02516+1j*1.25775,-0.02516-1j*1.25775])*(2.0*np.pi),
                        np.array([-0.00278125+1j*-0.444991,-0.00278125-1j*-0.444991,
                        -0.00363+1j*-0.725991,-0.00363-1j*-0.725991,
                        -0.00946+1j*-0.851347,-0.00946-1j*-0.851347,
                        -0.0161333+1j*-0.967866,-0.0161333-1j*-0.967866,
                        -0.00735+1j*1.02897,-0.00735-1j*1.02897,
                        -0.034125+1j*1.36457,-0.034125-1j*1.36457,
                        -0.03175+1j*1.2696,-0.03175-1j*1.2696,
                        -0.0048125+1j*-0.0768495,-0.0048125-1j*-0.0768495,
                        -0.00414+1j*-0.206959,-0.00414-1j*-0.206959])*(2.0*np.pi),
                        -0.0698906)
Pa = matlab.TransferFunction(num,den)
Pa = control.series(-1,Pa)

# Servo Filter
f0,f1 = 0.07,4
w0 = 2.0*np.pi*f0    
w1 = 2.0*np.pi*f1
servo = matlab.tf(*zpk2tf(np.array([-0.07,-0.07])*(2.0*np.pi),
                          np.array([-3.57143+1j*3.49927,-3.57143-1j*3.49927,
                                    -3.33333+1j*2.21108,-3.33333-1j*2.21108])*(2.0*np.pi),
                          19681172.6))
dc = matlab.tf(*zpk2tf([],np.array([-0.001])*(2.0*np.pi),[4]))
servo = control.series(dc,servo)

# Blending Filter (3rd)
fb = 0.1
wb = fb*(2.0*np.pi)
lp = matlab.tf([10*wb**3,5*wb**4,wb**5],
               [1,5*wb**1,10*wb**2,10*wb**3,5*wb**4,wb**5])
hp = matlab.tf([1,5*wb**1,10*wb**2,0,0,0],
               [1,5*wb**1,10*wb**2,10*wb**3,5*wb**4,wb**5])                    
# Closed Loop
oltf = control.series(Pa,servo) # G
cltf = control.feedback(oltf,1,-1) #G/(1+G)
hoge = control.feedback(1,oltf,-1) #1/(1+G)
gnd2tm_1 = cltf # from LVDT path
gnd2tm_2 = control.series(Ps,hoge) # from direct path
gnd2tm = control.parallel(gnd2tm_1,gnd2tm_2)
#gnd2tm = gnd2tm_1

# Bode Plot
wrap = lambda phases : ( phases + np.pi) % (2 * np.pi ) - np.pi
mag_ps,phase_ps,omega       = control.bode_plot(Ps,Plot=False,omega=np.logspace(-3,2,1e4),deg=False)
mag_pa,phase_pa,omega       = control.bode_plot(Pa,Plot=False,omega=np.logspace(-3,2,1e4),deg=False)
mag_lp,phase_lp,omega       = control.bode_plot(lp,Plot=False,omega=np.logspace(-3,2,1e4),deg=False)
mag_hp,phase_hp,omega       = control.bode_plot(hp,Plot=False,omega=np.logspace(-3,2,1e4),deg=False)
mag_servo,phase_servo,omega = control.bode_plot(servo,Plot=False,omega=np.logspace(-3,2,1e4),deg=False)
mag_oltf,phase_oltf,omega   = control.bode_plot(oltf,Plot=False,omega=np.logspace(-3,2,1e4),deg=False)
mag_gnd2tm,phase_gnd2tm,omega= control.bode_plot(gnd2tm,Plot=False,omega=np.logspace(-3,2,1e4),deg=False)

freq = omega/(2.0*np.pi)
fig,(ax1,ax2) = plt.subplots(2,1)
ax1.loglog(freq,mag_ps,label='Ps')
#ax1.loglog(freq,mag_lp,label='LP')
ax1.loglog(freq,mag_gnd2tm,label='GND2STG')
ax1.set_ylim(1e-4,5)
#ax1.set_xlim(0.6,2)
ax1.grid(which='major',color='black',linestyle='-')
ax1.grid(which='minor',color='black',linestyle=':')
ax2.semilogx(freq,np.rad2deg(wrap(phase_ps)),label='Ps')
#ax2.semilogx(freq,np.rad2deg(wrap(phase_lp)),label='LP')
ax2.semilogx(freq,np.rad2deg(wrap(phase_gnd2tm)),label='GND2STG')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlabel('Frequency [Hz]')
ax2.grid(which='major',color='black',linestyle='-')
ax2.grid(which='minor',color='black',linestyle=':')
ax1.legend()
ax2.legend()
plt.savefig('./results/img_cltf.png')
plt.close()

freq = omega/(2.0*np.pi)
fig,(ax1,ax2) = plt.subplots(2,1)
ax1.loglog(freq,mag_ps,label='Ps')
ax1.loglog(freq,mag_servo,label='Servo')
ax1.loglog(freq,mag_oltf,label='OLTF')
ax1.set_ylim(1e-4,1e3)
ax1.grid(which='major',color='black',linestyle='-')
ax1.grid(which='minor',color='black',linestyle=':')
ax2.semilogx(freq,np.rad2deg(wrap(phase_ps)),label='Ps')
ax2.semilogx(freq,np.rad2deg(wrap(phase_servo)),label='Serco')
ax2.semilogx(freq,np.rad2deg(wrap(phase_oltf)),label='OLTF')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlabel('Frequency [Hz]')
ax2.grid(which='major',color='black',linestyle='-')
ax2.grid(which='minor',color='black',linestyle=':')
ax1.legend()
ax2.legend()
plt.savefig('./results/img_oltf.png')
plt.close()



freq = omega/(2.0*np.pi)
fig,(ax1,ax2) = plt.subplots(2,1)
ax1.loglog(freq,mag_lp,label='LP')
ax1.loglog(freq,mag_hp,label='HP')
ax1.set_ylim(5e-4,1e1)
ax1.grid(which='major',color='black',linestyle='-')
ax1.grid(which='minor',color='black',linestyle=':')
ax2.semilogx(freq,np.rad2deg(wrap(phase_lp)),label='LP')
ax2.semilogx(freq,np.rad2deg(wrap(phase_hp)),label='HP')
ax2.set_ylim(-180,180)
ax2.set_yticks(range(-180,181,90))
ax2.set_xlabel('Frequency [Hz]')
ax2.grid(which='major',color='black',linestyle='-')
ax2.grid(which='minor',color='black',linestyle=':')
ax1.legend()
ax2.legend()
plt.savefig('./results/img_blend.png')
plt.close()
