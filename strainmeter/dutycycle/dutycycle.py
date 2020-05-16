import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.dates as mdates
from pandas import Timestamp as tsp
import matplotlib.pyplot as plt
import matplotlib as mpl

# ------------------------------------------------------------------------------

# load duty cycle per month
'''
v1 : 
    Absorption threshold : 200mV
    Fringe pk2pk threshold : 10mV
v2 : 
    Absorption threshold : 200mV
    Fringe pk2pk threshold : 3mV
'''
dc_v1 = pd.read_csv('./dutycycle_ver001.csv',
                    names=('date','total','laser','fringe'),
                    header=0,delimiter=',',
                    dtype={0:str,1:float,2:float,3:float},
                    parse_dates=[0])
dc_v2 = pd.read_csv('./dutycycle_ver002.csv',
                    names=('date','total','laser','fringe'),
                    header=0,delimiter=',',
                    dtype={0:str,1:float,2:float,3:float},
                    parse_dates=[0])

# calc duty cycle per year
dc2017_v1 = dc_v1[(dc_v1['date']>=dt.datetime(2017,1,1))
               & (dc_v1['date']<dt.datetime(2018,1,1))]
dc2018_v1 = dc_v1[(dc_v1['date']>=dt.datetime(2018,1,1))
               & (dc_v1['date']<dt.datetime(2019,1,1))]
dc2019_v1 = dc_v1[(dc_v1['date']>=dt.datetime(2019,1,1))
               & (dc_v1['date']<dt.datetime(2020,1,1))]
mean17_v1 = dc2017_v1['total'].mean()
mean18_v1 = dc2018_v1['total'].mean()
mean19_v1 = dc2019_v1['total'].mean()

dc2017_v2 = dc_v2[(dc_v2['date']>=dt.datetime(2017,1,1))
               & (dc_v2['date']<dt.datetime(2018,1,1))]
dc2018_v2 = dc_v2[(dc_v2['date']>=dt.datetime(2018,1,1))
               & (dc_v2['date']<dt.datetime(2019,1,1))]
dc2019_v2 = dc_v2[(dc_v2['date']>=dt.datetime(2019,1,1))
               & (dc_v2['date']<dt.datetime(2020,1,1))]
mean17_v2 = dc2017_v2['total'].mean()
mean18_v2 = dc2018_v2['total'].mean()
mean19_v2 = dc2019_v2['total'].mean()


# setting
fig, ax = plt.subplots(1,1,figsize=(10,5))
mpl.rcParams['lines.markersize'] = 3
ax.set_ylim(0,105)
ax.set_xlim(tsp('2017-01'), tsp('2020-05'))
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.grid('on',which='major',linestyle='-',color='gray')
ax.grid('on',which='minor',linestyle=':',color='gray')
ax.set_xlabel('Date [Month]')
ax.set_ylabel('Duty cycle [%]')
fname = 'dutycycle.png'

# plot
ax.plot(dc_v2['date'],dc_v2['laser'],'go-',label='Laser')
ax.plot(dc_v2['date'],dc_v2['fringe'],'bo-',label='Fringe')
ax.plot(dc_v2['date'],dc_v2['total'],'ro-',label='Total')
ax.plot(dc_v1['date'],dc_v1['total'],'o--',color='gray',alpha=0.5)

# hlines
kwargs = {'color':'red', 'linestyle':'--', 'alpha':1}
ax.hlines(mean17_v2,tsp('2017-01'),tsp('2018-01'),**kwargs)
ax.hlines(mean18_v2,tsp('2018-01'),tsp('2019-01'),**kwargs)
ax.hlines(mean19_v2,tsp('2019-01'),tsp('2020-01'),**kwargs)
kwargs = {'color':'gray', 'linestyle':'--', 'alpha':0.5}
ax.hlines(mean17_v1,tsp('2017-01'),tsp('2018-01'),**kwargs)
ax.hlines(mean18_v1,tsp('2018-01'),tsp('2019-01'),**kwargs)
ax.hlines(mean19_v1,tsp('2019-01'),tsp('2020-01'),**kwargs)

# text
bbox = {'facecolor':'white', 'alpha':1,"edgecolor" : "black",
        'boxstyle':'round','pad':0.15}
kwargs = {'color':'black','bbox':bbox,
          'verticalalignment':'bottom','alpha':1,
          'horizontalalignment':'right'}
ax.text(tsp('2018-01'),mean17_v2-1,'{0:3.1f}'.format(mean17_v2),**kwargs)
ax.text(tsp('2019-01'),mean18_v2-1,'{0:3.1f}'.format(mean18_v2),**kwargs)
ax.text(tsp('2020-01'),mean19_v2-1,'{0:3.1f}'.format(mean19_v2),**kwargs)

bbox = {'facecolor':'white', 'alpha':0.5,"edgecolor" : "gray",
        'boxstyle':'round','pad':0.15}
kwargs = {'color':'gray','bbox':bbox,
          'verticalalignment':'top','alpha':0.5,
          'horizontalalignment':'right'}
ax.text(tsp('2018-01'),mean17_v1-1,'{0:3.1f}'.format(mean17_v1),**kwargs)
ax.text(tsp('2019-01'),mean18_v1-1,'{0:3.1f}'.format(mean18_v1),**kwargs)
ax.text(tsp('2020-01'),mean19_v1-1,'{0:3.1f}'.format(mean19_v1),**kwargs)

# save
ax.legend(loc='lower right')
plt.savefig(fname)
plt.close()

