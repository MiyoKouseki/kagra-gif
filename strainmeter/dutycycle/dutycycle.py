import numpy as np

_dc = [
      56.17, # 2017/01, OK
      72.90, # 2017/02, OK
      63.85, # 2017/03
      21.43, # 2017/04
      44.23, # 2017/05
      63.87, # 2017/06, OK
      38.62, # 2017/07
      14.51, # 2017/08
      30.75, # 2017/09
      24.00, # 2017/10, okashii
      57.82, # 2017/11
      48.32, # 2017/12      
      76.81, # 2018/01, OK
      97.93, # 2018/02, OK
      20.00, # 2018/03, OK
      80.59, # 2018/04
      82.23, # 2018/05 
      76.78, # 2018/06
      85.63, # 2018/07
      94.28, # 2018/08
      94.38, # 2018/09
      99.98, # 2018/10
      96.71, # 2018/11
      99.91, # 2018/12
      95.16, # 2019/01, OK
      89.76, # 2019/02, OK
      99.38, # 2019/03, OK
      99.85, # 2019/04
      99.88, # 2019/05
      99.95, # 2019/06
      99.97, # 2019/07
      99.88, # 2019/08
      99.31, # 2019/09
      99.94, # 2019/10
      92.37, # 2019/11 okashii
      99.85, # 2019/12 
      99.74, # 2020/01, OK
      99.74, # 2020/02, OK
      99.55, # 2020/03, OK
      96.70, # 2020/04
    ]

dc2017 = (np.array(_dc[0:12])).mean()
dc2018 = (np.array(_dc[12:24])).mean()
dc2019 = (np.array(_dc[24:36])).mean()

import matplotlib.pyplot as plt
time = range(len(_dc))
fig, ax = plt.subplots(1,1,figsize=(10,5))
ax.plot(time,_dc,'ko-',markersize=3,label='duty cycle per month')
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
plt.savefig('dutycycle.png')
plt.close()
