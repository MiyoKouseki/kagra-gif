#
#! coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u

from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.segments import SegmentList
from gwpy.time import tconvert
from gwpy.detector import Channel

ok = SegmentList.read('segments_locked.txt')

segnum = 0
start = ok[segnum][0]
end = ok[segnum][1]

chname = 'K1:GIF-X_STRAIN_OUT16'
gif_x = TimeSeries.read('./segment_{0}/{1}.gwf'.format(segnum,chname),chname,verbose=True,nproc=2)*1e6*3000 # disp
chname = 'K1:PEM-SEIS_IXV_GND_X_OUT16'    
ixv_x = TimeSeries.read('./segment_{0}/{1}.gwf'.format(segnum,chname),chname,verbose=True,nproc=2)
chname = 'K1:PEM-SEIS_EXV_GND_X_OUT16'    
exv_x = TimeSeries.read('./segment_{0}/{1}.gwf'.format(segnum,chname),chname,verbose=True,nproc=2)
chname = 'K1:VIS-ETMX_IP_DAMP_L_OUT16'
etmx_ip_x = TimeSeries.read('./segment_{0}/{1}.gwf'.format(segnum,chname),chname,verbose=True,nproc=2)
chname = 'K1:VIS-ITMX_IP_DAMP_L_OUT16'
itmx_ip_x = TimeSeries.read('./segment_{0}/{1}.gwf'.format(segnum,chname),chname,verbose=True,nproc=2)
chname = 'K1:LSC-CARM_SERVO_SLOW_MON_OUT16'
carm_x = TimeSeries.read('./segment_{0}/{1}.gwf'.format(segnum,chname),chname,verbose=True,nproc=2)
chname = 'K1:IMC-MCL_SERVO_OUT16'
mcl = TimeSeries.read('./segment_{0}/{1}.gwf'.format(segnum,chname),chname,verbose=True,nproc=2)
chname = 'K1:ALS-X_PDH_SLOW_DAQ_INMON'
pdh_x = TimeSeries.read('./segment_{0}/{1}.gwf'.format(segnum,chname),chname,verbose=True,nproc=2)
chname = 'K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16'
#chname = 'K1:CAL-CS_PROC_XARM_FREQUENCY_OUT16'
nu = 299792458.0/1064e-9 # [1/s]
xarm_freq = TimeSeries.read('./segment_{0}/{1}.gwf'.format(segnum,chname),chname,verbose=True,nproc=2)*(3000.0/nu)*1e6
print xarm_freq

diff_x = ixv_x - exv_x
diff_ip_x = itmx_ip_x - etmx_ip_x

fftlength = 2**9

ave = int((end-start)/fftlength/0.5)
    
def asd_of_arm_displacement():
    '''
    
    '''    
    diff = diff_x.asd(fftlength=fftlength,overlap=fftlength/2)
    from miyopy.utils.trillium import tr120
    freq = diff.frequencies.value
    v2vel = tr120.tf(freq)/1202.5
    #
    diff = diff/(2.0*np.pi*diff.frequencies.value)/v2vel
    gif = gif_x.asd(fftlength=fftlength,overlap=fftlength/2)
    xarm = xarm_freq.asd(fftlength=fftlength,overlap=fftlength/2)
    #
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2,1,figsize=(8,8))
    plt.suptitle('X arm displacement',fontsize=30)
    ax[0].loglog(gif,'k-',label='GIF')
    ax[0].loglog(diff,'b-',label='Seismometers')
    ax[0].loglog(xarm,'r-',label='XARM cavity')
    ax[0].legend(fontsize=10)
    ax[0].set_ylim(1e-4,100)
    ax[0].set_ylabel('Displacement [um/rtHz]')
    #
    coh = gif_x.coherence(diff_x,fftlength=fftlength,overlap=fftlength/2)
    coh_ip = diff_ip_x.coherence(gif_x,fftlength=fftlength,overlap=fftlength/2)
    coh_carm = carm_x.coherence(gif_x,fftlength=fftlength,overlap=fftlength/2)
    coh_mcl = mcl.coherence(gif_x,fftlength=fftlength,overlap=fftlength/2)
    coh_pdh_x = pdh_x.coherence(gif_x,fftlength=fftlength,overlap=fftlength/2)
    coh_xarm_freq = xarm_freq.coherence(gif_x,fftlength=fftlength,overlap=fftlength/2)
    coh_xarm_freq_ = diff_x.coherence(xarm_freq,fftlength=fftlength,overlap=fftlength/2)
    #
    ax[1].semilogx(coh,'k-',label='GIF - Seismometers')
    #ax[1].semilogx(coh_ip,'r-',label='GIF-PIstages')
    #ax[1].semilogx(coh_carm,'b-',label='GIF-CARM')
    #ax[1].semilogx(coh_carm,'b-',label=coh_carm.name.replace('_',' ')[:-25])
    #ax[1].semilogx(coh_mcl,'g-',label=coh_mcl.name.replace('_',' ')[:-25])
    #ax[1].semilogx(coh_pdh_x,'m-',label=coh_pdh_x.name.replace('_',' ')[:-25])
    ax[1].semilogx(coh_xarm_freq_,'b-',label='Seismometers - XARM cavity')
    ax[1].semilogx(coh_xarm_freq,'r-',label='XARM cavity - GIF')
    ax[1].text(13,0.0,'GPS : {0}, Ave : {1:d}'.format(ok[segnum][0],ave),rotation=90,horizontalalignment='left',verticalalignment='bottom',fontsize=10)
    ax[1].legend(fontsize=10,loc='upper right')
    ax[1].set_ylim(0,1)
    #ax[1].set_xlim(1e-2,8)
    ax[1].set_xlabel('Frequency [Hz]')
    ax[1].set_ylabel('Coherence')
    print('./segment_1/asd_arm.png')    
    plt.savefig('./segment_{0}/asd_arm.png'.format(segnum))
    plt.close()
    return ax


