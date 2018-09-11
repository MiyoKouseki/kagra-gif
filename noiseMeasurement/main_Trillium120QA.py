#
#! coding:utf-8
from miyopy.utils.tips import *
from miyopy.signal import coherence,asd
from miyopy.plot import plot21_coherence


def plot_Coherence_SameAxis(t1,t2,t3,pair,tlen,start,end,fs,ave):
    t1_we,t1_ns,t1_zz = t1
    t2_we,t2_ns,t2_zz = t2
    t3_we,t3_ns,t3_zz = t3
    f, coh12_wewe, deg12_wewe = coherence(t1_we,t2_we,fs,tlen,ave=ave)
    f, coh13_wewe, deg13_wewe = coherence(t1_we,t3_we,fs,tlen,ave=ave)
    f, coh12_nsns, deg12_nsns = coherence(t1_ns,t2_ns,fs,tlen,ave=ave)
    f, coh13_nsns, deg13_nsns = coherence(t1_ns,t3_ns,fs,tlen,ave=ave)
    f, coh12_zzzz, deg12_zzzz = coherence(t1_zz,t2_zz,fs,tlen,ave=ave)
    f, coh13_zzzz, deg13_zzzz = coherence(t1_zz,t3_zz,fs,tlen,ave=ave)    
    plot21_coherence([f,f],
                     [coh13_wewe,coh12_wewe],
                     [deg13_wewe,deg12_wewe],
                     ave=32,
                     label=['L=3000m','L=0.3m'],
                     title='Coherence_we_{0}_{1}'.format(start,end),
                     )
    plot21_coherence([f,f],
                     [coh13_nsns,coh12_nsns],
                     [deg13_nsns,deg12_nsns],
                     ave=32,
                     label=['L=3000m','L=0.3m'],
                     title='Coherence_ns_{0}_{1}'.format(start,end),
                     )
    plot21_coherence([f,f],
                     [coh13_zzzz,coh12_zzzz],
                     [deg13_zzzz,deg12_zzzz],
                     ave=32,
                     label=['L=3000m','L=0.3m'],
                     title='Coherence_zz_{0}_{1}'.format(start,end),
                     )


def plot_Coherence_DifferentAxis(t1,t3,axis,tlen,start,end,fs,ave):
    '''
    '''
    t1_we,t1_ns,t1_zz = t1
    t3_we,t3_ns,t3_zz = t3
    f, coh13_wens, deg13_wens = coherence(t1_we,t3_ns,fs,tlen,ave=ave)
    f, coh13_wezz, deg13_wezz = coherence(t1_we,t3_zz,fs,tlen,ave=ave)    
    plot21_coherence([f,f],
                     [coh13_wens,coh13_wezz],
                     [deg13_wens,deg13_wezz],
                     ave=32,
                     label=['{0}we-ns'.format(axis),'{0}we-zz'.format(axis)],
                     title='Coherence_{0}_{1}_{2}'.format(axis,start,end),
                     )
    
def coh2snr(coh,deg):
    # if 1>coh>0 :SNR = - coh/(1-coh)
    # if coh<0   :SNR = - coh/(1-coh)
    _p = lambda x:  1*x/(1.0-x)
    _m = lambda x: -1*x/(1.0-x)
    #coh = coh*np.exp(1j*np.deg2rad(deg)).real
    #coh = coh*np.cos(np.deg2rad(deg))    
    snr = [_p(_coh) for _coh in coh]
    #snr = np.array(snr)
    snr = [_snr if _snr>1 else 1 for _snr in snr]
    #print(True in coh>1.0)
    #print(snr[:10])
    #print(coh[:10])
    #exit()
    #snr = map(_m,coh)
    #snr = [ _p(_coh) for _coh in coh]
    #snr = np.abs(snr)
    return np.array(snr)

c2V = 10.0/2**15

def V2vel(V):
    return V/1204.5
    
