#
#! coding:utf-8
from __future__ import print_function
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 1000000
#print(mpl.rcParams['agg.path.chunksize'])
import numpy as np
from scipy.signal import butter, lfilter
from scipy import signal, interpolate
from control import matlab
from trillium import selfnoise

from miyopy.timeseries import TimeSeries as ts

try:
    import nds2
    import gwpy    
    from gwpy.timeseries import TimeSeries
except:
    pass


def bandpass(data, lowcut, highcut, fs, order=None, w=None,**kwargs):
    '''時系列データをバンドパスする関数


    Parameter
    ---------
    data : 
        バンドパスされる時系列データ。
    lowcut:
        


    Return
    ------

    '''
    nyq = 0.5 * fs
    if highcut==None:
        low = lowcut / nyq
        b, a = butter(order, low, btype='low',analog=False)
    elif lowcut==None:
        low = lowcut / nyq                
        b, a = butter(order, high, btype='high',analog=False)
    else:
        low = lowcut / nyq
        high = highcut / nyq        
        b, a = butter(order, [low, high], btype='band',analog=False)    
    y = lfilter(b, a, data)
    return y,b,a


def fetch(chname,start,end,ndsserver='10.68.10.121'):
    try:
        print('Loading data from nds server... It may take few minutes..')
        print('ChannelName : {}'.format(chname))        
        data = TimeSeries.fetch(chname,start, end, host=ndsserver, port=8088)
        print('Done.')
        return data        
    except RuntimeError as e:
        print('[Error]',e)
        print('[Error] Faild to establish a connection to NDSserver({})'.format(ndsserver))
        print('[Error] Please check the connection with "ping {}"'.format(ndsserver))
        print('[Error] Exit..')
        exit()
    except ImportError as e:
        print('[Error] {}. Please execute "source ~/.bash_profile"'.format(e))
        exit()


def makedirs(newdir):
    try:
        os.makedirs(newdir)
    except OSError as e:
        if e.args[0]==17:
            print('[Attention] Oops! {} {}. So, skip mkdir'.format(e.args[1],newdir))


def remove_nandata(data_fname):
    '''Nanを含むDumpファイルを消す関数。

    読み込んだDumpファイルにNanが入っている場合，そのファイルを消す。

    Parameter
    ---------
    data_fname : str
    
    '''
    print('Finding nan data file...')
    for fname in data_fname:
        with open(prefix+fname,'rb') as f:
            data = np.load(f)
            if True in np.isnan(data):
                os.remove(prefix+fname)
                print('remove {}'.format(prefix+fname))
    print('Done.')

    
def does_data_exist(start,end,startlist,endlist):
    if start not in startlist:
        errortxt = 'Invalid start time; {0}\n'\
                   'Please choose start time in \n {1}'\
                   .format(start,(startlist))
        raise ValueError(errortxt)
    if end not in endlist or end<start:
        endlist = filter(lambda x:x>start,endlist)
        errortxt = 'Invalid end time; {0}\n'\
                   'Please choose end time in \n {1}'\
                   .format(end,(endlist))
        raise ValueError(errortxt)
    if end-start!=2**13:
        raise UserWarning('tlen is not 2**13.')
    
    return start,end
        
    
def get_time(remove_nandata=False):
    list = os.listdir(prefix)
    data_fname = filter(lambda x :re.match("121.*121.",x) ,list)
    start_end = np.array(map(lambda x:re.findall('[0-9]{10}',x),data_fname),
                         dtype=np.int32)
    startlist = np.unique(start_end[:,0])
    startlist = np.sort(startlist)
    endlist = np.unique(start_end[:,1])   
    endlist = np.sort(endlist)    
    if len(startlist)!=len(endlist):
        raise UserWarning('!')
    
    if remove_nandata:
        remove_nandata(data_fname)

    argvs = sys.argv  
    argc = len(argvs)
    if (argc == 3):
        start = int(argvs[1])
        end = int(argvs[2])
    else:
        raise ValueError('Usage:python {} <starttime> <endtime>'.format(argvs[0]))
    
    start, end = does_data_exist(start,end,startlist,endlist)
    return start,end


def download_gifdata(start,end,chname='CALC_STRAIN',
                     prefix=None,prefix_gif=None,**kwargs):
    print('taking data from gif')
    data = ts.read(start,end-start,chname,prefix=prefix_gif,**kwargs)
    value = data.value
    print('done')
    print('saving data')
    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
    print(fname)
    with open(fname,'w') as f:
        np.save(f,value)
    print('done')
    return value

    
def download_kagradata(start,end,chname=None,prefix=None,**kwargs):
    '''
    '''
    
    if chname==None:
        raise ValueError('Invalid chname name; {}'.format(chname))

    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
    print('data taking {}'.format(chname))
    data = TimeSeries.fetch(chname,
                            start, end,
                            host='10.68.10.121', port=8088)
    data =  data.value 
    print('done')
    print('save')

    fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])        
    with open(fname,'w') as f:
        np.save(f,data)
    return data


