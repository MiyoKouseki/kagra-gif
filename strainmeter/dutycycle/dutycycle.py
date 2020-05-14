import numpy as np


_dc = [
    ('2017/01', 56.17, 64.44, 56.32),
    ('2017/02', 72.90, 99.64, 73.02),
    ('2017/03', 63.85, 99.38, 63.87),
    ('2017/04', 21.43, 99.79, 21.44),
    ('2017/05', 44.23, 99.64, 44.25),
    ('2017/06', 63.87, 90.48, 65.77),
    ('2017/07', 38.62, 95.58, 38.99),
    ('2017/08', 14.51, 99.98, 14.53),
    ('2017/09', 30.75, 98.84, 30.84),
    ('2017/10', 29.72, 86.54, 30.13),
    ('2017/11', 57.82, 80.47, 58.46),
    ('2017/12', 48.32, 90.55, 49.20),
    ('2018/01', 76.81, 99.87, 76.85),
    ('2018/02', 97.93, 99.98, 97.93),
    ('2018/03', 20.00, 99.53, 20.00),
    ('2018/04', 80.59, 99.80, 80.59),
    ('2018/05', 82.23, 99.87, 82.23),
    ('2018/06', 76.78, 99.37, 76.79),
    ('2018/07', 85.63, 99.76, 85.64),
    ('2018/08', 94.28, 98.94, 95.11),
    ('2018/09', 94.38, 94.58, 95.59),
    ('2018/10', 99.98, 99.98, 100.00),
    ('2018/11', 96.71, 99.99, 96.72),
    ('2018/12', 99.91, 99.91, 99.94),
    ('2019/01', 95.16, 97.71, 95.30),
    ('2019/02', 89.76, 99.97, 89.79),
    ('2019/03', 99.38, 99.38, 99.43),
    ('2019/04', 99.85, 99.85, 99.92),
    ('2019/05', 99.88, 99.88, 99.93),
    ('2019/06', 99.95, 99.95, 100.00),
    ('2019/07', 99.97, 99.97, 100.00),
    ('2019/08', 99.88, 99.88, 99.95),
    ('2019/09', 99.31, 99.31, 99.69),
    ('2019/10', 99.94, 99.94, 99.96),
    ('2019/11', 92.37, 99.37, 99.96),
    ('2019/12', 99.85, 99.85, 100.00),
    ('2020/01', 99.74, 99.74, 100.00),
    ('2020/02', 99.74, 99.74, 100.00),
    ('2020/03', 99.55, 99.55, 99.96),
    ('2020/04', 96.70, 99.94, 96.76)]
    
dt = np.dtype([('date','|S10'),('dc','<f8'),('dc1','<f8'),('dc2','<f8')])
_dc1 = np.array(_dc,dtype=dt)['dc1']
_dc2 = np.array(_dc,dtype=dt)['dc2']
_dc = np.array(_dc,dtype=dt)['dc']
dc2017 = (np.array(_dc[0:12])).mean()
dc2018 = (np.array(_dc[12:24])).mean()
dc2019 = (np.array(_dc[24:36])).mean()

import matplotlib.pyplot as plt
time = range(len(_dc))
fig, ax = plt.subplots(1,1,figsize=(10,5))

total = True
if not total:
    ax.plot(time,_dc,'ko-',markersize=3,label='Total')
    ax.plot(time,_dc1,'go--',markersize=3,label='Laser')
    ax.plot(time,_dc2,'bo--',markersize=3,label='Contrast')
    fname = 'dutycycle_budget.png'    
else:
    ax.plot(time,_dc,'ko-',markersize=3,linewidth=2,label='Duty cycle per month')    
    ax.hlines(dc2017,0,12,color='r',linestyle='--')
    bbox=dict(facecolor='white', alpha=0.9,boxstyle='round',pad=0.1)
    ax.text(12,dc2017-1,'{0:3.1f}'.format(dc2017),color='red',
            verticalalignment='top',horizontalalignment='right',bbox=bbox)
    ax.hlines(dc2018,12,24,color='r',linestyle='--')
    ax.text(24,dc2018-1,'{0:3.1f}'.format(dc2018),color='red',
            verticalalignment='top',horizontalalignment='right',bbox=bbox)
    ax.hlines(dc2019,24,36,color='r',linestyle='--',
            label='Average per year')
    ax.text(36,dc2019-1,'{0:3.1f}'.format(dc2019),color='red',
            verticalalignment='top',horizontalalignment='right',bbox=bbox)
    fname = 'dutycycle_total.png'
ax.set_ylim(0,100)
ax.set_xlim(0,42)
ax.legend(loc='lower right')
ax.set_yticks([0,25,50,75,100],minor=False)
ax.set_yticks(range(0,100,5),minor=True)
ax.set_xticks([0,12,24,36,48],minor=False)
ax.set_xticks(range(48),minor=True)
ax.grid(which='major',linestyle='--',color='k')
ax.grid(which='minor',linestyle=':')
ax.set_xticklabels([0,25,50,75,100],
                   minor=False)
ax.set_xticklabels(['2017/01','2018/01','2019/01','2020/01','2021/01'],
                   minor=False)
ax.set_xlabel('Date [Month]')
ax.set_ylabel('Duty cycle [%]')
#ax.set_ylabel([])
plt.savefig(fname)
plt.close()
