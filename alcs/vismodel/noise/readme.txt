*OSEMnoiseworstproto_disp.dat
 The worst measured noise level of prototype OSEMs in [um/rtHz].
 The reference xml file can be found in TAMA standalone (133.40.117.66):
 /users/user_20m/sekiguchi/payload_k1visproto/140919_LOCKED_OSEM_FFT.xml

*LVDTnoiseworstproto_disp.dat
 The worst measured noise level of prototype LVDTs in [um/rtHz].
 We assume calibration factor of 1400 [ct/mm].
 The reference xml file can be found in TAMA standalone (133.40.117.66):
 /users/user_20m/sekiguchi/LVDT/130405_LVDT_noise_act.xml

*GEOnoiseproto_vel.dat
 The noise level of geophone preamp in [um/sec/rtHz],
 but the decrease of geophone response at low freqencies is not compensated.

*KamiokaSeismicHighNoise.dat
 Kamioka seismic spectrum in [m/rtHz].
 The low frequency part (<2 Hz) is measured by CMG-3T and 90% pertile
 of 1.5 years measurement is taken. The high frequency part is interpolation
 with a function proportional to f^-2.
 (29/06/2015 updated: < 30 mHz the magnitude is set constant)

*LVDTnoiseADC_disp.dat
 The noise level of LVDTs in [um/rtHz], assuming that the noise is limited by the ADC noise.
 We assume calibration factor of 1400 [ct/mm].