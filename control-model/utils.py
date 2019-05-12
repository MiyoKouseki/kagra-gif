from scipy.interpolate import interp1d
from control import matlab, bode
import numpy as np
from gwpy.frequencyseries import FrequencySeries


def times(tf_mag,tf_freq,asd,asd_freq):
    func = interp1d(tf_freq,tf_mag)
    vel2v = func(asd_freq[1:])
    asd = asd[1:]*vel2v
    if False:
        import matplotlib.pyplot as plt
        plt.loglog(tf_freq,tf_mag,'o-')
        plt.savefig('hoge.png')
        exit()
    return asd_freq[1:],asd

#def rms(tf_mag,tf_freq):    
#    return tf_freq,rms
def rms(asd,df):
    psd = asd**2
    rms = np.sqrt(np.cumsum(psd[::-1])[::-1]*df)
    return rms


def degwrap(phases):
    '''
    phases :  float
        phase of degree.
    '''
    phases = np.deg2rad(phases)
    phases = ( phases + np.pi) % (2 * np.pi ) - np.pi
    phases = np.rad2deg(phases)
    return phases

def _bode(*args,**kwargs):
    mag,phase,omega = bode(*args,**kwargs)
    freq = omega/2.0/np.pi
    return mag,phase,freq

def mybode(*args,**kwargs):
    freq = kwargs.pop('freq',None)
    kwargs['omega'] = freq*2.0*np.pi
    mag,phase,omega = bode(*args,**kwargs)
    phase = degwrap(phase)
    mag = FrequencySeries(mag,frequencies=freq)
    phase = FrequencySeries(phase,frequencies=freq)    
    return mag,phase


