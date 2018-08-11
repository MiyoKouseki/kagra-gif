import nds2
import gwpy
from gwpy.timeseries import TimeSeries
start = 1209286818
end = 1209286818+64
chname = 'K1:VIS-ETMY_TM_OPLEV_TILT_YAW_OUT_DQ'
#chname = 'K1:PEM-EX1_SEIS_NS_SENSINF_OUT_DQ'
etmy_yaw = TimeSeries.fetch(chname,
                        start, end,
                        host='10.68.10.121', port=8088)
chname = 'K1:PEM-EY1_SEIS_NS_SENSINF_OUT_DQ'
seis = TimeSeries.fetch(chname,
                        start, end,
                        host='10.68.10.121', port=8088)
if False:
    coh = etmy_yaw.coherence(seis, fftlength=128, overlap=64)
    plot = coh.plot(figsize=[12, 6], label=None)
    ax = plot.gca()
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Coherence')
    ax.set_yscale('linear')
    ax.set_ylim(0, 1)
    ax.set_title('Coherence between PSL periscope motion and LIGO-Hanford strain data')
    plot.savefig('coh.png')
    
etmy_yaw = etmy_yaw.bandpass(0.1,1)
plot = etmy_yaw.plot()
plot.savefig('time_etmy.png')

seis = seis.bandpass(0.01,1)
plot = seis.plot()
plot.savefig('time_seis.png')
