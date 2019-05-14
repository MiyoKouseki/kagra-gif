#!/usr/bin/env python
import warnings
warnings.filterwarnings("ignore")

from control.matlab import *
from matplotlib import pyplot as plt


def main():
    '''
    https://qiita.com/nnn_anoken/items/3604156086351a07e860
    '''
    k1 = 3.0
    m1 = 0.1
    c1 = 0.01
    k2 = 3.0
    m2 = 0.1
    c2 = 0.01
    A = [[0., 1,0,0], [-(k1+k2)/m1, -(c1+c2)/m1,k2/m1,c2/m1],[0., 0,0,1],
        [-k2/m2,c2/m2,-k2/m2,-c2/m2] ]
    B = [[0.], [0.], [0.], [1./m2]]
    C = [[0,0,1., 0.0]]
    D = [[0.]]
    sys1 = ss2tf(A, B, C, D)
    print sys1
    omega = np.logspace(-0,2,1e4)
    print dir(sys1)
    mag, phase, omega = bode(sys1,omega,Plot=True)
    plt.savefig('qiita_2dof.png')
    

if __name__ == "__main__":
  main()