def read(start,end,chname,**kwargs):
    import platform
    import socket    
    system = platform.system()
    hostname = socket.gethostname()    
    if system=='Darwin':
        prefix='/Users/miyo/Dropbox/KagraData/dump/'
        prefix_gif='/Users/miyo/Dropbox/KagraData/gif/'
        prefix_kagra='./'
    elif system=='Linux':
        if hostname=='z400-001':
            prefix='/home/miyo/Dropbox/KagraData/dump/'
            prefix_gif='/home/miyo/Dropbox/KagraData/gif/'
        else:
            prefix = './'
            prefix_gif = './'
            prefix_kagra='./'                    
    else:
        raise UserWarning('Invalid computer system; {}'.format(system))


    try:
        fname = prefix+'{0}_{1}_{2}'.format(start,end,chname[3:])
        with open(fname,'rb') as f:
            value = np.load(f)
    except Exception as e:
        print(e)
        if 'K1' not in chname:
            value = download_gifdata(start,end,chname=chname,prefix=prefix,prefix_gif=prefix_gif,**kwargs)
        else:
            value = download_kagradata(start,end,chname=chname,prefix=prefix_kagra)
    return value




def _bandpass(data, lowcut, highcut, fs, order=3, w=None,plot=False,**kwargs):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandpass',analog=True)
    if plot:
        w, mag, phase = signal.bode([b,a],w=w)
        if True in np.isinf(mag):
            raise ValueError('Data have Inf value! \n Exit..')
        return w,mag,phase
    else:
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
    print(d_[1])
    rms_mintrend = np.std(d_,axis=1)
    print(rms_mintrend[1])
    exit()
    return rms_mintrend

def histgram(noise,plot=True,fit=True,**kwargs):
    '''
    
    '''
    hist,bins,_ = plt.hist(noise,bins=250,histtype='step',**kwargs)
    return hist,bins


def plot_bandpass(lowHz,midHz,higHz,order,w,fs=None,**kwargs):
    w1,mag1,phase1 = _bandpass(None,lowHz[0],lowHz[1],fs,order,w=w,plot=True,**kwargs)
    w2,mag2,phase2 = _bandpass(None,midHz[0],midHz[1],fs,order,w=w,plot=True,**kwargs)
    w3,mag3,phase3 = _bandpass(None,higHz[0],higHz[1],fs,order,w=w,plot=True,**kwargs)
    w2f = lambda w :(fs*0.5/np.pi)*w
    fig, (ax1,ax2) = plt.subplots(2, 1, sharex=True, dpi=640)
    plt.subplots_adjust(hspace=0.17,top=0.90)    
    ax1.loglog(w2f(w1),10**(mag1/20),label='0.03-0.1Hz',color='k')    
    ax1.loglog(w2f(w2),10**(mag2/20),label='0.1-0.3Hz',color='b')
    ax1.loglog(w2f(w3),10**(mag3/20),label='0.3-1Hz',color='r')
    ax1.set_ylim(1e-2,2)
    ax1.set_xlim(1e-3,1e1)
    ax1.legend(loc='upper right')
    ax1.grid(which='major',linestyle='-', linewidth=1)
    ax1.grid(which='minor',linestyle=':', linewidth=1)
    ax1.set_ylabel('Magnitude')
    wrap = lambda deg:np.rad2deg(( np.deg2rad(deg)+np.pi)%(2*np.pi)-np.pi)     
    ax2.semilogx(w2f(w1),wrap(phase1),label='0.03-0.1Hz',color='k')
    ax2.semilogx(w2f(w2),wrap(phase2),label='0.1-0.3Hz',color='b')
    ax2.semilogx(w2f(w3),wrap(phase3),label='0.3-1Hz',color='r')
    ax2.set_yticklabels(np.arange(-180,181,90))
    ax2.set_ylim(-200,200)
    ax2.grid(which='major',linestyle='-', linewidth=1)
    ax2.grid(which='minor',linestyle=':', linewidth=1)    
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Phase [Degrees]')
    ax2.set_xlim(1e-3,1e1)    
    plt.suptitle('Bandpass Filter for Seismometer')
    plt.xlabel('Frequency [Hz]')
    plt.savefig('Bode_Bandpass.png')
    plt.close()
    

def get_bandpass(data1,fs=None,return_rms=False,plot=False,**kwargs):
    lowHz = [0.03,0.1] # Hz
    midHz = [0.1,0.3] # Hz
    higHz = [0.3,1] # Hz
    order = 1 # max 3??
    w = np.logspace(-7,1,1e5) # rad/sec
    
    if plot:
        plot_bandpass(lowHz,midHz,higHz,order,w,fs,**kwargs)
        print('plot.')
        exit()
        
    if fs==None:
        raise ValueError('Invalid fs; {}'.format(fs))
        
    if not return_rms:           
        nofilt = data1    
        lowfreq =    _bandpass(data1,lowHz[0],lowHz[1],fs,order)
        microseism = _bandpass(data1,midHz[0],midHz[1],fs,order)
        highfreq =   _bandpass(data1,higHz[0],higHz[1],fs,order)        
        return nofilt,lowfreq,microseism,highfreq
    if return_rms:
        nofilt = rms_mintrend(data1,fs)
        lowfreq = rms_mintrend(lowfreq,fs)
        microseism = rms_mintrend(microseism,fs)
        highfreq = rms_mintrend(highfreq,fs)
        time = np.arange(len(nofilt))/fs/60.0
        return nofilt,lowfreq,microseism,highfreq
    else:
        raise ValueError('Invalid rms flag; {}'.format(rms))
    


