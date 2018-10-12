#
#! coding-utf8

from miyopy.io.reader import gif
from miyopy.signal import asd



if __name__=='__main__':
    start = 1223251218
    tlen = 3600*3
    prefix = '/Users/miyo/Dropbox/KagraData/gif/'
    x500 = gif.read(start,tlen,'X500_BARO',prefix=prefix)
    x2000 = gif.read(start,tlen,'X2000_BARO',prefix=prefix)

    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    print(len(x500))
    ax1.plot(-x500)
    ax2 = ax1.twinx()
    ax2.plot(x2000,alpha=0.4,color='k')
    plt.savefig('hoge.png')
    plt.close()
    #
    # check
    f,asd_x500 = asd(x500,200,ave=32,integ=False,gif=False,psd='asd',scaling='density',window='hanning')
    f,asd_x2000 = asd(x2000,200,ave=32,integ=False,gif=False,psd='asd',scaling='density',window='hanning')
    plt.loglog(f,asd_x500)
    plt.loglog(f,asd_x2000)
    #plt.ylim(1e-6,1e-4)
    plt.savefig('hoge_asd.png')
    plt.close()
    
