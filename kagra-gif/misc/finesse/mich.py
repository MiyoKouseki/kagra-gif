#
# Reference 
#  [1] https://gwdoc.icrr.u-tokyo.ac.jp/cgi-bin/DocDB/ShowDocument?docid=1669
import numpy as np
from pykat import finesse
import matplotlib.pyplot as plt

kat = finesse.kat()
kat.verbose = False
kattext ='''
l i1 100 0 nL 
s sEOM 1 nL nEOin
mod eo1 10M 0.1 2 pm 0 nEOin nEOout
s sRE 1 nEOout nPOin
bs po 0 1 0 45 nPOin dump nPOout npo
s sBS 1 nPOout n1
bs bs1 0.5 0.5 0 45 n1 n2 n3 n4
s sAS 1 n4 nAS
s north-s 3000 n2 n5
s east-s 3001 n3 n6
m north-m 0.99995 50e-6 0 n5 n7
m east-m 0.99995 50e-6 90 n6 n8
pd1 Ctrl 10M 90 nAS
xaxis north-m phi lin -180 180 400
func y = 90-$x1
put* east-m phi $y # 
noplot y
yaxis lin abs
'''
kat.parse(kattext)
out = kat.run()
deg = out.x
asPD = out.y[:,0]
fig, ax = plt.subplots(1, 1, figsize=(10,6), dpi=320)
plt.plot(deg,asPD)
plt.xticks(np.arange(-90,91,45))
plt.xlim(-90,90)
plt.title('')
plt.legend(['AS (Q)'])
plt.xlabel('tuning DARM [deg]')
plt.ylabel('Abs')
plt.grid(b=None, which='both', axis='both', linestyle='--')
plt.savefig('mich.png')
