from sympy import *
import numpy as np
'''
Reference

    [1] Takemoto, Shuzo, et al. "A 100 m laser strainmeter system in the Kamioka Mine, Japan, for precise observations of tidal strains." Journal of Geodynamics 41.1-3 (2006): 23-29.
'''


def _alpha(_nu):
    ''' Calc C_R/C_S

    Equation comes from eq 1.37 on M. Beker Ph.D thesis.

    Parameter
    ---------
    _nu : float
        poisson ratio

    Return
    ------
    ans : float
        C_R/C_S, where C_R is velocity of Rayliegh wave, C_S is that of sencondary wave.
    '''
    x=Symbol('x')
    nu=Symbol('nu')
    _ans = solve(x**3 - 8.0*x**2 + 8.0*(2.0-nu)/(1.0-nu)*x - 8.0/(1.0-nu) ,x)
    ans = [ a.evalf(subs={nu:_nu}) for a in _ans ]
    ans = np.fromiter(ans, dtype=complex)    
    ans = np.sqrt(ans).real
    return ans[0]


def _beta(_nu):
    ''' Calc C_P/C_S
   
    Equation comes from eq 1.31 on M. Beker Ph.D thesis.

    Parameter
    ---------
    _nu : float
        poisson ratio
    
    Return
    ------
    x : float
        C_P/C_S, where C_P is velocity of primary wave, C_S is that of sencondary wave.
    '''
    return (2.0-2.0*_nu)/(1.0-2.0*_nu)


def _q(alpha,beta):
    '''
    q = sqrt(1-(C_R/C_P)**2)
    '''
    
    return np.sqrt(1.0-(alpha/beta)**2)

def _p(alpha):
    '''
    q = sqrt(1-(C_R/C_S)**2)
    '''    
    return np.sqrt(1.0-alpha**2)


def _horizontal(z,nu):
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
    alpha = _alpha(nu)
    beta = _beta(nu)
    p = _p(alpha)
    q = _q(alpha,beta)    
    return 1*( np.exp(-q*2.0*np.pi*z) - 2.0*q*p/(1+p**2)*np.exp(-p*2.0*np.pi*z) )
           
def _vertical(z,nu):
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
    alpha = _alpha(nu)
    beta = _beta(nu)
    p = _p(alpha)
    q = _q(alpha,beta)
    return -1*q*( np.exp(-q*2.0*np.pi*z) - 2.0/(1+p**2)*np.exp(-p*2.0*np.pi*z) )


    
if __name__ == '__main__':
    # --------------    
    # Poisson ratio
    # --------------
    # [1] 2003, Installation of 100 m laser strainmeters in the Kamioka Mine.
    nu = 0.283 # [1]

    
    # --------------
    # calc velocity
    # ---------------    
    alpha = _alpha(nu)
    beta = _beta(nu)
    cp = 5.5e3
    cs = cp/np.sqrt(beta)
    cr = cp*np.sqrt(alpha/beta)
    print 'Velocity'
    print ' Cp:{0:3.0f} m/s\n Cs:{1:3.0f} m/s\n Cr:{2:3.0f} m/s'.format(cp,cs,cr)

    
    # ----------------------
    # plot depth dependance
    # ----------------------    
    z = np.linspace(0,2,100) # normarized depth: z/lambda_r
    horizontal = _horizontal(z,nu)
    vertical = _vertical(z,nu)    
    import matplotlib.pyplot as plt
    fig, ax0 = plt.subplots(figsize=(5,6))
    ax0.plot(horizontal,z,'k',label='Horizontal displacement')
    ax0.plot(vertical,z,'k--',label='Vertical displacement')
    ax0.legend(loc='lower right')
    ax0.set_xticks(np.arange(-0.5,1.1,0.5))
    ax0.set_yticks(np.arange(0,2.1,0.5))
    ax0.set_ylim(-0.05,2)
    ax0.set_xlim(-0.5,1.0)    
    ax0.invert_yaxis()
    ax0.grid(which='major',color='black',linestyle=':')
    ax0.set_xlabel('Amplitude',fontsize=12)
    ax0.set_ylabel(r'Depth, $z/\lambda_{R}$',fontsize=12)
    plt.savefig('RayleighWave_displacement_vs_depth.png')
    plt.close()


    # ----------------------
    # plot depth dependance
    # ----------------------
    z0 = 200.0
    z = np.logspace(-4,1,1000) # normarized depth: z/lambda_r
    horizontal = _horizontal(z,nu)
    vertical = _vertical(z,nu)    
    import matplotlib.pyplot as plt
    fig, ax0 = plt.subplots(figsize=(8,6))
    ax0.loglog(z*(cr/z0),abs(horizontal/vertical),'k')
    ax0.legend(loc='lower right')
    ax0.grid(which='major',color='black',linestyle=':')
    ax0.set_ylabel('H/V',fontsize=12)
    ax0.set_xlabel(r'Frequency [Hz]',fontsize=12)
    ax0.set_ylim(1e-3,1)
    ax0.set_xlim(1e-3,1e2)    
    plt.savefig('HV_Ratio.png')
    plt.close()
    
