#
#! coding:utf-8
from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
#from trillium import selfnoise,V2Vel
from tips import *
#from plot import *
import re
from miyopy.plot import plotBandPassTimeseries,plotASD
from miyopy.utils.trillium import trillium120QA
#exit()

c2V = 10.0/2**15
deGain_compact = 10.0**(-45.0/20.0)
deGain_120QA = 10.0**(-30.0/20.0)
chname_dict = {'gifx':'CALC_STRAIN',
               'exx':'K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ',
               'exy':'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ',
               'exz':'K1:PEM-EXV_SEIS_Z_SENSINF_IN1_DQ',
               'eyx':'K1:PEM-EYV_SEIS_WE_SENSINF_IN1_DQ',
               'eyy':'K1:PEM-EYV_SEIS_NS_SENSINF_IN1_DQ',
               'eyz':'K1:PEM-EYV_SEIS_Z_SENSINF_IN1_DQ',
               'ixx':'K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ',
               'ixy':'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ',
               'ixz':'K1:PEM-IXV_SEIS_Z_SENSINF_IN1_DQ',
               'mcix':'K1:PEM-IMC_SEIS_MCI_WE_SENSINF_IN1_DQ',
               'mciy':'K1:PEM-IMC_SEIS_MCI_NS_SENSINF_IN1_DQ',
               'mciz':'K1:PEM-IMC_SEIS_MCI_Z_SENSINF_IN1_DQ',
               'mcex':'K1:PEM-IMC_SEIS_MCE_WE_SENSINF_IN1_DQ',
               'mcey':'K1:PEM-IMC_SEIS_MCE_NS_SENSINF_IN1_DQ',
               'mcez':'K1:PEM-IMC_SEIS_MCE_Z_SENSINF_IN1_DQ',
                }
fs = 2048.0
'''
chname_dict = {'gifx':'CALC_STRAIN',
               'exx':'K1:PEM-EXV_SEIS_WE_SENSINF_INMON',
               'exy':'K1:PEM-EXV_SEIS_NS_SENSINF_INMON',
               'exz':'K1:PEM-EXV_SEIS_Z_SENSINF_INMON',
               'eyx':'K1:PEM-EYV_SEIS_WE_SENSINF_INMON',
               'eyy':'K1:PEM-EYV_SEIS_NS_SENSINF_INMON',
               'eyz':'K1:PEM-EYV_SEIS_Z_SENSINF_INMON',
               'ixx':'K1:PEM-IXV_SEIS_WE_SENSINF_INMON',
               'ixy':'K1:PEM-IXV_SEIS_NS_SENSINF_INMON',
               'ixz':'K1:PEM-IXV_SEIS_Z_SENSINF_INMON',
               'mcix':'K1:PEM-IMC_SEIS_MCI_WE_SENSINF_INMON',
               'mciy':'K1:PEM-IMC_SEIS_MCI_NS_SENSINF_INMON',
               'mciz':'K1:PEM-IMC_SEIS_MCI_Z_SENSINF_INMON',
               'mcex':'K1:PEM-IMC_SEIS_MCE_WE_SENSINF_INMON',
               'mcey':'K1:PEM-IMC_SEIS_MCE_NS_SENSINF_INMON',
               'mcez':'K1:PEM-IMC_SEIS_MCE_Z_SENSINF_INMON',
                }        
fs = 16.0
'''
def main_xarm_seis_timeseries(start,tlen,exx,ixx):    
    plotBandPassTimeseries(exx,start,end,'K1:PEM-EXV_SEIS_WE_SENSINF_INMON',
                           ylabel='Velocity [m/sec]',
                           xlabel='Time [Minutes]')
    plotBandPassTimeseries(ixx,start,end,'K1:PEM-IXV_SEIS_WE_SENSINF_INMON',
                           ylabel='Velocity [m/sec]',
                           xlabel='Time [Minutes]')
    

