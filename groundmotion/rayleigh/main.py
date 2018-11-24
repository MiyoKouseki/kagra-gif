from sympy import *
import numpy as np
'''
Reference

    [1] Takemoto, Shuzo, et al. "A 100 m laser strainmeter system in the Kamioka Mine, Japan, for precise observations of tidal strains." Journal of Geodynamics 41.1-3 (2006): 23-29.
'''


def alpha(_nu):
    x=Symbol('x')
    nu=Symbol('nu')
    _ans = solve(x**3 - 8.0*x**2 + 8.0*(2.0-nu)/(1.0-nu)*x - 8.0/(1.0-nu) ,x)
    ans = [ a.evalf(subs={nu:_nu}) for a in _ans ]
    ans = np.fromiter(ans, dtype=complex)    
    ans = np.sqrt(ans).real
    return ans[0]


def beta(_nu):
    return np.sqrt((2.0-2.0*_nu)/(1.0-2.0*_nu))


def q(alpha,beta):
    return np.sqrt(1.0-(alpha/beta)**2)


def p(alpha):
    return np.sqrt(1.0-alpha**2)


def horizontal(x,z,kr,q,p):
    '''

    Parameters
    ----------
    x : array-like
        direction vector. 3 components;{x,y,x}.
    z : array-like
        depth.
    kr : array-like
        wave number vector. 3 components;{x,y,z}
    p : float
        dimensionless number calculated with poisson ratio
    q : float
        dimensionless number calculated with poisson ratio

    Returns
    -------
    value : array-like
        3*N dimension array when len(z)=N.

    '''
    return kr*(np.exp(-q*2*np.pi*z) \
                    - 2.0*q*p/(1.0+p**2)*np.exp(-p*2*np.pi*z) \
                    )

           
def vertical(x,z,kr,q,p):
    '''

    Parameters
    ----------
    x : array-like
        direction vector. 3 components;{x,y,x}.
    z : array-like
        depth normarized with wave length
    kr : array-like
        wave number vector. 3 components;{x,y,z}
    p : float
        dimensionless number calculated with poisson ratio
    q : float
        dimensionless number calculated with poisson ratio

    Returns
    -------
    value : array-like
        3*N dimension array when len(z)=N.
    '''
    return -q*kr*(np.exp(-q*2.0*np.pi*z) \
                      - 2.0/(1.0+p**2)*np.exp(-p*2*np.pi*z) \
                      )
                      

if __name__ == '__main__':
    _nu = 0.283 # [1]
    #_nu = 0.16
    _alpha = alpha(_nu)
    _beta = beta(_nu)
    _q = q(_alpha,_beta)
    _p = p(_alpha)
    print _p,_q
    lambda_r = 50.0e3 # meter
    x = np.array([1.,0.,0.]) # aim x direction
    z = np.linspace(0,2,100) # normarized depth
    kr = np.array([2*np.pi/lambda_r,0.,0.]) # x direction
    kr = 1.0
    #kr = 2*np.pi/lambda_r
    #kr = 4.0
    _horizontal = horizontal(x,z,kr,_p,_q)
    _vertical = vertical(x,z,kr,_p,_q)
    import matplotlib.pyplot as plt
    fig, ax0 = plt.subplots(figsize=(6,7))
    ax0.plot(_horizontal,z,label='horizontal')
    ax0.plot(_vertical,z,label='vertical')
    ax0.hlines([0], -1, 4, "black", linestyles='--')
    ax0.vlines([0], -0.1, 2, "black", linestyles='--')
    ax0.set_ylim(-0.05,2)
    ax0.set_xlim(-1,4)
    ax0.legend()
    ax0.set_xticks(np.arange(-1,4.1,1))
    ax0.set_yticks(np.arange(0,2.1,0.2))
    ax0.invert_yaxis()
    ax0.grid(which='major',color='black',linestyle=':')
    ax0.set_xlabel('Amplitude [a.u.]')
    ax0.set_ylabel(r'Depth, $z/\lambda_{R}$')
    plt.savefig('RayleighWave_displacement_vs_depth.png')
    plt.close()
