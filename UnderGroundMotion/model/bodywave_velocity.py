#
#! coding:utf-8
from astropy import units as u
from numpy import sqrt


'''
Reference
[1] 竹本修三, et al. "神岡鉱山における 100 メートルレーザー伸縮計について." (2003).

'''
lam = 3.27e11*u.dyn/u.cm**2 
mu = 2.51e11*u.dyn/u.cm**2
rho = 2.7*u.g/u.cm**3

vL = sqrt((lam+2*mu)/rho)
vT = sqrt((mu)/rho)

print '{0:7.1f}'.format(vL.si)
print '{0:7.1f}'.format(vT.si)
