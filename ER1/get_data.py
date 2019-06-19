#
#! coding:utf-8
import numpy as np

from astropy import units as u

from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.segments import SegmentList
from gwpy.time import tconvert
from gwpy.detector import Channel

ok = SegmentList.read('segments_locked.txt')

segnum = 4
start = ok[segnum][0]
end = ok[segnum][1]

seis_ch = ['K1:PEM-SEIS_IXV_GND_X_OUT16',
           'K1:PEM-SEIS_IXV_GND_Y_OUT16',
           'K1:PEM-SEIS_IXV_GND_Z_OUT16',
           'K1:PEM-SEIS_EXV_GND_X_OUT16',
           'K1:PEM-SEIS_EXV_GND_Y_OUT16',
           'K1:PEM-SEIS_EXV_GND_Z_OUT16',
           'K1:PEM-SEIS_EYV_GND_X_OUT16',
           'K1:PEM-SEIS_EYV_GND_Y_OUT16',
           'K1:PEM-SEIS_EYV_GND_Z_OUT16',
           'K1:PEM-SEIS_MCF_GND_X_OUT16',
           'K1:PEM-SEIS_MCF_GND_Y_OUT16',
           'K1:PEM-SEIS_MCF_GND_Z_OUT16',
           'K1:PEM-SEIS_BS_GND_X_OUT16',
           'K1:PEM-SEIS_BS_GND_Y_OUT16',
           'K1:PEM-SEIS_BS_GND_Z_OUT16',]
gif_ch = ['K1:GIF-X_STRAIN_OUT16',
          'K1:GIF-X_ZABS_OUT16',]
sus_ch = ['K1:VIS-ETMX_IP_BLEND_ACCL_OUT16',
          'K1:VIS-ETMX_IP_BLEND_ACCT_OUT16',
          'K1:VIS-ETMX_IP_BLEND_ACCY_OUT16',
          'K1:VIS-ETMX_IP_DAMP_L_OUT16',
          'K1:VIS-ETMX_IP_DAMP_T_OUT16',
          'K1:VIS-ETMX_IP_DAMP_Y_OUT16',
          'K1:VIS-ETMX_IP_VELDAMP_L_OUT16',
          'K1:VIS-ETMX_IP_VELDAMP_T_OUT16',
          'K1:VIS-ETMX_IP_VELDAMP_Y_OUT16',          
          'K1:VIS-ITMX_IP_BLEND_ACCL_OUT16',
          'K1:VIS-ITMX_IP_BLEND_ACCT_OUT16',
          'K1:VIS-ITMX_IP_BLEND_ACCY_OUT16',
          'K1:VIS-ITMX_IP_DAMP_L_OUT16',
          'K1:VIS-ITMX_IP_DAMP_T_OUT16',
          'K1:VIS-ITMX_IP_DAMP_Y_OUT16',
          'K1:VIS-ITMX_IP_VELDAMP_L_OUT16',
          'K1:VIS-ITMX_IP_VELDAMP_T_OUT16',
          'K1:VIS-ITMX_IP_VELDAMP_Y_OUT16',]
ifo_ch = ['K1:LSC-CARM_SERVO_SLOW_MON_OUT16',
          'K1:IMC-MCL_SERVO_OUT16',              
          'K1:VIS-MCE_TM_LOCK_L_OUT16',
          'K1:ALS-X_PDH_SLOW_DAQ_INMON',
          'K1:CAL-CS_PROC_XARM_FREQUENCY_MON',
          'K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16',
              ]    
    
chname = seis_ch + gif_ch + sus_ch + ifo_ch
#chname = ifo_ch

data = TimeSeriesDict.fetch(chname,start,end,host='10.68.10.121',
                            verbose=True,port=8088,pad=np.nan)

for _data in data.values():
    print './segment_{0}/{1}.gwf'.format(segnum,_data.name)
    _data.override_unit('ct')
    _data.write('./segment_{0}/{1}.gwf'.format(segnum,_data.name),format='gwf.lalframe')
    
