import numpy as np
from scipy.special import jv
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeriesDict,TimeSeries

'''


'''

def main(chnames,start,end,
         check_timeseries=False,
         check_velocity=False,check_reduction_rate=True):
    # ----------------------------------------
    # TimeSeries Data from nds
    # ----------------------------------------
    datadict = TimeSeriesDict.fetch(chnames,start,end,host='10.68.10.121',
                                    verbose=True,port=8088)
    try:
        ts_eyv = datadict['K1:PEM-SEIS_EYV_GND_EW_IN1_DQ']
        ts_exv = datadict['K1:PEM-SEIS_EXV_GND_EW_IN1_DQ']
        ts_ixv = datadict['K1:PEM-SEIS_IXV_GND_EW_IN1_DQ']
        ts_bs = datadict['K1:PEM-SEIS_BS_GND_EW_IN1_DQ']
        ts_mcf = datadict['K1:PEM-SEIS_MCF_GND_EW_IN1_DQ']        
    except KeyError as e:
        print('''KeyError: Channel name not found, {0}. Please check this channel name.'''.format(e))
        exit()
    except Exception as e:
        print('Unexpected Error!!')
        print(e)
        exit()
    if check_timeseries:
        for data in datadict.values():
            plot = data.rms().plot()        
            plot.savefig('./{0}/img_TimeSeries_RMS_{1}.png'.format(segname,data.name))
            print('./{0}/img_TimeSeries_RMS_{1}.png'.format(segname,data.name))
            plot.close()
    # ----------------------------------------
    # Coherence
    # ----------------------------------------
    fftlength = 2**7
    csd3000 = ts_exv.csd(ts_ixv,fftlength=fftlength,overlap=fftlength/2.0) # CSD
    csd30 = ts_mcf.csd(ts_bs,fftlength=fftlength,overlap=fftlength/2.0) # CSD
    csd60 = ts_mcf.csd(ts_ixv,fftlength=fftlength,overlap=fftlength/2.0) # CSD 
    exv = ts_exv.asd(fftlength=fftlength,overlap=fftlength/2.0) # ASD
    ixv = ts_ixv.asd(fftlength=fftlength,overlap=fftlength/2.0) # ASD
    mcf = ts_mcf.asd(fftlength=fftlength,overlap=fftlength/2.0) # ASD
    bs = ts_bs.asd(fftlength=fftlength,overlap=fftlength/2.0) # ASD
    coh3000 = np.real(csd3000)/exv/ixv # Re[coh]
    coh30 = np.real(csd30)/mcf/bs # Re[coh]
    coh60 = np.real(csd60)/mcf/ixv # Re[coh]

    # ----------------------------------------
    # SPAC model
    # ----------------------------------------
    freq = np.logspace(-3,2,1e4)
    w = 2.0*np.pi*freq
    L_ixv2exv = 3000.0
    L_mcf2bs = 22.0
    L_mcf2ixc = 62.0
    L_mcf2ixv = 62.0 # guess
    L_mcf2mce = 22.0
    #cp = 5500.0 # m/sec
    #cr = 2910 # m/sec
    L_KAGRA = 3000.0
    L_Virgo = 4000.0
    cr_virgo = lambda f: 150.0+1000.0*np.exp(-f/1.5) # from M. Beker PhD thesis.
    cr_kagra = lambda f: 800.0+3000.0*np.exp(-f/1.5) # by eye
    cr_kagra_x = lambda f: 2200.0+3000.0*np.exp(-f/1.5) # by eye
    cp_kagra_x = lambda f: 5400.0*np.ones(len(f))    
    spac = lambda f,c,L: np.real(jv(0,L*2.0*np.pi*f/c))
    spac_kagra = lambda f,L: spac(f,cr_kagra(f),L)
    spac_kagra_p = lambda f,L: spac(f,cp_kagra_x(f),L)
    spac_kagra_r = lambda f,L: spac(f,cr_kagra_x(f),L)
    reduction = lambda f,c,L: 1.0-np.real(jv(0,L*2.0*np.pi*f/c))

    # ----------------------------------------
    # ASD
    # ----------------------------------------
    from miyopy.utils.trillium import Trillium    
    tr120q = Trillium('120QA')
    trcpt = Trillium('compact')
    v2vel_120 = tr120q.v2vel
    v2vel_cpt = trcpt.v2vel
    c2v = 20.0/2**15
    print c2v
    amp = 10**(30.0/20.0)
    #ixv = v2vel_120(ixv*c2v)/amp
    #exv = v2vel_120(exv*c2v)/amp
    #mcf = v2vel_cpt(mcf*c2v)/amp
    #bs = v2vel_cpt(bs*c2v)/amp        
    if True:        
        fig, ax = plt.subplots(1,1,figsize=(8,6))
        if 'UD' in ts_ixv.name:
            plt.title(segname.replace('_','\_')+', ASD'+', Z')
        elif 'EW' in ts_ixv.name:
            plt.title(segname.replace('_','\_')+', ASD'+', X')
        ax.loglog(ixv,label='ixv')
        ax.loglog(exv,label='exv')
        ax.loglog(mcf,label='mcf')
        ax.loglog(bs,label='bs')
        ax.set_xlim(0.01,100)
        ax.set_xlabel('Frequency [Hz]')
        ax.set_ylabel('Count')
        ax.legend()
        if 'UD' in ts_ixv.name:
            plt.savefig('./{0}/img_ASD_Z.png'.format(segname))
            print('saved ./{0}/img_ASD_Z.png'.format(segname))
        elif 'EW' in ts_ixv.name:
            plt.savefig('./{0}/img_ASD_X.png'.format(segname))
            print('saved ./{0}/img_ASD_X.png'.format(segname))            
        plt.close()
        

    # ------------------------------------------
    # Spatial autocorrection (SPAC) 
    # ------------------------------------------
    if 'UD' in ts_ixv.name:
        fig, ax = plt.subplots(1,1,figsize=(8,6))
        plt.title(segname.replace('_','\_')+', SPAC')
        ax.axvspan(0.01, 0.1, alpha=0.2, color='gray')
        ax.axvspan(2, 100, alpha=0.2, color='gray')
        ax.semilogx(coh3000,'r',label='3000 m ')
        ax.semilogx(freq,spac_kagra(freq,3000.0),'k--',label='3000 m model')
        ax.semilogx(coh30,'b',label='22 m')
        ax.semilogx(freq,spac_kagra(freq,22.0),'k--',label='3000 m model')
        #ax.semilogx(coh60,'g',label='60 m ')
        #ax.semilogx(freq,spac_kagra(freq,62.0),'k--',label='60 m model')        
        ax.set_ylim(-1.1,1.1)
        ax.set_xlim(0.01,20)
        ax.set_xlabel('Frequency [Hz]')
        ax.set_ylabel('Coherence')
        ax.set_yticks(np.arange(-1.0,1.1,0.5))
        ax.text(110, -1.1, 'START : {0}'.format(start), rotation=90,
                ha='left',va='bottom')
        ax.legend()
        plt.savefig('./{0}/img_SPAC.png'.format(segname))
        print('saved ./{0}/img_SPAC.png'.format(segname))
        plt.close()
    # ------------------------------------------
    # Spatial autocorrection (SPAC) X
    # ------------------------------------------
    if 'EW' in ts_ixv.name:
        fig, ax = plt.subplots(1,1,figsize=(8,6))
        plt.title(segname.replace('_','\_')+', X')
        ax.axvspan(0.01, 0.1, alpha=0.2, color='gray')
        ax.axvspan(1.5, 100, alpha=0.2, color='gray')        
        ax.semilogx(coh3000,'r',label='3000 m ')
        ax.semilogx(freq,spac_kagra_r(freq,3000.0),'k--',label='3000 m model')
        ax.semilogx(freq,spac_kagra_p(freq,3000.0),'g--',label='3000 m model (p)')
        ax.semilogx(coh30,'b',label='22 m')
        ax.semilogx(freq,spac_kagra_r(freq,22.0),'k--',label='22 m model')
        ax.semilogx(freq,spac_kagra_p(freq,22.0),'g--',label='22 m model (p)')        
        #ax.semilogx(coh60,'g',label='60 m ')
        #ax.semilogx(freq,spac_kagra_x(freq,62.0),'k--',label='60 m model')        
        ax.set_ylim(-1.1,1.1)
        ax.set_xlim(0.01,20)
        ax.set_xlabel('Frequency [Hz]')
        ax.set_ylabel('Coherence')
        ax.set_yticks(np.arange(-1.0,1.1,0.5))
        ax.text(110, -1.1, 'START : {0}'.format(start), rotation=90,
                ha='left',va='bottom')
        ax.legend()
        plt.savefig('./{0}/img_SPAC_X.png'.format(segname))
        print('saved ./{0}/img_SPAC_X.png'.format(segname))
        plt.close()
        

    # ------------------------------------------
    # Reyleigh wave velocity in KAGRA and Virgo
    # ------------------------------------------
    if check_velocity:    
        fig, ax = plt.subplots(1,1,figsize=(7,6))
        plt.title('Phase Velocity of Rayleigh Wave',fontsize=25)
        ax.loglog(freq,cr_virgo(freq),'k',label='Virgo')
        ax.loglog(freq,cr_kagra(freq),'r',label='KAGRA (Vertical)')
        ax.loglog(freq,cr_kagra_x(freq),'r--',label='KAGRA (Horizontal)??')
        ax.loglog(freq,cp_kagra_x(freq),'r:',label='ref. KAGRA P-wave')
        ax.set_xlabel('Frequency [Hz]')
        ax.set_ylabel('Velocity [m/s]')
        ax.set_ylim(100,10e3)
        ax.set_xlim(1e-3,100)
        ax.legend(fontsize=15)
        plt.savefig('./{0}/img_RwaveVelocity.png'.format(segname))
        print('saved ./{0}/img_RwaveVelocity.png'.format(segname))
        plt.close()
        
    # ----------------------------------
    # Reduction Rate of arm displacement in KAGRA and Virgo 
    # ----------------------------------
    if check_reduction_rate:
        fig, ax = plt.subplots(1,1,figsize=(7,6))
        plt.title('Displacement Reduction of the Bedrock',fontsize=25)
        ax.loglog(freq,reduction(freq,cr_virgo(freq),L_Virgo),'k',label='Virgo (Z velo.)')
        ax.loglog(freq,reduction(freq,cr_kagra_x(freq),L_KAGRA),'r',label='KAGRA (X velo.)')
        ax.set_xlim(0.01,20)
        ax.set_ylim(1e-3,2)
        ax.legend(fontsize=15)
        ax.set_xlabel('Frequency [Hz]')
        ax.set_ylabel('Reduction Rate')
        plt.savefig('./{0}/img_ReductionRate.png'.format(segname))
        print('saved ./{0}/img_ReductionRate.png'.format(segname))
        plt.close()
        

