from dttdata import DttData

dtt = DttData('xarm_seismometer_IN1_DQ.xml')
ch1 = 'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ'
ch2 = 'K1:PEM-IXV_SEIS_TEST_NS_SENSINF_IN1_DQ'
ch3 = 'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ'

if False:    
    f,asd = dtt.getASD(ch1,ref=False)
    f,mag,deg = dtt.getCoherence(ch1,ch2,ref=False)
    
    import matplotlib.pyplot as plt
    fig, (ax0,ax1) = plt.subplots(2,1,figsize=(12, 6), dpi=80)
    ax0.semilogx(f,mag,label='/'.join([ch2,ch2]))
    ax0.legend()
    ax0.set_ylim(0,1)
    ax0.set_ylabel('Coherence',fontsize=20)
    ax1.semilogx(f,deg,label='/'.join([ch2,ch2]))
    ax1.legend()
    ax1.set_ylim(-180,180)
    ax1.set_yticks(range(-180,181,90))
    ax1.set_ylabel('Phase [deg]',fontsize=20)
    ax1.set_xlabel('Frequency [Hz]',fontsize=20)
    plt.savefig('test_coh_.png')
    plt.close()

from gwpy.frequencyseries import FrequencySeries
from gwpy.plotter import Plot

coh_12 = dtt.getCoherence(ch1,ch2,ref=False)
f,mag,deg = coh_12
mag_spec = FrequencySeries(mag, f0=f[0], df=f[1]-f[0])
deg_spec = FrequencySeries(deg, f0=f[0], df=f[1]-f[0])

plot = mag_spec.plot(label='Un-cleaned')
fig = plot.figure
print fig
#ax = plot.gca()
#ax.plot(deg_spec, label='Cleaned')
#plot = mag_spec.plot(ylabel='Magnitude',title='Coherence')
plot.savefig('test_coh.png')
