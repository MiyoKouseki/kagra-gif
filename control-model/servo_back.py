from scipy import signal
import numpy as np
from control import matlab

def servo(f0=0.1,f1=5,gain=5e3):
    w0 = 2.0*np.pi*f0
    w1 = 2.0*np.pi*f1
    num,den = signal.zpk2tf([-w0,-w0],[0,-w1],[gain])
    servo = matlab.tf(num,den)
    return servo
