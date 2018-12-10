


from gwpy.frequencyseries import FrequencySeries
import matplotlib.pyplot as plt
import numpy as np

asd_no5_temp = FrequencySeries.read('asd_no5_temp.hdf5')
asd_no5_humd = FrequencySeries.read('asd_no5_humd.hdf5')
asd_no5_baro = FrequencySeries.read('asd_no5_baro.hdf5')
asd_no6_temp = FrequencySeries.read('asd_no6_temp.hdf5')
asd_no6_humd = FrequencySeries.read('asd_no6_humd.hdf5')
asd_no6_baro = FrequencySeries.read('asd_no6_baro.hdf5')


import numpy as np
from astropy import units as u
from astropy.constants import k_B

Vnn = 3e-6*u.V/(u.Hz)**(1/2.)
fcv = 2.7*u.Hz
fcc = 140.0*u.Hz
Inn = 0.4e-12*u.A/(u.Hz)**(1/2.)
R1 = 10e3*u.ohm
R2 = 10e3*u.ohm
#R3 = 100e3*u.ohm
Rs = 10e3*u.ohm
T = (273+28)*u.K
e1 = np.sqrt(4*np.pi*k_B*T*R1)*(1+R2/R1)
e2 = np.sqrt(4*np.pi*k_B*T*R2)
es = np.sqrt(4*np.pi*k_B*T*Rs)*(R2/R1)
inn_s = Inn*Rs*(1+R2/R1)
inn_2 = Inn*R2
inn = Inn*Rs
vnn = Vnn*(1+R2/R1)
f = np.logspace(-3,3,1e3)*u.Hz

Enn = vnn**2*(1+fcv/f) + (inn_s**2+inn_2**2)*(1+fcc/f) + e1**2 + e2**2 + es**2
Enn = vnn**2*(1+fcv/f) #+ inn**2
print 'First Amp output {0}'.format(np.sqrt(Enn))
noise = np.sqrt(Enn)#/3

plot, ax0 = plt.subplots(nrows=1, figsize=(8, 8), sharex=True)
c2V = 2.0*10/2**15
ax0.loglog(asd_no5_baro,label='No5(IXV)')
ax0.loglog(asd_no6_baro,label='No6(IYC)')
ax0.loglog(f,noise,label='noise',color='k',linestyle='--')
xlimmax = 500
xlimmin = asd_no5_baro.frequencies[1].value
ax0.set_xlim(xlimmin,xlimmax)
ax0.set_ylim(1e-6,1e0)
ax0.legend()
ax0.set_ylabel('Temperature [V/rtHz]')
ax0.set_xlabel('Frequency [Hz]')
plot.savefig('NoiseBudget.png')
