import scipy.io 
from control import matlab,tf
from control import StateSpace
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

mat_dict = scipy.io.loadmat("./linmod.mat")
st = mat_dict['st']
A,B,C,D,statename,outputname,inputname,operpoint,ts = st[0][0]
ss = StateSpace(A, B, C, D)

inputname = np.asarray([i[0][0] for i in inputname])
outputname = np.asarray([i[0][0] for i in outputname])
#print filter(lambda x:'LTM' in x,outputname)
start = 'TypeBp/actLTM'
end = 'TypeBp/OpLev_LTM'
idx_from = np.where(inputname==start)[0][0]
idx_to = np.where(outputname==end)[0][0]
print 'From :',idx_from,inputname[idx_from]
print 'To   :',idx_to,outputname[idx_to]


out = ss.returnScipySignalLti()
ss = out[idx_to][idx_from]
ss = ss.to_ss()

f = np.logspace(-2,2,1e5)
w, mag, phase = signal.bode(ss,f*2.0*np.pi)
mag = 10**(mag/20.0)
phase = np.unwrap(phase)
fig,(ax0,ax1) = plt.subplots(2,1)
f = w/2.0/np.pi
ax0.loglog(f,mag)
ax1.semilogx(f,phase)
ax0.set_xlim(1e-2,2e2)
ax1.set_xlim(1e-2,2e2)
ax1.set_ylim(-181,181)
ax1.set_yticks(range(-180,181,90))
plt.savefig('hoge.png')
plt.close()
