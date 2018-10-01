#
#! coding:utf-8
try:    
    import nds2
except:
    pass
import gwpy
from miyopy.timeseries import TimeSeries as ts
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter


def _bandpass(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    #b, a = butter(order, high, btype='low')    
    y = lfilter(b, a, data)
    return y


def _lowpass(data, lowcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = butter(order, low, btype='low')    
    y = lfilter(b, a, data)
    return y


def rms_mintrend(data,fs,tlen=60):
    ''' rms 
    
    1分(60sec)ごとにRMSを求める関数。    

    Parameter
    ---------
    
    '''
    if np.mod(len(data),tlen) != 0:
        mod = np.mod(len(data),tlen)*-1
        #print 
        #print 'data = data[:{0}]'.format(mod)
        data = data[:mod]
    
    d_ = data.reshape(len(data)/tlen,tlen)
    print d_[1]
    rms_mintrend = np.std(d_,axis=1)
    print rms_mintrend[1]
    #exit()
    return rms_mintrend

def histgram(noise,plot=True,fit=True,**kwargs):
    '''
    
    '''
    hist,bins,_ = plt.hist(noise,bins=250,histtype='step',**kwargs)
    return hist,bins

def get_blrms(data1):
    fs = 16.0
    #time = np.arange(len(data1))/fs/60.0/60.0    
    #data1_ = _lowpass(data1,0.03,16,4)    
    data1_lowfreq = _bandpass(data1,0.03,0.1,16,4)
    data1_microseism = _bandpass(data1,0.1,0.3,16,4)
    data1_highfreq = _bandpass(data1,0.3,3,16,4)
    #
    if True:
        nofilt = rms_mintrend(data1,fs)
        data1_lowfreq = rms_mintrend(data1_lowfreq,fs)
        data1_microseism = rms_mintrend(data1_microseism,fs)
        data1_highfreq = rms_mintrend(data1_highfreq,fs)
        time = np.arange(len(nofilt))/fs/60.0
    return nofilt,data1_lowfreq,data1_microseism,data1_highfreq,time


def plot_axs(ax1,time,data1,data2,**kwargs):
    print kwargs
    ylim1 = kwargs.get('ylim1', [0,3e0])
    ylim2 = kwargs.get('ylim2', [0,30])
    label1 = kwargs.get('label1', 'hoge')
    label2 = kwargs.get('label2', 'hoge')
    #ax1 = axs[0]
    ax2 = ax1.twinx()
    ax1.set_ylim(ylim2[0],ylim2[1])    
    ax1.plot(time,data2,label=label2,color='r')
    ax2.set_ylim(ylim1[0],ylim1[1])        
    ax2.plot(time,data1,label=label1,color='k',alpha=0.4)
    #plt.plot(time_,p500,label='Pressure X500')
    ax2.set_ylabel('Yend \n Horizon [um/sec]',color='k')
    ax1.set_ylabel('ETMY TM \nYaw [urad]',color='r')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    return ax1

def plot_blrms(data1,data2):
    nofilt1,low1,mid1,high1,time1 = get_blrms(data1)
    nofilt2,low2,mid2,high2,time2 = get_blrms(data2)
    time = time1
    #
    if False:
        fs_ = 200        
        #p500 = rms_mintrend(p500,fs_)
        time_ = np.arange(len(p500))/fs_/60.0/60.0
    #
    print 'calc timeseries'    
    fig = plt.figure(figsize=(10,8))
    fig, axs = plt.subplots(4, 1, figsize=(10, 8))    
    #plt.ylabel('Velocity [um/sec]')    
    #plt.title('Hoge')
    ylim1 = [0,3e0]
    ylim2 = [0,30]        
    plot_axs(axs[0],time1,nofilt1,nofilt2,ylim1=ylim1,ylim2=ylim2,
             label1='nofilt',
             label2='nofilt')
    plot_axs(axs[1],time1,high1,high2,ylim1=ylim1,ylim2=ylim2,
             label1='0.3-3Hz',
             label2='0.3-3Hz')
    plot_axs(axs[2],time1,mid1,mid2,ylim1=ylim1,ylim2=ylim2,
             label1='0.1-0.3Hz',
             label2='0.1-0.3Hz')             
    plot_axs(axs[3],time1,low1,low2,ylim1=ylim1,ylim2=ylim2,
             label1='0.03-0.1Hz',
             label2='0.03-0.1Hz')             
    
    axs[3].set_xlabel('Time [Hours]',fontsize=15)
    plt.tight_layout()
    print 'timeseries_{0}.png'.format(fname)
    plt.savefig('timeseries_{0}.png'.format(fname))
    #plt.show()
    plt.close()

    
    print 'calc histgram'
    #hist,bins = histgram(data1_lowfreq,cumulative=True)
    #hist,bins = histgram(data1_microseism,cumulative=True)
    #plt.savefig('histfram_{0}.png'.format(fname))
    #plt.close()    
    


if __name__ == '__main__':
    #start = 1209286818-5000
    start = 1209368000 # utc 2018-05-03T07:33:02
    start = 1209368000 # utc 2018-05-03T07:33:02
    start = 1214784018 # utc 2018-07-05T00:00:00
    #start = 1214611218 # utc 2018-07-03T00:00:00    
    # 
    #start = 1209368000 + 2**19
    #start = 1211252736
    end = start+2**13
    #end = start+2**10
    #end = start+2**17
    # read 
    if False:
        print 'taking data from gif'
        chname = 'X500_BARO'
        p500 = ts.read(start,end-start,'X500_BARO')
        p500 = p500.value
        print 'done'
        fname = '{0}_{1}_{2}'.format(start,end,chname[3:])        
        with open(fname,'w') as f:
            np.save(f,p500)
        exit()
        
    if False:
        #chname = 'K1:VIS-ETMY_TM_OPLEV_TILT_YAW_OUT16'
        chname = 'K1:PEM-EX1_SEIS_WE_SENSINF_OUT16'
        fname = '{0}_{1}_{2}'.format(start,end,chname[3:])        
        print 'data taking'    
        ey1 = TimeSeries.fetch(chname,
                            start, end,
                            host='10.68.10.121', port=8088)
        ey =  ey1.value#/1e-6 # um/sec
        ylim = [0,5e0]
        print 'done'
        print 'save'
        # save
        fname = '{0}_{1}_{2}'.format(start,end,chname[3:])        
        with open(fname,'w') as f:
            np.save(f,ey)
        exit()

    # load
    if False:
        chname = 'X500_BARO'
        fname = '{0}_{1}_{2}'.format(start,end,chname[3:])
        #ylim = [-5e0,5e0]
        #ylim = [0,5e0]
        with open(fname,'r') as f:
            p500 = np.load(f)

    if True:
        chname = 'K1:PEM-EX1_SEIS_WE_SENSINF_OUT16'
        fname = '{0}_{1}_{2}'.format(start,end,chname[3:])
        ylim = [-5e0,5e0]
        ylim = [0,3e0]
        with open(fname,'r') as f:
            exx = np.load(f)/1e-6 # um/sec
            
    if False:
        chname = 'K1:VIS-ETMY_TM_OPLEV_TILT_YAW_OUT16'
        fname = '{0}_{1}_{2}'.format(start,end,chname[3:])
        ylim = [-200,200]
        ylim = [0,30]        
        with open(fname,'r') as f:
            etmy_tm_yaw = np.load(f)                       
            yaw = etmy_tm_yaw
            
    plot_blrms(exx,exx)
    