def main_xarm_comdiff(start,tlen,diff,comm,gifx):
    # Xアームの基線長伸縮を比較するためのデータセット
    data1 = [diff,comm,gifx*3.0e3/np.sqrt(2.0)] # [V, V, m] に注意
    plot21_cdmr(data1,
                start=start,
                tlen=tlen,            
                title='Common Differential Mode Rate (CDMR) on the X-Arm Bedrock',
                fname='cdmr_xarm_gifx',
                labels1=['(Xend-Center)/sqrt(2) : Diff',
                         '(Xend+Center)/sqrt(2) : Com',
                         'GIFx'],
                labels2=['Com/Diff','Com/GIFx'],
                model='comm/gifx',
                linestyle=['k-','k:','r-'],
                adcnoise=True,
                selfnoiseplot=True,
                trillium='120QA',            
                )

    
def main_xarm_seis_asd(start,tlen,exx,ixx,**kwargs):
    data1 = [exx,ixx]
    '''
    data1 = [exx,
             trillium120QA.bandpass(exx,0.01,None,fs,3),
             trillium120QA.bandpass(exx,0.01,0.05,fs,3),
             trillium120QA.bandpass(exx,0.05,0.3,fs,3),
             trillium120QA.bandpass(exx,0.3,1,fs,3)
            ] '''
    plotASD(data1,
            start=start,             
            tlen=tlen,
            title='Seismometer at the EXV and IXV, and GIFx',
            fname='ASD-EXV_IXV_GIFX',
            #labels1=['exx','ixx'],
            labels1=['exx','ixx','low','mid','high'],
            #labels1=['exx','dc','low','mid','high'],
            linestyle=['k-','r--','b--','g--','m--'],
            ylim=[1e-9,1e-6],
            adcnoise=True,
            selfnoise=True,
            text='GPS:{0}\nHanning,ovlp=50%\n' \
                 'chname:{1}'.format(start,''),
            )    

def main_xarm_disp():
    # Xアームの基線長伸縮を比較するためのデータセット
    data9 = [exx/5500,ixx/5500,gifx] # [V, V, m] に注意
    labels91 = ['(Xend-Center)/sqrt(2) : Diff','(Xend+Center)/sqrt(2) : Com','GIFx']
    labels92 = ['Com/Diff','Com/GIFx']
    plot(data9,
         start=start,             
         tlen=tlen,
         title='Seismometer at the EXV and IXV, and GIFx',
         fname='ASD-EXV_IXV_GIFX_strain',
         labels1=labels11,
         labels2=labels12,
         adcnoise=True,
         selfnoise=True,
         unit='strain',
         trillium='120QA'                        
         )    
    

def main_yarm_comdiff():
    # Yアームの基線長伸縮
    diff = (eyy-ixy)/np.sqrt(2.0)
    comm = (eyy+ixy)/np.sqrt(2.0)
    data5 = [diff, # V
             comm, # V
             #adc # V
            ]
    labels51 = ['(Yend-Center)/sqrt(2) : Diff','(Yend+Center)/sqrt(2) : Com','--']
    labels52 = ['Com/Diff', 'None','ADC']
    plot21_cdmr(data5,
                start=start,                    
                tlen=tlen,
                title='Common Differential Mode Rate (CDMR) on the Y-Arm Bedrock',
                fname='cdmr_yarm',
                labels1=labels51,
                labels2=labels52,
                linestyle=['k-','k:','r-'],            
                adcnoise=True,
                selfnoiseplot=True,
                trillium='120QA',           
                )

    
def main_imc_comdiff():    
    # IMCの基線長伸縮を比較するためのデータセット        
    diff = (mciy-mcey)/np.sqrt(2.0)
    comm = (mciy+mcey)/np.sqrt(2.0)
    data2 = [diff, # V
             comm, # V
             #adc*c2V # V
             ] 
    labels21 = ['(MCiy-MCey)/sqrt(2) : Diff','(MCiy+MCey)/sqrt(2) : Com','---']
    labels22 = ['Com/Diff','Com/GIF','---']
    plot21_cdmr(data2,
                start=start,                    
                tlen=tlen,
                title='Common Differential Mode Rate (CDMR) on the IMC Bedrock',
                fname='cdmr_imc',
                labels1=labels21,
                labels2=labels22,
                L=20,
                linestyle=['k-','k:','r-'],            
                adcnoise=True,
                selfnoiseplot=True,
                trillium='compact',            
                )

    
