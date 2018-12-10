#
#! coding:utf-8
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from control import matlab
from scipy.signal import argrelmax

def H_compact(flat=True):
    ''' Trillium Compact TransferFunction

    Transfer function from Velocity to Voltage

    Retrun
    ------
    H : matlab.tf
    
    '''
    #
    if flat:
        return 749.1
    z = np.array([0, 0, -434.1]) # rad/sec
    p = np.array([-0.03691+0.03712j,
                -0.03691-0.03712j,
                -371.2,
                -373.9+475.5j,
                -373.9-475.5j,
                -588.4+1508j,
                -588.4-1508j])# rad/sec
    k = 8.184*10e11
    S = 1/(9.98243029518/749.1) # 749.1 at 1Hz
    num,den  = signal.zpk2tf(z,p,S*k)
    H  = matlab.tf(num,den)
    return H


def H_120QA(flat=True):
    ''' Trillium 120QA TransferFunction

    Transfer function from Velocity to Voltage.

    Retrun
    ------
    H : matlab.tf
    
    '''    
    if flat:
        return 1202.5
    z = np.array([0, 0, -31.63,-160,0350,03177]) # rad/sec
    p = np.array([-0.03661+0.037059j,
                -0.03661-0.037059j,
                -32.55,
                -142,
                -364+404j,
                -364-404j,
                -1260,
                -4900+5200j,
                -4900-5200j,
                -7100+1700j,
                -7100-1700j,])# rad/sec
    k = 8.3187*10e17
    S = 1*(1202.5/3.47045072616) # 1202.5 at 1Hz
    num,den  = signal.zpk2tf(z,p,S*k)
    H120  = matlab.tf(num,den)
    return H120

def readDiaggui_PSD(filename):
    ''' Read frequency data from Diaggui data with dat format.

    Parameter
    ---------
    filename : str
        filename you want to read data
    
        
    Return
    ------
    f : np.array
        Frequency.
    psd : array
        spectrum. it depend format you choise to export from diaggui.
    '''    
    data  = np.loadtxt(filename)
    f,psd = data[1:,0],data[1:,1]*c2V # remove 0 Value at 0 index.
    return f,psd


def V2Vel(f,Asd,trillium=None,flat=False):
    ''' Convert from Voltage to Velocity
        
    Parameter
    ---------
    f : np.array
        Frequency.
    asd : np.array
        Asd. not Psd.
    '''
    
    if trillium=='120QA':
        H = H_120QA(flat=flat)        
    elif trillium=='compact':
        H = H_compact(flat=flat)
    else:
        raise ValueError('Invalid trillium model name : {}'.format(trillium))
    
    mag, phase, omega = matlab.bode(1./H,f*(2.*np.pi),Plot=False,dB=False)
    Asd = Asd*mag
    return f,Asd


def selfnoise(trillium='120QA',psd='PSD',acc='acc'):
    '''
    
    Parameter
    ---------
    trillium : str
        model name of the trillium seismometer
    psd : str
        if PSD, return psd. if ASD, return asd. default is psd.
    acc : str
        if "acc", return acc. if "velo", return velocity, if "disp", 
        return displacement.

    Return 
    ------
    f : np.array
        Frequency
    selfnoise : np.array
        selfnoise spectrum. unit is depend what you choose.    
    '''
    if trillium=='compact':
        data = np.array([[1e-3,-145], # Freq [Hz], PSD (m/s^2)^2/Hz [dB]
                        [3e-3,-153],
                        [4e-2,-169],
                        [1e-1,-171],
                        [1e0, -175],
                        [3e0, -173],
                        [1e1, -166],
                        [2e1, -159],
                        [5e1, -145],
                        [5e2, -105]])
        f,selfnoise = data[:,0],data[:,1]  # PSD Acceleration with dB
        selfnoise     = 10**(selfnoise/10) # PSD Acceleration with Magnitude
    elif trillium=='120QA':
        data = np.array([[1e-3,-171], # Freq [Hz], PSD (m/s^2)^2/Hz [dB]
                        [3e-3,-179],
                        [1e-2,-184],
                        [3e-2,-188],
                        [1e-1,-189],
                        [2e-1,-188],
                        [1e0, -186],
                        [3e0, -182],
                        [1e1, -169],
                        [2e1, -158],
                        [2e2, -118]]) # fit 
        f,selfnoise = data[:,0],data[:,1] # PSD Acceleration with dB
        selfnoise = 10**(selfnoise/10) # PSD Acceleration with Magnitude
        
    if acc=='acc':
        f, selfnoise = f, selfnoise
    elif acc=='velo':
        f, selfnoise = f, selfnoise/(2.0*np.pi*f)**2
    elif acc=='disp':
        f, selfnoise = f, selfnoise/(2.0*np.pi*f)**4
    else:
        raise ValueError('!')
        
    if psd=='PSD':
        f, selfnoise = f, selfnoise
    elif psd=='ASD':
        f, selfnoise = f, np.sqrt(selfnoise)
    else:
        raise ValueError('psd {} didnt match PSD or ASD'.format(psd))        
        
    return f, selfnoise



