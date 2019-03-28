from control import matlab, bode
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

w0 = 0.1 # [Hz]
Q = 5 # [Hz]
Pa = matlab.tf([0.01],[1,w0/Q,w0**2] )
num,den = signal.zpk2tf([-0.1],[-10],[100])
damp = matlab.tf(num,den)
num,den = signal.zpk2tf([-0.1,-0.1],[0.0,-10],[100])
servo = matlab.tf(num,den)
oltf_damp = Pa*damp
sensfunc_damp = 1./(1.0+Pa+damp)
oltf_servo = Pa*servo
sensfunc_servo = 1./(1.0+Pa+servo)

if True:
    t = np.linspace(0, 3000, 1e5)
    yout, T = matlab.step(Pa, t)
    plt.plot(T, yout)
    yout, T = matlab.step(sensfunc_servo, t)
    plt.plot(T, yout)    
    plt.axhline(1, color="b", linestyle="--")
    plt.savefig('hoge.png')
    plt.close()
    exit()

fig ,[ax0,ax1] = plt.subplots(2,1)
mag,phase,omega = bode(Pa,np.logspace(-3,2,1e5),label='Pa',Plot=False)
ax0.loglog(omega,mag,'b-',label='IP response')
ax1.semilogx(omega,phase,'b-')

mag,phase,omega = bode(servo,np.logspace(-3,2,1e5),label='Servo',Plot=False)
ax0.loglog(omega,mag,'k-',label='Servo Filter')
ax1.semilogx(omega,phase,'k-')
mag,phase,omega = bode(oltf_servo,np.logspace(-3,2,1e5),Plot=False)
ax0.loglog(omega,mag,'r-',label='openloop w/ servo')
ax1.semilogx(omega,phase,'r-')

# mag,phase,omega = bode(sensfunc_servo,np.logspace(-3,2,1e5),Plot=False)
# ax0.loglog(omega,mag,'g-',label='sensitive func. w/ servo')
# ax1.semilogx(omega,phase,'g-')

ax0.set_ylim(1e-2,1e5)
ax1.set_ylim(-180,180)
ax1.set_yticks(np.arange(-180,181,90))
ax0.set_xlim(1e-3,2e1)
ax1.set_xlim(1e-3,2e1)
ax0.grid(b=True, which='major', color='gray', linestyle=':')
ax0.grid(b=True, which='minor', color='gray', linestyle=':')
ax1.grid(b=True, which='major', color='gray', linestyle=':')
ax1.grid(b=True, which='minor', color='gray', linestyle=':')
ax0.legend(loc='lower left')
plt.savefig('ServoFilterDesign.png')



fig ,[ax0,ax1] = plt.subplots(2,1)
mag,phase,omega = bode(Pa,np.logspace(-3,2,1e5),label='Pa',Plot=False)
ax0.loglog(omega,mag,'b-',label='IP response')
ax1.semilogx(omega,phase,'b-')
mag,phase,omega = bode(damp,np.logspace(-3,2,1e5),label='Damp',Plot=False)
ax0.loglog(omega,mag,'k-',label='Damp Filter')
ax1.semilogx(omega,phase,'k-')
mag,phase,omega = bode(oltf_damp,np.logspace(-3,2,1e5),Plot=False)
ax0.loglog(omega,mag,'r-',label='openloop w/ damp')
ax1.semilogx(omega,phase,'r-')
# mag,phase,omega = bode(sensfunc_damp,np.logspace(-3,2,1e5),Plot=False)
# ax0.loglog(omega,mag,'g-',label='sensitive func. w/ servo')
# ax1.semilogx(omega,phase,'g-')

ax0.set_ylim(1e-2,1e5)
ax1.set_ylim(-180,180)
ax1.set_yticks(np.arange(-180,181,90))
ax0.set_xlim(1e-3,2e1)
ax1.set_xlim(1e-3,2e1)
ax0.grid(b=True, which='major', color='gray', linestyle=':')
ax0.grid(b=True, which='minor', color='gray', linestyle=':')
ax1.grid(b=True, which='major', color='gray', linestyle=':')
ax1.grid(b=True, which='minor', color='gray', linestyle=':')
ax0.legend(loc='lower left')
plt.savefig('DampFilterDesign.png')

