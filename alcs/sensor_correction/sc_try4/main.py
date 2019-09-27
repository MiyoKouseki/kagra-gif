import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.frequencyseries import FrequencySeries
import numpy as np

on = True
plot_prs = False
plot_seiscomm = True
plot_acccomm = False
plot_accdiff = False
plot_seisdiff = True
plot_rms = True
plot_gif = True
plot_xarm = True
plot_simu = True
plot_coherence = True

channels = [
    'K1:GIF-X_STRAIN_OUT16',
    'K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16',
    'K1:PEM-SEIS_EXV_GND_X_OUT16',
    'K1:PEM-SEIS_IXV_GND_X_OUT16',
    'K1:VIS-PR3_TM_OPLEV_SERVO_YAW_OUT16',
    'K1:VIS-PR2_TM_OPLEV_SERVO_YAW_OUT16',
    # 'K1:VIS-ETMX_IP_ACCINF_H1_OUT16',
    # 'K1:VIS-ETMX_IP_ACCINF_H2_OUT16',
    # 'K1:VIS-ETMX_IP_ACCINF_H3_OUT16',
    # 'K1:VIS-ETMX_IP_ACC2EUL_1_1',
    # 'K1:VIS-ETMX_IP_ACC2EUL_1_2',
    # 'K1:VIS-ETMX_IP_ACC2EUL_1_3',
    # 'K1:VIS-ETMX_IP_ACC2EUL_2_1',
    # 'K1:VIS-ETMX_IP_ACC2EUL_2_2',
    # 'K1:VIS-ETMX_IP_ACC2EUL_2_3',
    # 'K1:VIS-ITMX_IP_ACCINF_H1_OUT16',
    # 'K1:VIS-ITMX_IP_ACCINF_H2_OUT16',
    # 'K1:VIS-ITMX_IP_ACCINF_H3_OUT16',
    # 'K1:VIS-ITMX_IP_ACC2EUL_1_1',
    # 'K1:VIS-ITMX_IP_ACC2EUL_1_2',
    # 'K1:VIS-ITMX_IP_ACC2EUL_1_3',
    # 'K1:VIS-ITMX_IP_ACC2EUL_2_1',
    # 'K1:VIS-ITMX_IP_ACC2EUL_2_2',
    # 'K1:VIS-ITMX_IP_ACC2EUL_2_3',
    'K1:VIS-ETMX_IP_DAMP_L_OUT16',
    'K1:VIS-ETMX_IP_DAMP_Y_OUT16',    
    'K1:VIS-ETMX_IP_SUMOUT_L_OUT16',
    'K1:VIS-ETMX_IP_SUMOUT_T_OUT16',
    'K1:VIS-ETMX_BF_LVDTEUL_L_INMON',
    'K1:VIS-ETMX_BF_LVDTEUL_T_INMON',    
    # 'K1:VIS-ETMX_F0_SUMOUT_GAS_OUT16',
    # 'K1:VIS-ETMX_F1_SUMOUT_GAS_OUT16',
    # 'K1:VIS-ETMX_F2_SUMOUT_GAS_OUT16',
    # 'K1:VIS-ETMX_F3_SUMOUT_GAS_OUT16',
    # 'K1:VIS-ETMX_BF_SUMOUT_GAS_OUT16',
    'K1:VIS-ITMX_IP_DAMP_L_OUT16',
    'K1:VIS-ITMX_IP_DAMP_Y_OUT16',        
    'K1:VIS-ITMX_IP_SUMOUT_L_OUT16',
    'K1:VIS-ITMX_IP_SUMOUT_T_OUT16',
    'K1:VIS-ITMX_BF_LVDTEUL_L_INMON',
    'K1:VIS-ITMX_BF_LVDTEUL_T_INMON',        
    ]

#                H1,     H2,     H3,
etmx_acc_mat = [[ 0.6500,-0.1483,-0.4185], # L
                [-0.0099,-0.5598, 0.9110], # T
                [ 0.8679, 0.4580, 1.0462],] # Y
