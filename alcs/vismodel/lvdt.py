import matplotlib.pyplot as plt
import numpy as np
from gwpy.frequencyseries import FrequencySeries

_freq, f0gas, h1, h2, h3 = np.loadtxt('./noise/LVDTnoiseETMX_disp.dat').T
lvdt = np.sqrt(h1**2 + h2**2 + h3**2)
lvdt = FrequencySeries(lvdt,frequencies=_freq,name='ETMX_LVDT_L',unit='um') # m/rtHz
lvdt.override_unit('m')
_lvdt = lvdt.interpolate(0.0009765625)

fig = plt.figure(figsize=(10,7))
plt.loglog(_freq,h1,label='ETMX IP H1')
plt.loglog(_freq,h2,label='ETMX IP H2')
plt.loglog(_freq,h3,label='ETMX IP H3 ')
#plt.loglog(_freq,lvdt,label='ETMX IP Length')
plt.loglog(lvdt,label='ETMX IP Length')
plt.loglog(_lvdt,label='ETMX IP Length')
plt.legend(fontsize=15)
plt.ylabel('Displacement [um/rtHz]')
plt.ylim(1e-4,1e0)
plt.xlabel('Frequency [Hz]')
plt.savefig('img_noise_etmx_lvdt.png')
plt.close()



