from pykat import finesse
import matplotlib.pyplot as plt

kat = finesse.kat()
kat.verbose = False
kattext ='''
# optics configuration
m m1 0.9 0.0001 0 n1 n2     # mirror R=0.9, T=0.0001, phi=0
s s1 1200 n2 n3             # space L=1200m?
s s2 1 nn n1                # space L=1200m?
m m2 1 0 0 n3 dump          # mirror R=1 T=0 phi=0
l i1 1 0 n0                 # laser P=1W, f_offset=0Hz
mod eo1 40k 0.3 3 pm n0 nn  # phase modulator f_mod=40kHz
    	    	     	    # midx=0.3 order=3
pd1 inphase 40k 0 n1
pd1 quadrature 40k 90 n1

# output data 
xaxis m2 phi lin -90 90 400 
yaxis abs
'''
kat.parse(kattext)
for i in dir(kat):
    print i
out = kat.run()

fig, ax = plt.subplots(1, 1, figsize=(10,6), dpi=320)
print(out.y.shape)
plt.plot(out.x,out.y)
plt.title(r'Phase difference at the ITM')
plt.xlabel('tuning ETM [deg]')
plt.ylabel('phase difference [deg]')
plt.savefig('hoge.png')
