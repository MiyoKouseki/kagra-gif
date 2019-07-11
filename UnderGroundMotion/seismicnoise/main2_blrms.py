from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert,from_gps
import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np

press = np.loadtxt('./data_jma/miyako_press.txt',dtype=np.float32)
# 05/31 2018 01:00 - 07/02 2019 00:00 (JST)
# 1211731218 - 1246028418 
times = range(1211731218,1246028418+1,3600)*u.s
press = TimeSeries(press,times=times,unit='hPa',name='JMA:MIYAKO-PRESS')
press.write('./data_jma/miyako_press.gwf')

toyama = TimeSeries.read('./data_jma/toyama_pressure.gwf','JMA:TOYAMA-PRESSURE')
takayama = TimeSeries.read('./data_jma/takayama_pressure.gwf','JMA:TAKAYAMA-PRESSURE')
inotani = TimeSeries.read('./data_jma/inotani_rain.gwf','JMA:INOTANI-RAIN')
kamioka = TimeSeries.read('./data_jma/kamioka_rain.gwf','JMA:KAMIOKA-RAIN')
shiomisaki = TimeSeries.read('./data_jma/shiomisaki_press.gwf','JMA:SHIOMISAKI-PRESS')
aomori = TimeSeries.read('./data_jma/aomori_press.gwf','JMA:AOMORI-PRESS')
tanegashima = TimeSeries.read('./data_jma/tanegashima_press.gwf','JMA:TANEGASHIMA-PRESS')
tsuruga = TimeSeries.read('./data_jma/tsuruga_press.gwf','JMA:TSURUGA-PRESS')
choshi = TimeSeries.read('./data_jma/choshi_press.gwf','JMA:CHOSHI-PRESS')
omaezaki = TimeSeries.read('./data_jma/omaezaki_press.gwf','JMA:OMAEZAKI-PRESS')
irago = TimeSeries.read('./data_jma/irago_press.gwf','JMA:IRAGO-PRESS')
miyako = TimeSeries.read('./data_jma/miyako_press.gwf','JMA:MIYAKO-PRESS')

c2v = 20.0/2**15
gain = 10**(30.0/20)    
blrms100_300 = TimeSeries.read('./data2/LongTerm_Z_BLRMS_100_300mHz.gwf','K1:PEM-EX1_SEIS_Z_SENSINF_IN1_DQ')
blrms100_300 = blrms100_300/gain*c2v/1000*1e6
blrms0_100 = TimeSeries.read('./data2/LongTerm_Z_BLRMS_0_100mHz.gwf','K1:PEM-EX1_SEIS_Z_SENSINF_IN1_DQ')
blrms0_100 = blrms0_100/gain*c2v/1000*1e6
blrms200_300 = TimeSeries.read('./data2/LongTerm_Z_BLRMS_200_300mHz.gwf','K1:PEM-EX1_SEIS_Z_SENSINF_IN1_DQ')
blrms200_300 = blrms200_300/gain*c2v/1000*1e6
blrms100_200 = TimeSeries.read('./data2/LongTerm_Z_BLRMS_100_200mHz.gwf','K1:PEM-EX1_SEIS_Z_SENSINF_IN1_DQ')
blrms100_200 = blrms100_200/gain*c2v/1000*1e6
blrms1_3 = TimeSeries.read('./data2/LongTerm_Z_BLRMS_1_3Hz.gwf','K1:PEM-EX1_SEIS_Z_SENSINF_IN1_DQ')
blrms1_3 = blrms1_3/gain*c2v/1000*1e6

