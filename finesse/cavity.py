import numpy as np
from pykat import finesse
import matplotlib.pyplot as plt

kat = finesse.kat()
kat.verbose = False
kattext ='''
# Optics configuration
m1 itm 40e-4 45e-4 0 n1 n2  # T=40ppm, Loss=45ppm @1064nm [1]
s s1 3000 n2 n3             # space L=3000m?
s s2 1 nn n1                # space L=1m?
m1 etm 10e-4 45e-4 0 n3 n4  # T=10ppm, Loss=45ppm @1064nm [1]
l i1 1 0 n0                 # laser P=1W, f_offset=0Hz
mod eo1 45k 0.3 2 pm n0 nn  # phase modulator 
    	    	     	    # f_mod=40kHz, midx=0.3, order=3

# Detector
pd1 refl_I 45k 0  n1
pd1 refl_Q 45k 90 n1
pd1 trans_I 45k 0 n4
pd1 trans_Q 45k 90 n4

# Output data 
xaxis etm phi lin -90 90 400
yaxis abs
#scale 1e6

# Reference
# [1] http://gwwiki.icrr.u-tokyo.ac.jp/JGWwiki/LCGT/subgroup/ifo/MIF/OptParam
'''
kat.parse(kattext)
out = kat.run()

fig, (ax0,ax1) = plt.subplots(2, 1, figsize=(10,6), dpi=320)
deg = out.x
refl = out.y[:,:2]
trans = out.y[:,2:]
ax0.plot(deg,refl)
ax0.legend(['Refl (I)','Refl (Q)'],loc='upper right')
ax1.plot(deg,trans)
ax1.legend(['Trans (I)','Trans (Q)'],loc='upper right')
ax0.set_title('PDH signal')
ax0.set_xticks(np.arange(-90,91,45))
ax1.set_xticks(np.arange(-90,91,45))
ax0.set_xlim(-90,90)
ax1.set_xlim(-90,90)
ax0.grid(b=None, which='both', axis='both', linestyle='--')
ax1.grid(b=None, which='both', axis='both', linestyle='--')
ax1.set_xlabel('Tuning ETM [deg]')
ax0.set_ylabel('Abs [?]')
ax1.set_ylabel('Abs [?]')
plt.savefig('cavity.png')
