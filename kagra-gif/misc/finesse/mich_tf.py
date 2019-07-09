#
# Reference 
#  [1] https://gwdoc.icrr.u-tokyo.ac.jp/cgi-bin/DocDB/ShowDocument?docid=1669
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
fsig sig1 east-m 1000 0
fsig sig2 north-m 1000 180
pd2 GW 10M 0 1000 max nAS
xaxis sig1 f log 1 10k 100
put GW f2 $x1
scale meter
yaxis log abs
'''
kat.parse(kattext)
out = kat.run()
deg = out.x
asPD = out.y[:,1]
fig, ax = plt.subplots(1, 1, figsize=(10,6), dpi=320)
plt.loglog(deg,asPD)
#plt.plot(deg,asPD)
plt.title(r'Phase difference at the ITM')
plt.xlabel('tuning ETM [deg]')
plt.ylabel('phase difference [deg]')
plt.savefig('mich_tf.png')