def plot21_Trillium_TF(trillium='120QA',savefig=True):
    ''' Plot Transfer function of the Trillium seismometer
    
    Parameter
    ---------
    trillium : str
        model name of the trillium seismometer
    savefig : bool
        If true, save as image file. If False, do not save.              
    '''
    if trillium=='120QA':        
        H = H_120QA()
    elif trillium=='compact':
        H = H_compact()
    else:
        raise ValueError('invalid name of trillium seismometer model')
                    
    f = np.logspace(-3,3,1e4)
    mag, phase, w = matlab.bode(H,2.0*np.pi*f,Hz=True,deg=True,Plot=False)
    f = w/(2.0*np.pi)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, dpi=640)    
    plt.subplots_adjust(hspace=0.1,top=0.92)
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.suptitle('Frequency Response')

    ax1.loglog(f,mag,'k-',label='Trillium {0}'.format(trillium))
    ax1.set_ylim([1e0,5e3])
    ax1.grid(which='major',linestyle='-', linewidth=1)
    ax1.grid(which='minor',linestyle=':', linewidth=1)
    ax1.set_ylabel('Magnitude [V/(m/s)] ')
    ax1.legend(loc='lower right')
    ax1.yaxis.set_label_coords(-0.1,0.5)    
    ax2.semilogx(f,phase,'k-',label='Trillium {0}'.format(trillium))
    ax2.set_ylim([-200,200])
    ax2.grid(which='major',linestyle='-', linewidth=1)
    ax2.grid(which='minor',linestyle=':', linewidth=1)
    ax2.set_yticks(np.arange(-180,181,90))
    ax2.set_ylabel('Phase [Degree]')
    ax2.legend(loc='upper right')        
    ax2.yaxis.set_label_coords(-0.1,0.5)
    
    if savefig==False:
        pass
    else:
        plt.savefig('TF_Trillium_{}.png'.format(trillium))
        plt.close()       

    return fig,ax1,ax2


def plot_Trillium_Selfnoise(trillium='120QA',savefig=True,psd='PSD',acc='acc', **kwargs):
    ''' Plot Transfer function of the Trillium seismometer
    
    Parameter
    ---------
    trillium : str
        model name of the trillium seismometer
    savefig : bool
        If true, save as image file. If False, do not save.              
    '''

    if psd =='PSD':
        if acc == 'acc':
            unit = '(m/s/s)**2/Hz'
        elif acc == 'velo':
            unit = '(m/s)**2/Hz'
        elif acc == 'disp':
            unit = 'm**2/Hz'
        else:
            raise ValueError('Value error. acc : {}'.format(acc))    
    elif psd == 'ASD':
        if acc == 'acc':
            unit = '(m/s/s)/sqrtHz'
        elif acc == 'velo':
            unit = '(m/s)/sqrtHz'
        elif acc == 'disp':
            unit = 'm/sqrtHz'
        else:
            raise ValueError('Value error. acc : {}'.format(acc))            
    else:
        raise ValueError('Value error. psd : {}'.format(psd))

    f,mag = selfnoise(trillium=trillium,psd=psd,acc=acc)            
    fig, ax1 = plt.subplots(1, 1, sharex=True, dpi=640)    
    plt.subplots_adjust(hspace=0.1,top=0.92)
    #plt.setp(ax1.get_xticklabels(), visible=False)
    plt.suptitle('Selfnoise')

    ax1.loglog(f,mag,'k-',label='Trillium {0}'.format(trillium))
    ax1.set_ylim([1e-13,1e-5])
    ax1.grid(which='major',linestyle='-', linewidth=1)
    ax1.grid(which='minor',linestyle=':', linewidth=1)
            
    ax1.set_ylabel('{0} [{1}]'.format(psd,unit))
    ax1.set_xlabel('Frequency [Hz]')
    ax1.legend(loc='upper right')
    ax1.yaxis.set_label_coords(-0.1,0.5)    
    
    if savefig==False:
        pass
    else:
        plt.savefig('Selfnoise_Trillium_{}.png'.format(trillium))
        plt.close()       

    return fig,ax1


def main_Trillium_TF_ALL():
    fig, ax1, ax2 = plot21_Trillium_TF(trillium='compact',savefig=False)
    H = H_120QA()
    f = np.logspace(-3,3,1e4)
    mag, phase, w = matlab.bode(H,2.0*np.pi*f,Hz=True,deg=True,Plot=False)
    f = w/(2.0*np.pi)    
    ax1.loglog(f,mag,'b-',label='Trillium {0}'.format('120QA'))
    ax1.legend(loc='lower right')            
    ax2.semilogx(f,phase,'b-',label='Trillium {0}'.format('120QA'))
    ax2.legend(loc='upper right')            
    plt.savefig('TF_Trillium_ALL.png')
    plt.close()       

    
def main_Trillium_Selfnoise_ALL():
    fig, ax1 = plot_Trillium_Selfnoise(trillium='compact',savefig=False,
                                       psd='ASD',acc='disp')    
    f,mag = selfnoise(trillium='120QA',psd='ASD',acc='disp')    
    ax1.loglog(f,mag,'b-',label='Trillium {0}'.format('120QA'))
    ax1.legend(loc='upper right')            
    plt.savefig('Selfnoise_Trillium_ALL.png')
    plt.close()       
    
    
if __name__ == '__main__':
    plot21_Trillium_TF(trillium='compact')
    main_Trillium_TF_ALL()    
    plot_Trillium_Selfnoise(trillium='compact',psd='ASD',acc='disp')    
    main_Trillium_Selfnoise_ALL()