etmx_acc_mat = np.array(etmx_acc_mat)
# 
#                H1,     H2,     H3,
itmx_acc_mat = [[ 0.5152,-0.1943,-0.3234], # L 
                [ 0.0858,-0.4984, 0.4062], # T
                [ 0.5617, 0.5664, 0.5876],] # Y
itmx_acc_mat = np.array(itmx_acc_mat)    
if on:
    # 1st 
    start = 'Sep 24 2019 21:55:00 JST'  
    end   = 'Sep 24 2019 22:05:00 JST'
    # 2nd Notch210mHz at ETMX MN P12
    start = 'Sep 24 2019 23:20:00 JST'  
    end   = 'Sep 25 2019 00:10:00 JST'
    # 3d Notch210mHz at ETMX BF YAW
    start = 'Sep 25 2019 00:11:00 JST'  
    end   = 'Sep 25 2019 00:38:00 JST'
    # 4th Update P12
    start = 'Sep 25 2019 00:53:00 JST'  
    end   = 'Sep 25 2019 01:03:00 JST'
    # 5th
    start = 'Sep 25 2019 01:15:00 JST'
    end   = 'Sep 25 2019 01:40:00 JST'
    onoff = 'ON'
    #total = FrequencySeries.read('../vismodel/total_wsc.hdf5')
    #total = 1
    total = FrequencySeries.read('../vismodel/total_wosc.hdf5')
else: # OFF
    # 
    start = 'Sep 24 2019 22:08:00 JST'  
    end   = 'Sep 24 2019 22:18:00 JST'
    #start = 'Sep 24 2019 22:42:00 JST'  
    #end   = 'Sep 24 2019 22:52:00 JST'        
    onoff = 'OFF'
    total = FrequencySeries.read('../vismodel/total_wosc_1.0.hdf5')
    total = FrequencySeries.read('../vismodel/total_wosc_1.4.hdf5')

    
# setting
fftlen = 2**6
ovlp = fftlen/2.0

def timeseries(start,end,plot=True):
    kwargs = {'verbose':True,'host':'10.68.10.121','port':8088}
    #kwargs = {'verbose':True,'host':'localhost','port':8088}
    data = TimeSeriesDict.fetch(channels,start,end,**kwargs)
    c = 299792458 # m/sec
    lam = 1064e-9 # m
    gif = data['K1:GIF-X_STRAIN_OUT16']*3000*1e6
    xarm = data['K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16']*3000.0/(c/lam)*1e6 # [um]
    # Seismometer
    etmx_seis = data['K1:PEM-SEIS_EXV_GND_X_OUT16']
    itmx_seis = data['K1:PEM-SEIS_IXV_GND_X_OUT16']
    diff_seis = etmx_seis - itmx_seis
    comm_seis = etmx_seis + itmx_seis
    # # ACC
    # etmx_acc_h1 = data['K1:VIS-ETMX_IP_ACCINF_H1_OUT16']
    # etmx_acc_h2 = data['K1:VIS-ETMX_IP_ACCINF_H2_OUT16']
    # etmx_acc_h3 = data['K1:VIS-ETMX_IP_ACCINF_H3_OUT16']
    # P = etmx_acc_mat    
    # etmx_acc_l = P[0][0]*etmx_acc_h1 + P[0][1]*etmx_acc_h2 + P[0][2]*etmx_acc_h3 # L
    # etmx_acc_t = P[1][0]*etmx_acc_h1 + P[1][1]*etmx_acc_h2 + P[1][2]*etmx_acc_h3 # T
    # itmx_acc_h1 = data['K1:VIS-ITMX_IP_ACCINF_H1_OUT16']
    # itmx_acc_h2 = data['K1:VIS-ITMX_IP_ACCINF_H2_OUT16']
    # itmx_acc_h3 = data['K1:VIS-ITMX_IP_ACCINF_H3_OUT16']
    # P = itmx_acc_mat 
    # itmx_acc_l = P[0][0]*itmx_acc_h1 + P[0][1]*itmx_acc_h2 + P[0][2]*itmx_acc_h3 # L
    # itmx_acc_t = P[1][0]*itmx_acc_h1 + P[1][1]*itmx_acc_h2 + P[1][2]*itmx_acc_h3 # T
    # diff_acc_l = etmx_acc_l + itmx_acc_l
    # diff_acc_t = etmx_acc_t + itmx_acc_t
    # print np.abs(etmx_acc_mat[0,:]).sum()
    # IP ACT
    etmx_act_l = data['K1:VIS-ETMX_IP_DAMP_L_OUT16']
    itmx_act_l = data['K1:VIS-ITMX_IP_DAMP_L_OUT16']
    diff_act_l = - etmx_act_l - itmx_act_l
    diff_acc_l = diff_act_l
    #diff_acc_l = etmx_act_l
    # GAS ACT
    #etmx_gas_f0 = data['K1:VIS-ETMX_F0_SUMOUT_GAS_OUT16']
    #diff_acc_l = etmx_gas_f0
    #
    #pr3 = data['K1:VIS-PR3_TM_OPLEV_SERVO_YAW_OUT16'
    #pr2 = data['K1:VIS-PR3_TM_OPLEV_SERVO_YAW_OUT16']        
    pr3 = data['K1:VIS-ETMX_IP_DAMP_Y_OUT16']
    pr2 = data['K1:VIS-ITMX_IP_DAMP_Y_OUT16']

    if plot:
        plt.plot(gif)
        plt.savefig('timeseries.png')
        plt.close()
    return gif,xarm,diff_seis,comm_seis,diff_acc_l,pr3,pr2