def timeseries():
    print gif_x
    import matplotlib.pyplot as plt
    #fig, ax0 = plt.subplots(1,1,figsize=(10,6))
    plot = gif_x.plot()
    ax0 = plot.gca()
    ax0.plot(gif_x,'k',label='GIF')
    ax0.legend(fontsize=15)
    ax0.set_ylabel('Displacement [um]')
    ax1 = ax0.twinx()
    ax1.plot(xarm_freq,'r',label='XARM',alpha=0.3)
    ax1.legend(loc='lower right',fontsize=15)
    ax1.set_ylabel('Frequency [Hz]')    
    plot.savefig('./segment_{0}/{1}.png'.format(segnum,gif_x.name))
    plot.close()
    

def short_timeseries():
    print gif_x
    import matplotlib.pyplot as plt
    fig, (ax0,ax1) = plt.subplots(2,1)
    gif_x = gif_x.bandpass(0.2,0.3,16.0)
    diff_x = diff_x.bandpass(0.2,0.3,16.0)
    gif_x = gif_x.crop(gif_x.t0.value+1200,gif_x.t0.value+1300)
    diff_x = diff_x.crop(diff_x.t0.value+1200,diff_x.t0.value+1300)*0.55
    diff_x.shift('-1.1s') 
    res = diff_x - gif_x    
    ax0.plot(gif_x,label='gif')
    ax0.plot(diff_x,label='seismometer')
    ax0.set_ylim(-1e-1,1e-1)
    ax0.legend()
    ax1.plot(res,label='residual')
    ax1.set_ylim(-1e-1,1e-1)
    ax1.legend()    
    plt.savefig('./segment_{0}/{1}.png'.format(segnum,gif_x.name))
    plt.close()
    exit()
    diff = diff_x.asd(fftlength=fftlength,overlap=fftlength/2)
    from miyopy.utils.trillium import tr120
    freq = diff.frequencies.value
    v2vel = tr120.tf(freq)/1202.5
    diff = diff/(2.0*np.pi*diff.frequencies.value)/v2vel
    gif = gif_x.asd(fftlength=fftlength,overlap=fftlength/2)        
    fig, ax = plt.subplots(1,1)
    ax.loglog(gif)
    ax.loglog(diff)
    ax.set_xlim(1e-2,8)
    ax.set_ylim(1e-3,1)
    plt.savefig('./segment_{0}/asd_arm_.png'.format(segnum))
    plt.close()
    print('!')

    
def plot21(ax0,ax1):
    fig,(_ax0,_ax1) = plt.subplots(2,1)
    #print ax0
    #print [a for a in dir(_ax0.axes) if 'axes' in a]
    #_ax0.update_from(ax0)
    #fig2 = plt.figure()
    fig.axes.append(ax0)
    #fig2.add_axes(ax0)
    #_ax1._axes(ax1)
    plt.savefig('./segment_{0}/xarm.png'.format(segnum))
    print('./segment_{0}/xarm.png'.format(segnum))
    plt.close()

if __name__ == "__main__":    
    ax0 = asd_of_arm_displacement()
    timeseries()    
