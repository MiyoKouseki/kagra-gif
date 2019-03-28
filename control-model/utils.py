from scipy.interpolate import interp1d 

def times(tf_mag,tf_freq,asd,asd_freq):
    func = interp1d(tf_freq,tf_mag)
    vel2v = func(asd_freq[1:])
    asd = asd[1:]*vel2v
    if False:
        import matplotlib.pyplot as plt
        plt.loglog(tf_freq,tf_mag,'o-')
        plt.savefig('hoge.png')
        exit()
    return asd_freq[1:],asd

def rms(tf_mag,tf_freq):    
    exit()
    return tf_freq,rms
