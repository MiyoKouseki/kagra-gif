#
#! coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

c2V_dd = 20.0/2**16 # differential -> differential
c2V_sd = c2V_dd*2.0 # single-end -> diferential
func_temp2ohm = lambda x,a,b: a*x+b
func_ohm2inv = lambda y: (y-100.0)/0.388 # Fitting Result


def V2humi(V):
    humi = V/2.0/5.0*100.0
    print "{0:6.2f} %".format(humi)
    return humi

def V2baro(V):
    baro = V/2.0/5.0*(1100-800)+800
    print "{0:6.2f} Pa".format(baro)
    return baro

def V2temp(V,unit='ohm'):
    ohm = V/0.001/78.0
    if unit=='ohm':
        temp = ohm
    else:
        #temp = (V/0.001/78.0-107.79)/0.388+20.0
        temp = func_ohm2inv(ohm)
    print "{0:6.2f} Degree".format(temp)
    return temp

def main():
    print 'baro',9565*c2V_sd
    print 'humi',13200*c2V_sd
    print 'temp',14072*c2V_sd
    print '-------'
    baro = V2baro(9628*c2V_sd)
    humi = V2humi(7360*c2V_sd)
    temp = V2temp(14180*c2V_sd,unit='Degree')


def Pt100():
    data = np.loadtxt('./pt100.txt')
    temp,ohm = data[:,0],data[:,1]
    param, cov = curve_fit(func_temp2ohm,temp,ohm)
    print param
    plt.plot(temp,ohm,'o')
    plt.plot(temp,func_temp2ohm(temp,*param),'-')
    plt.title('Pt100')
    plt.xlabel('Temperature [Degree Celsius]')
    plt.ylabel('Resistance [Ohm]')
    plt.savefig('pt100.png')
    plt.close()

if __name__=='__main__':    
    main()
    #Pt100()