def main(start,end):
    t1_ns = read(start,end,'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ')*c2V
    t1_we = read(start,end,'K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ')*c2V
    t1_zz = read(start,end,'K1:PEM-IXV_SEIS_Z_SENSINF_IN1_DQ')*c2V
    t3_ns = read(start,end,'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ')*c2V
    t3_we = read(start,end,'K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ')*c2V
    t3_zz = read(start,end,'K1:PEM-EXV_SEIS_Z_SENSINF_IN1_DQ')*c2V
    t2_ns = read(start,end,'K1:PEM-IXV_SEIS_TEST_NS_SENSINF_IN1_DQ')*c2V
    t2_we = read(start,end,'K1:PEM-IXV_SEIS_TEST_WE_SENSINF_IN1_DQ')*c2V
    t2_zz = read(start,end,'K1:PEM-IXV_SEIS_TEST_Z_SENSINF_IN1_DQ')*c2V
    # init
    tlen = end - start
    fs = len(t1_we)/tlen
    ave = 32
    t1 = [t1_we,t1_ns,t1_zz]
    t2 = [t2_we,t2_ns,t2_zz]
    t3 = [t3_we,t3_ns,t3_zz]
    #
    f_, asd1_we = asd(t1_we,fs,ave=ave)
    f_, asd2_we = asd(t2_we,fs,ave=ave)
    f_, asd3_we = asd(t3_we,fs,ave=ave)
    #
    f, coh13_wewe, deg13_wewe = coherence(t1_we,t3_we,fs,tlen,ave=ave)
    f, coh12_wewe, deg12_wewe = coherence(t1_we,t2_we,fs,tlen,ave=ave)
    coh13_wewe = np.sqrt(coh13_wewe)
    coh12_wewe = np.sqrt(coh12_wewe)
    snr13_wewe = coh2snr(coh13_wewe,deg13_wewe)
    snr12_wewe = coh2snr(coh12_wewe,deg12_wewe)
    n12_wewe = V2vel(asd1_we)*np.sqrt(1.0/(1+snr12_wewe))
    s12_wewe = V2vel(asd1_we)*np.sqrt(1.0/(1+snr12_wewe)*snr12_wewe)
    s13_wewe = np.sqrt(V2vel(asd1_we)*V2vel(asd3_we)*coh13_wewe)
    envnoise = s12_wewe - s13_wewe
    selfnoise = n12_wewe
    #
    import matplotlib.pyplot as plt
    plt.loglog(f_,V2vel(asd1_we),label='1_we')
    plt.loglog(f_,V2vel(asd2_we),label='2_we')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('ASD [m/sec/sqrtHz]')
    plt.ylim(1e-10,1e-5)
    plt.savefig('asd.png')    
    plt.close()    
    plt.loglog(f_,snr12_wewe)
    plt.savefig('snr.png')
    plt.close()
    plt.loglog(f_,V2vel(asd1_we),label='1_we',linewidth=3)
    plt.loglog(f_,V2vel(asd2_we),label='2_we',linewidth=3)    
    plt.loglog(f_,s12_wewe,label='x+b')
    #plt.loglog(f_,s13_wewe,label='x')
    plt.loglog(f_,selfnoise,label='n')
    #plt.semilogx(f_,snr12_wewe,label='snr12_wewe')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('ASD [m/sec/sqrtHz]')
    plt.ylim(1e-10,1e-5)    
    plt.legend()
    plt.savefig('selfnoise.png')
    plt.close()
    # plot 
    #plot_Coherence_SameAxis(t1,t2,t3,'1_23',tlen,start,end,fs,ave)
    #plot_Coherence_SameAxis(t1,t2,t3,'2_13',tlen,start,end,fs,ave)
    #plot_Coherence_DifferentAxis(t1,t1,'11',tlen,start,end,fs,ave)
    #plot_Coherence_DifferentAxis(t2,t2,'22',tlen,start,end,fs,ave)
    #plot_Coherence_DifferentAxis(t3,t3,'33',tlen,start,end,fs,ave)    
    #plot_Coherence_DifferentAxis(t1,t2,'12',tlen,start,end,fs,ave)
    #plot_Coherence_DifferentAxis(t1,t3,'13',tlen,start,end,fs,ave)
    #plot_Coherence_DifferentAxis(t2,t3,'23',tlen,start,end,fs,ave)    
    
    
        

if __name__ == "__main__":
    tlen = 2**13
    start = 1220194818
    end = start+tlen
    main(start,end)
    


    
