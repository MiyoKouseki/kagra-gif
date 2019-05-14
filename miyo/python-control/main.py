import scipy.io 
from control import matlab,tf
from control import StateSpace
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


mat_dict = scipy.io.loadmat("../TypeBp/linmod_typeBp.mat")
mat_dict = scipy.io.loadmat("../TypeBp/linmod.mat")
st = mat_dict['st']
A,B,C,D,statename,outputname,inputname,operpoint,ts = st[0][0]
ss = StateSpace(A, B, C, D)
#idx = np.where(C!=0)
#print C[idx]
#exit()
inputname = np.asarray([i[0][0] for i in inputname])
outputname = np.asarray([i[0][0] for i in outputname])
#print filter(lambda x:'LTM' in x,outputname)
start = 'TypeBp/actLTM'
start = 'TypeBp/accLGND'
end = 'TypeBp/OpLev_LTM'
idx_from = np.where(inputname==start)[0][0]
idx_to = np.where(outputname==end)[0][0]
print 'From :',idx_from,inputname[idx_from]
print 'To   :',idx_to,outputname[idx_to]

#out = ss.returnScipySignalLti()
#ss = out[idx_to][idx_from]
#print ss.C
#ss = ss.to_tf()
ss = matlab.ss2tf(A, B, C, D)
siso = ss.returnScipySignalLti()[idx_to][idx_from]
#print siso
#exit()
f = np.logspace(-2,2,1e6)
#w, mag, phase = bode(ss,f*2.0*np.pi,Plot=True)
w,mag, phase = signal.bode(siso,f*2.0*np.pi)
#exit()
mag = 10**(mag/20.0)
phase = np.rad2deg(np.unwrap(np.deg2rad(phase)))
#phase = np.deg2rad(phase)
#phase = np.unwrap(phase)
fig,(ax0,ax1) = plt.subplots(2,1)
f = w/2.0/np.pi
ax0.loglog(f,mag)
ax1.semilogx(f,phase)
ax0.set_xlim(1e-2,1e2)
ax1.set_xlim(1e-2,1e2)
ax0.set_ylim(9e-5,5e2)
ax1.set_ylim(-181,181)
ax1.set_yticks(range(-180,181,90))
plt.savefig('hoge.png')
plt.close()
