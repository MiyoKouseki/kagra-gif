import matplotlib.pyplot as plt
import numpy as np
from scipy.special import jv

f = np.logspace(-3,2,1e6)
w = 2.0*np.pi*f
L = 3000.0 # m
c = 5500.0 # m/sec

cdmr1 = lambda w: np.sqrt(abs(1.0/np.tan(L*w/c/2)))
cdmr2 = lambda w: np.sqrt((1+jv(0,L*w/c))/(1-jv(0,L*w/c)))

fig,(ax0,ax1) = plt.subplots(2,1,dpi=300)


ax1.loglog(f,cdmr1(w),'--')
ax1.loglog(f,cdmr2(w),'--')
ax1.set_ylim(1e-1,1e2)
ax1.set_xlim(1e-3,1e2)
plt.savefig('cdmr.png')
plt.close()