# def coherence(gif,xarm,diff_seis,comm_seis,fftlen=2**8,ovlp=2**7):
#     coh_gif2xarm = gif.coherence(xarm,fftlength=fftlen,overlap=ovlp)
#     coh_gif2seis = gif.coherence(diff_seis,fftlength=fftlen,overlap=ovlp)
#     coh_xarm2seiscomm = xarm.coherence(comm_seis,fftlength=fftlen,overlap=ovlp)
#     return coh_gif2xarm,coh_gif2seis,coh_xarm2seiscomm


def asd(gif,xarm,diff_seis,comm_seis,pr3,pr2,diff_acc,fftlen=2**8,ovlp=2**7):
    gif = gif.asd(fftlength=fftlen,overlap=ovlp)
    xarm = xarm.asd(fftlength=fftlen,overlap=ovlp)
    diff_seis = diff_seis.asd(fftlength=fftlen,overlap=ovlp)    
    comm_seis = comm_seis.asd(fftlength=fftlen,overlap=ovlp)
    diff_acc = diff_acc.asd(fftlength=fftlen,overlap=ovlp)
    pr3 = pr3.asd(fftlength=fftlen,overlap=ovlp)
    pr2 = pr2.asd(fftlength=fftlen,overlap=ovlp)
    w = 2.0*np.pi*(diff_seis.frequencies.value)
    diff_seis = diff_seis/w
    comm_seis = comm_seis/w
    diff_acc = diff_acc/w
    return gif,xarm,diff_seis,comm_seis,diff_acc,pr3,pr2


# simulation

# Timeseries
gif,xarm,diff_seis,comm_seis,diff_acc,pr3,pr2 = timeseries(start,end)

# Coherence
coh_gif2xarm = gif.coherence(xarm,fftlength=fftlen,overlap=ovlp)
coh_gif2diff = gif.coherence(diff_seis,fftlength=fftlen,overlap=ovlp)
coh_gif2comm = gif.coherence(comm_seis,fftlength=fftlen,overlap=ovlp)
coh_xarm2seiscomm = xarm.coherence(comm_seis,fftlength=fftlen,overlap=ovlp)
coh_xarm2seisdiff = xarm.coherence(diff_seis,fftlength=fftlen,overlap=ovlp)
coh_xarm2accdiff = xarm.coherence(diff_acc,fftlength=fftlen,overlap=ovlp)
coh_xarm2pr3 = xarm.coherence(pr3,fftlength=fftlen,overlap=ovlp)
coh_xarm2pr2 = xarm.coherence(pr2,fftlength=fftlen,overlap=ovlp)

