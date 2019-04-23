from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np

start = tconvert('Apr 23 2019 13:50:00 JST')
end = tconvert('Apr 23 2019 13:50:01 JST')
# chname = [
#     'K1:GIF-X_ANGLE_IN1_DQ',
#     'K1:GIF-X_LAMP_IN1_DQ',
#     'K1:GIF-X_PHASE_IN1_DQ',
#     'K1:GIF-X_PPOL_IN1_DQ',
#     'K1:GIF-X_P_AMP_IN1_DQ',
#     'K1:GIF-X_P_OFFSET_IN1_DQ',
#     'K1:GIF-X_ROTATION_IN1_DQ',
#     'K1:GIF-X_SPOL_IN1_DQ',
#     'K1:GIF-X_STRAIN_IN1_DQ',
#     'K1:GIF-X_S_AMP_IN1_DQ',
#     'K1:GIF-X_S_OFFSET_IN1_DQ',
#     'K1:GIF-X_ZABS_IN1_DQ',
#     ]

chname = [
    'K1:GIF-X_PPOL_IN1_DQ',
    'K1:GIF-X_SPOL_IN1_DQ',
    ]
    
data = TimeSeriesDict.fetch(chname,start,end,
                            host='10.68.10.121',port=8088)

N = 128
# angle = data['K1:GIF-X_ANGLE_IN1_DQ']
# angle = angle.value[:N]
# angle = np.unwrap(angle)
# angle = np.rad2deg(angle)
ppol = data['K1:GIF-X_PPOL_IN1_DQ']
p_ave = np.average(ppol.value)
ppol = ppol.value[:N]
spol = data['K1:GIF-X_SPOL_IN1_DQ']
s_ave = np.average(spol.value)
spol = spol.value[:N]
time = np.arange(len(angle))/2048.0
print time

import matplotlib.pyplot as plt
if True:
    fig, ax = plt.subplots(1,1,figsize=(8,8),dpi=160)
    ax.plot(spol,ppol,'ko',markersize=1)
    ax.plot(spol[0],ppol[0],'ro',markersize=6,linewidth=2)    
    ax.set_xlabel('s [counts]')
    ax.set_ylabel('p [counts]')
    plt.savefig('Lissajous_hoge.png')
    plt.close()
    exit()

if True:
    phase = data['K1:GIF-X_PHASE_IN1_DQ'].value[:N]
    angle = data['K1:GIF-X_ANGLE_IN1_DQ'].value[:N]
    angle = angle - angle[0]
    rotation = data['K1:GIF-X_ROTATION_IN1_DQ']
    fig, ax = plt.subplots(1,1,figsize=(8,8),dpi=160)
    time = np.arange(len(angle))/2048.0
    func = lambda t: -2.0*np.pi*(34.0)*t
    _time = np.linspace(0,N,1000)/2048.0
    ax.plot(time,np.rad2deg(angle),'ro',markersize=3)    
    ax.plot(_time,np.rad2deg(func(_time)+angle[0]),'k-')    
    ax.set_yticks(np.arange(0,-721,-180))
    ax.set_xlabel('Time [sec]')
    ax.set_ylabel('Angle [degree]')
    ax.legend(['Result (K1:GIF-X\_ANGLE\_IN1\_DQ)','Expected'])
    plt.title('')
    plt.savefig('Angle.png')
    plt.close()    