def plot_axs(ax1,time,data1,data2,**kwargs):
    print(kwargs)
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
    print('calc timeseries'    )
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
    print('timeseries_{0}.png'.format(fname))
    plt.savefig('timeseries_{0}.png'.format(fname))
    #plt.show()
    plt.close()

    
    print('calc histgram')
    #hist,bins = histgram(data1_lowfreq,cumulative=True)
    #hist,bins = histgram(data1_microseism,cumulative=True)
    #plt.savefig('histfram_{0}.png'.format(fname))
    #plt.close()
    
def interp(data,f,f_):
        f1 = interpolate.interp1d(f, data)
        return f1(f_)        

def cf(alpha=0.05,k=32):
    from scipy.stats import chi2   
    cfmax = k/chi2.ppf(alpha/2.0, k)
    cfmin = k/chi2.ppf(1.0-alpha/2.0, k)
    return cfmin, cfmax

def H(asd):
    return asd

def asd(data1,fs,ave=None,integ=False,gif=False,
        psd='asd',scaling='density',window='hanning',**kwargs):
    
    if ave==None:
        raise ValueError('Average is not defined. ave; {}'.format(ave))
    
    f, Pxx_den = signal.welch(data1,
                              fs,
                              nperseg=len(data1)/ave,
                              window=window,
                              scaling=scaling,
                              #**kwargs
                              )
    f = f[1:]
    Pxx_den = Pxx_den[1:]
    if psd=='asd':        
        Asd_den = np.sqrt(Pxx_den)
    elif psd=='psd':
        Asd_den = Pxx_den
        pass
    else:
        raise ValueError('invalid type psd; {}'.format(psd))    
            
    if integ:
        Asd_den = Asd_den/(2.0*np.pi*f)
    if gif:
        Asd_den = H(Asd_den)
    return f, Asd_den

def get_coh(data1,data2,fs,tlen=None,ave=32,integ=False,gif=False,**kwargs):
    print(tlen)
    f, P1_den = signal.welch(data1,
                             fs,
                             nperseg=len(data1)/ave,
                             window='hanning',
                             scaling='density',
    )
    f, P2_den = signal.welch(data1,
                             fs,
                             nperseg=len(data2)/ave,
                             window='hanning',
                             scaling='density',
    )
    f, csd = signal.csd(data1,
                        data2,
                        fs,
                        nperseg=len(data1)/ave,
                        window='hanning',
                        scaling='density',
                        )
    f, coh2 = signal.coherence(data1, data2, fs=len(data1)/tlen, nperseg=len(data1)/ave)        
    A1_den = np.sqrt(P1_den)
    A2_den = np.sqrt(P2_den)
    #csd = np.sqrt(csd)
    deg = np.rad2deg(np.angle(csd))
    if gif:
        Pxx_den = H(Pxx_den)            
    #coh2 = np.sqrt((np.abs(csd)**2/np.sqrt(P1_den*P2_den)))
    return f, coh2, deg


def test_get_bandpass():
    from random import random
    tlen = 2**13
    fs = 2048.0
    freq = 100.0
    ave = 64
    time = np.arange(tlen*fs)/fs
    bw = np.sqrt(1.0/tlen*(float(ave*2)))     
    noise_amp = 1e-3 * np.sqrt(fs) # 1e-3 [V]
    signal_amp = 1.0*np.sqrt(2.0) # rms [V]
    y = np.random.normal(scale=noise_amp, size=time.shape)
    y += signal_amp*np.sin(time*freq*2.0*np.pi)
    y0,y1,y2,y3 = get_bandpass(y,fs=fs,plot=False)    
    f, asd_y0 = asd(y0,fs,ave=ave,psd='asd',scaling='spectrum',window='flattop' )
    #f, asd_y0 = asd(y0,fs,ave=ave,psd='asd',scaling='density',window='hanning' )
    print('bw : {} [sqrtHz]'.format(bw))
    print('amp : {} [V/sqrtHz]'.format(max(asd_y0)))
    print('amp : {} [V]'.format(max(asd_y0)*bw))
    #f, asd_y1 = asd(y1,fs,ave=64,psd='asd')
    #f, asd_y2 = asd(y2,fs,ave=64,psd='asd')
    #f, asd_y3 = asd(y3,fs,ave=64,psd='asd')
    plt.loglog(f,asd_y0)
    #plt.loglog(f,asd_y1)
    #plt.loglog(f,asd_y1)
    #plt.loglog(f,asd_y2)
    #plt.ylim([1e-4,1e1])
    #plt.plot(time,y)
    plt.grid(which='major',linestyle='-', linewidth=1)
    plt.grid(which='minor',linestyle=':', linewidth=1)        
    plt.savefig('test_get_bandpass.png')
    plt.close()
    
if __name__ == "__main__":
    test_get_bandpass()
