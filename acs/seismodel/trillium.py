from gwpy.frequencyseries import FrequencySeries
from control import matlab
from miyopy.utils.trillium import selfnoise

tr120 = matlab.tf(*matlab.zpk2tf([0,0,-31.63,-160.0,-350.0,-3177.0],
                                 [-0.036614+0.037059j,-0.036614-0.037059j,
                                      -32.55,-142.0,
                                      -364.0+404.0j,-364.0-404.0j,
                                      -1260.0,
                                      -4900.0+5200.0j,-4900.0-5200.0j,
                                      -7100.0+1700.0j,-7100.0-1700.0j,
                                    ],
                                     1202.5*8.31871e17)
                      )

tr120_u = matlab.tf(*matlab.zpk2tf([0,0,-31.63,-160.0,-350.0,-3177.0],
                                   [-0.036614+0.037059j,-0.036614-0.037059j,
                                        -32.55,-142.0,
                                        -364.0+404.0j,-364.0-404.0j,
                                        -1260.0,
                                        -4900.0+5200.0j,-4900.0-5200.0j,
                                        -7100.0+1700.0j,-7100.0-1700.0j,
                                   ],
                                       8.31871e17)
                    )

f,selfnoise = selfnoise(trillium='120QA',psd='ASD',unit='disp')
tr120_selfnoise = FrequencySeries(selfnoise,frequencies=f)

plottr120 = False
if plottr120:
    fig ,[ax0,ax1] = plt.subplots(2,1)
    ax0.loglog(freq,mag_tr120_u,'b-',label='Trillium120QA')
    ax0.set_xlim(1e-3,2e2)
    ax0.grid(b=True, which='major', color='gray', linestyle=':')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax0.legend(loc='lower left')
    ax0.set_ylabel('Magnitude ')    
    ax1.semilogx(freq,phase_tr120,'b-')
    ax1.set_ylim(-180,180)
    ax1.set_yticks(np.arange(-180,181,90))
    ax1.set_xlim(1e-3,2e3)
    ax1.set_xlabel('Frequency [rad Hz]')
    ax1.set_ylabel('Phase [degree]')
    ax1.grid(b=True, which='major', color='gray', linestyle=':')
    ax1.grid(b=True, which='minor', color='gray', linestyle=':')
    plt.savefig('img_trillium120QA.png')


    
