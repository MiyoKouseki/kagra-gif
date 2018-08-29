#
#! coding:utf-8

from miyopy.utils import readdump
import matplotlib.pyplot as plt
import numpy as np

n = 8
# JST 2018-08-27T00:00:00
tlen = 2**13
gst = 1219330818+tlen*n
get = gst+tlen

# JST 2018-08-28T00:00:00
#tlen = 2**13
#gst = 1219417218+tlen*n
#get = gst+tlen

chname1 = 'K1:PEM-EXV_SEIS_NS_SENSINF_INMON'
data1 = readdump(gst,get,chname1) # Count
nlen = len(data1)
fs = nlen/tlen
time1 = np.arange(nlen)/fs/60.0 # sec
print('nlen : {0}\n'\
      'tlen : {1}\n'\
      'fs : {2}'.format(nlen,tlen,fs))
      
chname2 = 'CALC_STRAIN'      
data2 = readdump(gst,get,chname2) # Count
nlen = len(data2)
fs = nlen/tlen
time2 = np.arange(nlen)/fs/60.0 # sec
print('nlen : {0}\n'\
      'tlen : {1}\n'\
      'fs : {2}'.format(nlen,tlen,fs))      

fname = '{0}_{1}.png'.format(gst,n)

fig , (ax0,ax1) =  plt.subplots(2,1,dpi=320, figsize=(10, 6))
plt.suptitle(fname)
ax0.plot(time1,data1,label=chname1)
ax0.legend(loc='upper right')
ax0.set_ylabel('Velocity [count]')
ax0.set_ylabel('Velocity [count]')
ax1.plot(time2,data2,label=chname2)
ax1.legend(loc='upper right')
ax1.set_xlabel('Time [minutes]')
ax1.set_ylabel('Strain')
#plt.
plt.savefig(fname)
plt.close()
