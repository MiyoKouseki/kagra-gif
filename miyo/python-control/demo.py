#!/usr/bin/env python
import warnings
warnings.filterwarnings("ignore")

from control.matlab import *
from matplotlib import pyplot as plt
from scipy import signal

def main():
    '''
    This is 2input1output system.
    
    Input/Output    
    * Input1 : GND
    * Input2 : F
    * Output1 : OUTPUT
    
    '''
    k = 100.
    m = 1.    
    A = [[0., -k/m],[1., 0.]]
    B = [[k/m, 1/m], [0., 0.]]
    C = [[0., 1.0]]
    D = [[0.,0.]]
    sys1 = ss2tf(A, B, C, D)
    print sys1
    siso11 = sys1.returnScipySignalLti()[0][0] # [out][in]
    siso21 = sys1.returnScipySignalLti()[0][1] # [out][in]
    print siso11
    w = np.logspace(-2,2,1e4)
    w, mag, phase = signal.bode(siso11,w)    
    mag = 10**(mag/20.0)
    #phase = np.unwrap(phase)
    fig,(ax0,ax1) = plt.subplots(2,1)
    f = w/2.0/np.pi
    ax0.loglog(f,mag)
    ax1.semilogx(f,phase)
    ax0.set_xlim(1e-2,2e2)
    ax1.set_xlim(1e-2,2e2)
    ax1.set_ylim(-181,181)
    ax1.set_yticks(range(-180,181,90))    
    plt.savefig('demo.png')
    

if __name__ == "__main__":
  main()