if __name__ == '__main__':
    # ----------------------------------------
    # Parse Arguments
    # ----------------------------------------
    import argparse 
    parser = argparse.ArgumentParser(description='description')
    parser.add_argument('segnames',nargs='*',
                        help='data name which you want to calculate')
    args = parser.parse_args()
    segnames = args.segnames        
    # ----------------------------------------
    # Data Segments
    # ----------------------------------------
    segments = {'ER1_0':(1244004884.875,1244010528), # BAD DAQ,  
                'ER1_1':(1244013088,1244018445.1875), # 
                'ER1_2':(1243999747.25,1244004703.125), # EQ
                'ER1_3':(1244010624,1244012140.6875), # 
                'ER1_4':(1244018493.375,1244019618),
                'JUN09_00':(1244041218,1244041218+3*3600), # JST 00:00 - 03:00
                'JUN10_00':(1244127618,1244127618+3*3600), # JST 00:00 - 03:00
                'JUN11_03':(1244311218,1244311218+3*3600), # JST 03:00 - 05:00
                'JUN13_00':(1244386818,1244386818+3*3600), # JST 00:00 - 03:00
                'JUN14_00':(1244473218,1244473218+3*3600), # JST 00:00 - 03:00
                    }        
    # ----------------------------------------
    # Channel List
    # ----------------------------------------
    chnames = ['K1:PEM-SEIS_IXV_GND_EW_IN1_DQ',
               'K1:PEM-SEIS_EXV_GND_EW_IN1_DQ',
               'K1:PEM-SEIS_EYV_GND_EW_IN1_DQ',
               'K1:PEM-SEIS_MCF_GND_EW_IN1_DQ',
               'K1:PEM-SEIS_BS_GND_EW_IN1_DQ',]        
    # ----------------------------------------
    # Main function
    # ----------------------------------------
    print(segnames)    
    segname = segnames[0]
    start = segments[segname][0]
    end = segments[segname][1]
    main(chnames,start,end,check_reduction_rate=True,check_velocity=True)    
    for segname in segnames[1:]:
        start = segments[segname][0]
        end = segments[segname][1]
        main(chnames,start,end)