t0 = blrms100_300.t0
print from_gps(t0.value)
tlen = 3600*24*30*6*u.s
#t0 = t0 + tlen
tend = t0 + tlen
#
blrms100_300 = blrms100_300.crop(t0.value,(t0+tlen).value)
blrms200_300 = blrms200_300.crop(t0.value,(t0+tlen).value)
blrms100_200 = blrms100_200.crop(t0.value,(t0+tlen).value)
blrms0_100   = blrms0_100.crop(t0.value,(t0+tlen).value)
blrms1_3     = blrms1_3.crop(t0.value,(t0+tlen).value)*10
#
toyama      = toyama.crop(t0.value,(t0+tlen).value)
takayama    = takayama.crop(t0.value,(t0+tlen).value)
inotani     = inotani.crop(t0.value,(t0+tlen).value)
kamioka     = kamioka.crop(t0.value,(t0+tlen).value)
shiomisaki  = shiomisaki.crop(t0.value,(t0+tlen).value)
aomori      = aomori.crop(t0.value,(t0+tlen).value)
tanegashima = tanegashima.crop(t0.value,(t0+tlen).value)
tsuruga     = tsuruga.crop(t0.value,(t0+tlen).value)
choshi      = choshi.crop(t0.value,(t0+tlen).value)
omaezaki    = omaezaki.crop(t0.value,(t0+tlen).value)
irago       = irago.crop(t0.value,(t0+tlen).value)
miyako      = miyako.crop(t0.value,(t0+tlen).value)
#
fig,(ax,ax2,ax3) = plt.subplots(3,1,figsize=(19,7),sharex=True)
ax.plot(blrms100_300,'ko',markersize=1,label='Vertical: 100-300 mHz')
ax2.plot(blrms100_200,'bo',markersize=1,label='Vertical: 100-200 mHz')
ax2.plot(blrms200_300,'ro',markersize=1,label='Vertical: 200-300 mHz')
#ax.plot(blrms0_100,'ko',markersize=1,label='Vertical: 0-100 mHz')
#ax.plot(blrms1_3,'ro',markersize=1,label='Z: 1-3 Hz')
ax3.plot(toyama,'go',markersize=1,label='Toyama')
ax3.plot(choshi,'mo',markersize=1,label='Choshi')
#ax3.plot(takayama,'bo',markersize=1,label='Takayama')
#ax3.plot(shiomisaki,'ko',markersize=1,label='Shiomisaki')
#ax3.plot(aomori,'ko',markersize=1,label='Aomori')
#ax3.plot(tanegashima,'go',markersize=1,label='Tanegashima')
#ax3.plot(tsuruga,'ko',markersize=1,label='Tsuruga')
#ax3.plot(omaezaki,'ko',markersize=1,label='Omaezaki')
#ax3.plot(irago,'ko',markersize=1,label='Irago')
#ax3.plot(miyako,'ko',markersize=1,label='Miyako')
ax.set_xscale('auto-gps')
ax2.set_xscale('auto-gps')
ax3.set_xscale('auto-gps')
ax.set_ylabel('Velocity [um/sec]',fontsize=20)
ax2.set_ylabel('Velocity [um/sec]',fontsize=20)
ax3.set_ylabel('Pressure [hPa]',fontsize=20)
ax.set_xlim(t0.value,tend.value)
ax.set_ylim(0,3)
ax2.set_ylim(0,3)
ax3.set_ylim(940,1040)
ax3.set_yticks(range(940,1040,40))
ax.legend(fontsize=20,loc='upper left',numpoints=1,markerscale=10)
ax2.legend(fontsize=20,loc='upper left',numpoints=1,markerscale=10)
ax3.legend(fontsize=20,loc='lower left',numpoints=1,markerscale=10)
#ax2.set_ylim(990,1050)
if False:
    ax3.plot(inotani,'go',markersize=1,label='Inotani')
    ax3.plot(kamioka,'mo',markersize=1,label='Kamioka')
    ax3.set_xscale('auto-gps')
    ax3.set_ylabel('Rain [mm]',fontsize=20)
    ax3.set_ylim(0,25)
    ax3.legend(fontsize=20,loc='lower left',numpoints=1,markerscale=10)
plt.savefig('./results/blrms.png')
plt.close()
