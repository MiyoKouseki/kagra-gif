import numpy as np
from scipy.signal import freqs, zpk2tf
from scipy.interpolate import interp1d    

from gwpy.frequencyseries import FrequencySeries

from miyopy.utils import trillium



def count2vel(fseries):

    c2v = 10.0/2**15
    degain = 10**(-30./20.)
    z,p,k = trillium.zpk_120qa()
    num,den = zpk2tf(z,p,k)
    w,h = freqs(num,den,worN=np.logspace(-4,5,1e2))
    mag = abs(h)
    f = w/np.pi/2.0
    func = interp1d(f,mag)
    if False:
        plt.loglog(f,abs(mag),'o')
        plt.loglog(_f,_mag)
        plt.savefig('hoge.png')
    _f = fseries.frequencies.value
    vel2v = func(_f[1:])
    value = fseries.value[1:]*c2v*degain/(vel2v)
    f0 = fseries.f0
    df = fseries.df   
    return FrequencySeries(value,df=df,f0=f0+df)
