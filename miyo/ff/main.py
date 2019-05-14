

# DESIGN   PR3_SF_SC_Z 6zpk([0.0045+i*0.00779423;0.0045-i*0.00779423;0.2979+i*0.515978;0.2979-i*0.515978;3.5+i*6.06218; \
#                            3.5-i*6.06218],[0.006+i*0.0103923;0.006-i*0.0103923;0.078125+i*0.302577;0.078125-i*0.302577; \
#                            0.39455+i*0.683381;0.39455-i*0.683381],1,"n")gain(0.0259747)gain(13.0392)

#DESIGN   PR3_SF_SC_Z 6
#zpk([0.0045+i*0.00779423; 0.0045-i*0.00779423; 0.2979+i*0.515978; 0.2979-i*0.515978; 3.5+i*6.06218; 3.5-i*6.06218],
#    [0.006+i*0.0103923; 0.006-i*0.0103923; 0.078125+i*0.302577; 0.078125-i*0.302577; 0.39455+i*0.683381; 0.39455-i*0.683381],1,"n")
#
#gain(0.0259747)gain(13.0392)

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

z = [0.0045+1j*0.00779423,
     0.0045-1j*0.00779423,
     0.2979+1j*0.515978,
     0.2979-1j*0.515978,
     3.5+1j*6.06218,
     3.5-1j*6.06218]
p = [0.006+1j*0.0103923,
     0.006-1j*0.0103923,
     0.078125+1j*0.302577,
     0.078125-1j*0.302577,
     0.39455+1j*0.683381,
     0.39455-1j*0.683381]
k = 1.0*0.0259747*13.0392



from control import matlab
w = np.logspace(-3,2,1e5)
z = [10-10j,10+10j]
p = [1]
k = 1
num, den = signal.zpk2tf(z,p,k)
K = matlab.tf(num, den)
mag,phase,w = matlab.bode(K,w,Plot=False)




w, h = signal.freqs_zpk(z,p,k,w)
mag = np.abs(h)#/np.abs(h[0])
phase = np.rad2deg(np.angle(h)*-1)


phase,mag,w = phase,mag,w
fig,ax = plt.subplots(2,1)
ax[0].loglog(w,mag,'k')
ax[0].grid(b=True, which='major', color='gray', linestyle=':')
ax[0].grid(b=True, which='minor', color='gray', linestyle=':')
ax[1].semilogx(w,phase,'k')
ax[1].grid(b=True, which='major', color='gray', linestyle=':')
ax[1].grid(b=True, which='minor', color='gray', linestyle=':')
ax[1].set_ylim(-180,180)
ax[1].set_yticks(np.arange(-180,181,90))
plt.savefig('bode.png')


