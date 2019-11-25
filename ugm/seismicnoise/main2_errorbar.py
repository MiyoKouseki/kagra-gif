from scipy.stats import chi,chi2
import numpy as np

def hoge(nu,alpha,asd=True,db=True):
    if not db:
        return nu/chi2.ppf([1-alpha/2,alpha/2],df=nu)
    if asd:        
        err_box = 20*np.log10(nu/chi2.ppf([1-alpha/2,alpha/2],df=nu))
    else:
        err_box = 10*np.log10(nu/chi2.ppf([1-alpha/2,alpha/2],df=nu))
        
    return err_box

nu = 32
alpha = 0.05
#print('PSD : {0:3.2f} dB, {1:3.2f}dB Peterson'.format(-2.14,2.87))
print('PSD : {0:3.2f} dB, {1:3.2f}dB Calc'.format(*hoge(nu,alpha,asd=False)))
print('ASD : {0:3.2f} dB, {1:3.2f}dB Calc'.format(*hoge(nu,alpha,asd=True)))

print('{0:3.2f}, {1:3.2f} Calc'.format(*hoge(nu,alpha,asd=False,db=False)))
