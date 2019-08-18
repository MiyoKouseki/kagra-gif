from scipy import optimize
import numpy as np
import cmath
import matplotlib.pyplot as plt
'''
1. Q,f0,G(zpq) -> Zero,Pole,Gain(zpk)
2. Plot data
'''
# 1.
def zpq2zpk(fq):
    '''
    Convert from non-complex pole or zero to complex ones.
    '''
    f0 = fq[0]
    q = fq[1] 
    w0 = 2.0*np.pi*f0
    if not q==1.0/2.0:
        _p = (-1*w0)/(2.0*q)*(1.0+cmath.sqrt((1.0-2*q)*(1.0+2*q)))
        _m = (-1*w0)/(2.0*q)*(1.0-cmath.sqrt((1.0-2*q)*(1.0+2*q))) 
        return [_p,_m] # [rad Hz]
    else:
        return [-1*w0,np.nan] # [rad Hz]
            
pole_QFK = np.array([ # Fitted value by Lucia?
                      [0.077, 8],
                      [0.218, 25],                      
                      [0.445, 80],
                      [0.726, 100],
                      [0.8514, 45],
                      [0.968, 30],
                      [1.029, 70],
                      [1.365, 20],
                      [1.27, 20],
                   ])
zero_QFK = np.array([ # Fitted value by Lucia?
                      [0.156, 25],
                      [0.398, 100],
                      [0.687, 100],
                      [0.843, 40],
                      [0.955, 30],
                      [1.0162, 80],
                      [1.258, 25],    
                      [1.35, 30],
                      [7, 6.5]
                   ])
Gain = 3.64e-4
pole = np.array([zpq2zpk(qf) for qf in pole_QFK]).flatten()
zero = np.array([zpq2zpk(qf) for qf in zero_QFK]).flatten()

# 2.
def qfk(freq,*param):
    Gain = param[0]
    N = (len(param)-1)/2
    pole_f0 = param[1:N+1][::2]
    pole_q = param[1:N+1][1::2]
    zero_f0 = param[N+1:][::2]
    zero_q = param[N+1:][1::2]
    h = 1*Gain
    f = freq
    for p in zip(pole_f0,pole_q):
        pf0,pQ = p
        h *= (1./2./np.pi)**2/(-f**2+pf0/pQ*(1j*f)+pf0**2)
    for z in zip(zero_f0,zero_q):
        zf0,zQ = z
        h *= (2.*np.pi)**2*(-f**2+zf0/zQ*(1j*f)+zf0**2)
    return h

def deco(qfk):
    def wrapper(*args, **kwargs):
        return np.abs(qfk(*args, **kwargs))
    return wrapper

@deco
def qfk_mag(freq,*param):
    return qfk(freq,*param)

if __name__ == '__main__':
    param = np.r_[Gain,pole_QFK.flatten(),zero_QFK.flatten()]
    #h = qfk(freq,*param)
    #_mag,_phase = np.abs(h),np.rad2deg(np.angle(h))
    #_h = qfk_mag(_freq,*param)


    data = np.loadtxt('tfmodel.txt')
    freq = data[:,0]
    mag = data[:,1]
    phase = data[:,2]
    p_init = param
    p_opt, cov = optimize.curve_fit(qfk_mag, freq, mag, p0=p_init)
    _freq = np.logspace(-2,2,1e6)
    h = qfk(_freq,*p_opt)
    _mag,_phase = np.abs(h),np.rad2deg(np.angle(h))


    fig , [ax0,ax1] = plt.subplots(2,1)
    ax0.loglog(freq,mag,'ko',markersize=1)
    ax0.loglog(_freq,_mag,'r',linewidth=1)
    ax0.set_ylabel('Magnitude')
    ax1.semilogx(freq,phase,'ko',markersize=1)
    ax1.semilogx(_freq,_phase,'r',linewidth=1)
    ax1.set_ylim(-180,180,90)
    ax1.set_yticks(np.arange(-180,181,90))
    ax1.set_xlabel('Frequency [Hz]')
    ax1.set_ylabel('Phase [Deg.]')
    plt.savefig('./TF_ETMX.png')
