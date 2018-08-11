#
#! coding:utf-8

from miyopy.timeseries import TimeSeries
import matplotlib.pyplot as plt




def main(*args):
    t0,tlen,title = args
    strain = TimeSeries.read(t0,tlen,'CALC_STRAIN')
    p500 = TimeSeries.read(t0,tlen,'X500_BARO')
    plt.plot(strain.value)
    #plt.plot(p500.value)
    plt.savefig('hoge.png')
    #plot = p500.plot()
    #plot.savefig('hoge.png')    

    
def _main(*args):
    import numpy as np    
    data = np.loadtxt('./X1500_TR240velEW.csv',delimiter=' ')
    fs = 1./(data[0,1]-data[0,0])#*u.Hz
    t0 = data[0,0]#*u.s
    value = data[:,1]#*u.um/u.s
    name = 'huge'
    p500 = TimeSeries(value,t0=t0,dt=1.0/fs,name=name)
    print p500.name
    print type(p500)

    
if __name__ == '__main__':   
    t0 = 1209168018 # [UTC] 2018-05-01T00:00:00
    #t0 = 1206576018 # [UTC] 2018-04-01T00:00:00
    #t0 = 1203897618 # [UTC] 2018-03-01T00:00:00
    #t0 = 1201478418 # [UTC] 2018-02-01T00:00:00
    tlen = 3600#*24*1
    title = 'QuietMicroseimic'
    main(t0,tlen,title)
    #_main(t0,tlen,title)    