def main_yarm_seis():
    # Yエンドとセンターの地震計
    fs = float(len(eyy)/tlen)
    data6 = [eyy,
             ixy,
             #adc*c2V
             ]
    labels61 = ['Yend','Center','ADC(Center)']
    labels62 = ['Yend','Center','ADC(Center)']
    plot(data6,
         start=start,             
         tlen=tlen,
         title='Seismometer at the EYV and IXV',
         fname='ASD-EYV_IXV',         
         labels1=labels61,
         labels2=labels62,
         adcnoise=True,
         selfnoise=True,
         trillium='120QA'
         )    
    print('asd eyv,ixv')
    plot21_coherence(data6,
                     start=start,                         
                     tlen=tlen,
                     title='Seismometer at the EYV and IXV',
                     fname='Coherence-EYV_IXV',         
                     labels1=labels61,
                     labels2=labels62,
                     adcnoise=True,            
                    )            
    
    
def main_imc_seis():    
    # MCi,MCeの地震計
    fs = float(len(mciy)/tlen)
    data4 = [mciy, # V
             mcey, # V
             #adc # V
             ]
    labels41 = ['MCi','MCe','ADC']
    labels42 = ['MCi','MCe','ADC']
    plot_timeseries(data4,
                    tlen=tlen,
                    title='Timeseries',
                    fname='Timeseries-MCi_MCe',
                    labels1=labels41,
                    labels2=labels42,
                    )
    
    
    plot(data4,
         start=start,             
         tlen=tlen,
         title='Seismometer at the MCi and MCe',
         fname='ASD-MCi_MCe',
         labels1=labels41,
         labels2=labels42,
         adcnoise=True,
         selfnoise=True,
         linestyle=['r-','b-'],
         trillium='compact'
         )
    print('asd mci,mce')  
    plot21_coherence(data4,
                     start=start,                         
                     tlen=tlen,
                     title='Seismometer at the MCi and MCe',
                     fname='Coherence-MCi_MCe',         
                     labels1=labels41,
                     labels2=labels42,
                     adcnoise=True,            
                     )   



    
if __name__ == '__main__':
    #start,end = get_time()
    tlen = 2**13
    start,end = 1217926818, 1217926818+tlen
    start,end = 1217935011, 1217943203
    start,end = 1217257218, 1217257218+tlen
    start,end = 1217170818, 1217170818+tlen
    start,end = 1219309218, 1219309218+tlen  # JST 2018-08-26T18:00:00
    #start,end = 1219309218, 1219309218+2**12  # JST 2018-08-26T18:00:00
    #
    exx = read(start,end,chname_dict['exx'])*deGain_120QA*c2V # Volt
    exy = read(start,end,chname_dict['exy'])*deGain_120QA*c2V # Volt
    exz = read(start,end,chname_dict['exz'])*deGain_120QA*c2V # Volt
    eyx = read(start,end,chname_dict['eyx'])*c2V # Volt
    eyy = read(start,end,chname_dict['eyy'])*c2V # Volt
    eyz = read(start,end,chname_dict['eyz'])*c2V # Volt
    ixx = read(start,end,chname_dict['ixx'])*c2V # Volt
    ixy = read(start,end,chname_dict['ixy'])*c2V # Volt
    ixz = read(start,end,chname_dict['ixz'])*c2V # Volt
    mcex = None
    mcey = read(start,end,chname_dict['mcey'])*deGain_compact*c2V # Volt
    mcez = read(start,end,chname_dict['mcez'])*deGain_compact*c2V # Volt
    mcix = None
    mciy = read(start,end,chname_dict['mciy'])*deGain_compact*c2V # Volt        
    mciz = read(start,end,chname_dict['mciz'])*deGain_compact*c2V # Volt
    gifx = read(start,end,chname_dict['gifx']) # strain
    diff = (exx-ixx)/np.sqrt(2.0) # Volt
    comm = (exx+ixx)/np.sqrt(2.0) # Volt
    #
    #
    exx = trillium120QA.V2Vel(exx)
    #
    # main
    #
    #main_xarm_comdiff(start,tlen,diff,comm,gifx)
    main_xarm_seis_asd(start,tlen,exx,ixx)
    #main_xarm_seis_timeseries(start,tlen,exx,ixx)
    
    exit()
    main_xarm_disp()        
    main_yarm_seis()
    main_yarm_comdiff()
    main_imc_comdiff()
    main_imc_seis()