# ASD
gif,xarm,diff_seis,comm_seis,diff_acc,pr3,pr2 = asd(gif,xarm,diff_seis,comm_seis,
                                            diff_acc,pr3,pr2,fftlen=fftlen,ovlp=ovlp)


# plot ASD and coherence
fig, (ax1,ax2) = plt.subplots(2,1,figsize=(10,10),sharex=True)
plt.subplots_adjust(hspace=0.06)
ax1.set_title('Sensor Correction {0}'.format(onoff),fontsize=40)
ax1.set_ylabel('Displacement [um/rtHz or um]',fontsize=25)
ax1.set_ylim(1e-4,10)
ax2.set_ylabel('Coherence',fontsize=25)
ax2.set_xlabel('Frequency [Hz]',fontsize=25)
ax2.set_ylim(0,1)
ax2.set_xlim(2e-2,8)
#ax1.loglog(xarm.frequencies.value[1:],abs(xarm.value[1:]-total.value),label='Resi',color='g',linewidth=2)
if plot_prs:
    ax1.loglog(pr3,label='PR3',linewidth=2)
    ax1.loglog(pr2,label='PR2',linewidth=2)
    ax2.semilogx(coh_xarm2pr2,label='X-arm vs. PR2',linewidth=2)
    ax2.semilogx(coh_xarm2pr3,label='X-arm vs. PR3',linewidth=2)
if plot_xarm:
    ax1.loglog(xarm,label='X-Arm (Measured)',color='g',linewidth=2)
if plot_simu:
    #ax1.loglog(total,color='m',linewidth=2,linestyle='-',label='X-Arm (Expected)')
    pass
if plot_gif:
    ax1.loglog(gif,label='GIF strainmeter',color='k')
    if plot_rms:
        ax1.loglog(diff_seis.rms(),color='k',linestyle='--')        
    if plot_xarm:
        ax2.semilogx(coh_gif2xarm,label='X-arm vs. GIF',color='k',linewidth=2)
    else:
        ax2.semilogx(coh_gif2diff,label='GIF vs. DIff',color='k',linewidth=2)
    if plot_rms:
        ax1.loglog(xarm.rms(),color='g',linewidth=2,linestyle='--')
if plot_seiscomm:
    ax1.loglog(comm_seis,label='Seis Comm',linestyle='--',linewidth=2,color='red')
    if plot_xarm:        
        ax2.semilogx(coh_xarm2seiscomm,label='X-arm vs. Seis Comm',linewidth=2,
                     color='red',zorder=0)
    else:
        ax2.semilogx(coh_gif2comm,label='GIF vs. Comm',color='red',linestyle='-',
                     linewidth=2)

if plot_seisdiff:
    ax1.loglog(diff_seis,label='Seis Diff',linestyle='--',linewidth=2,color='k')
    if plot_xarm:    
        ax2.semilogx(coh_xarm2seisdiff,label='X-arm vs. Seis Diff',
                     linewidth=2,color='k',linestyle='--')
        ax2.semilogx(coh_gif2diff,label='GIF vs. DIff',color='k',
                     linewidth=2,alpha=0.5,zorder=0)
    else:
        pass
if plot_accdiff:
    if plot_xarm:        
        ax1.loglog(diff_acc,label='Acc Diff',linestyle='--',linewidth=2,color='b')
        ax2.semilogx(coh_xarm2accdiff,label='X-arm vs. Acc Diff',
                    linewidth=2,color='b',linestyle='--')
    else:
        ax1.loglog(diff_acc,label='Acc Diff',linestyle='--',linewidth=2,color='b')
    
ax1.legend(fontsize=15,loc='lower left')
ax2.legend(fontsize=15,loc='upper left')
#ax1.set_yscale('linear')
#ax1.set_ylim(0,3)
plt.savefig('result.png')
plt.close()
