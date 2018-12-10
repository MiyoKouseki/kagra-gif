

import numpy as np
from astropy import units as u
from astropy.constants import k_B

Vnn = 3e-6*u.V/(u.Hz)**(1/2.)
fcv = 2.7*u.Hz
fcc = 140.0*u.Hz
Inn = 0.4e-12*u.A/(u.Hz)**(1/2.)
R1 = 10e3*u.ohm
R2 = 68e3*u.ohm
Rs = 10e3*u.ohm
T = (273+28)*u.K
e1 = np.sqrt(4*np.pi*k_B*T*R1)*(1+R2/R1)
e2 = np.sqrt(4*np.pi*k_B*T*R2)
es = np.sqrt(4*np.pi*k_B*T*Rs)*(R2/R1)
inn_s = Inn*Rs*(1+R2/R1)
inn_2 = Inn*R2
vnn = Vnn*(1+R2/R1)

f = 100*u.Hz

Pnn = vnn**2*(1+fcv/f) + (inn_s**2+inn_2**2)*(1+fcc/f) + e1**2 + e2**2 + es**2
print np.sqrt(Pnn)



