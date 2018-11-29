from astropy.units import Quantity
from astropy import units as u

c2V = 2.0*(10.0/2**15)

def v2temp(v,gif=False,**kwargs):
    if not v.unit == 'V':
        raise ValueError('!')
    if gif:
        ohm = v/10.0/(1.0+3300.0/430.0)/(0.001*u.A)
    else:
        ohm = v/78.0/(0.001*u.A)
        
    temp = (ohm-100.0*u.ohm)/(0.388*u.ohm/u.deg_C)
    return temp.decompose()


def v2humd(v,**kwargs):
    if not v.unit == 'V':
        raise ValueError('!')
    if v < 0.0:
        v = -v
    val = v/5.0/2.0*(100.0*u.pct/u.V)
    return val


def v2baro(v,**kwargs):
    if not v.unit == 'V':
        raise ValueError('!')
    if v < 0.0:
        v = -v        
    val = v/2.0/5.0*(1100.0-800.0)*(u.hPa/u.V)+800.0*u.hPa
    return val


x500 = {'temp':+8.92*u.V, # OK? 
        'humd':-9.43*u.V, # OK
        'baro':-5.96*u.V} # OK

x2000 = {'temp':+8.92*u.V, # OK?
         'humd':-1.3*u.V, # 
         'baro':+5.96*u.V} # OK
    
x500_sub = {'temp':8.37*u.V, # OK?
            'humd':4.66*u.V, # OK
            'baro':6.29*u.V} # OK

x500_sub_iy0 = {'temp':14170*c2V*u.V, # OK?
                'humd':5765*c2V*u.V, # OK
                'baro':9830*c2V*u.V} # OK
   
    
no4 = {'temp': 8.34*u.V, # OK?
       'humd': 12.9*u.V, # 
       'baro': 0.00*u.V} # 

no5 = {'temp':8.35*u.V, # OK?
       'humd':-3.92*u.V, # OK
       'baro':6.39*u.V} # OK

no5_iy0 = {'temp':14160*c2V*u.V, # OK?
           'humd':-5880*c2V*u.V, # OK
           'baro':9860*c2V*u.V} # OK
    

def printall(dict,**kwargs):
    print 'Temp : {0:+7.2f}'.format(v2temp(dict['temp'],**kwargs))
    print 'Humd : {0:+7.2f}'.format(v2humd(dict['humd'],**kwargs))
    print 'Baro : {0:+7.2f}'.format(v2baro(dict['baro'],**kwargs))

    
#print('x500')
#printall(x500,gif=True)

#printall(x2000)

#print('x500_sub')
#printall(x500_sub)

#print('no4')
#printall(no4)

#print('no5')
#printall(no5) 

print('no5_iy0')
printall(no5_iy0) 

print('x500_sub_iy0')
printall(x500_sub_iy0)



# remove
print v2temp(1e-2*c2V*u.V)
