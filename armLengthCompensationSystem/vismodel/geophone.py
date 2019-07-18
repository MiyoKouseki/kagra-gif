from control import matlab,bode
import matplotlib.pyplot as plt
import numpy as np
from gwpy.frequencyseries import FrequencySeries

_freq, geo = np.loadtxt('./vismodel/noise/GEOnoiseproto_vel.dat').T
geo = np.sqrt(3)*geo
geo = FrequencySeries(geo,frequencies=_freq,name='ETMX_GEO_L',unit='um/sec') # m/rtHz


#Ge = 276 #[V/(m/s)], sensitivity
Ge = 1 #[V/(m/s)], sensitivity
eta = 0.28 # [], damping ratio
w0 = 1*2*np.pi # [rad/sec], resonant frequency
num = [-Ge,0,0]
den = [1,2*eta*w0,w0**2]
geo_tf = matlab.tf(num,den)



def plot_noise():
    fig = plt.figure(figsize=(10,7))
    plt.loglog(geo,label='ETMX IP GEOPHONE Length')
    plt.legend(fontsize=15)
    plt.ylabel('Displacement [um/sec/rtHz]')
    plt.ylim(1e-4,1e0)
    plt.xlabel('Frequency [Hz]')
    plt.savefig('img_noise_etmx_geo.png')


def plot_tf():
    bode(geo_tf,Plot=True)
    plt.savefig('hoge.png')

if __name__ == '__main__':
    #plot_noise()
    plot_tf()
