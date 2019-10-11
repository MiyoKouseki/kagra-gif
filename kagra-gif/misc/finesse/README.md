
Finesse:  Frequency domain INterfErometer Simulation SoftwarE

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.821363.svg)](https://doi.org/10.5281/zenodo.821363)

Daniel Brown and Andreas Freise 26.06.2017
http://www.gwoptics.org/finesse/


README
------------------------------------------------------------

Finesse [1] is a numeric simulation for laser interferometers 
using the frequency domain and Hermite-Gauss modes. It is open
source software distributed for OSX, Linux, and Windows. You
can download the binaries at:
    
    http://www.gwoptics.org/finesse/
    
The source code is available at:

    https://git.ligo.org/finesse/finesse/

This document gives a short overview of the main features of
Finesse. Please see the file INSTALL for information on
installing and running Finesse.


HOW TO CITE FINESSE
------------------------------------------------------------

For results using Finesse please cite the following DOI:

@misc{finesse,
  author       = {Brown, Daniel David and
                  Freise, Andreas},
  title        = {Finesse},
  month        = may,
  year         = 2014,
  note         = {{You can download the binaries and source code at 
                   \url{http://www.gwoptics.org/finesse}.}},
  doi          = {10.5281/zenodo.821363},
  url          = {http://www.gwoptics.org/finesse}
}


Table of Contents:
------------------------------------------------------------

    1. Interferometer signals
    2. Beam geometry and imaging 
    3. Documentation, support and examples
    4. Examples of the impact of Finesse on commissioning tasks
    5. Finesse with Python and MATLAB
    6. References

------------------------------------------------------------


1. Interferometer signals
------------------------------------------------------------

Finesse can be used to compute a great variety of interferometer
signals for control systems, including longitudinal control, 
alignment control and thermal compensation, for example:

- transfer functions and error signals using up to five 
  demodulations per photodiode.
- detectors for amplitude, phase, intensity (all three can be 
  given integrated over the beam or as CCD-like images), user- 
  defined split detectors
- noise propagations, such as laser frequency noise or oscillator
  phase noise
- quantum noise and radiation pressure effects such as optical
  springs

2. Beam geometry and imaging 
------------------------------------------------------------

One of the main features of Finesse is the extensive integration
of physics related to the beam shape. This makes it possible to 
study interferometer signals in the presence of defects such as 
misalignments and mode mismatch, mirror surface defects, thermal 
deformations and mis-centred, split photo detectors.

Finesse can also model imaging properties of optical systems,
for example, it automatically determines eigenmodes of cavities 
and interferometers. Gouy phases and beam waist positions can be 
plotted as functions of positions of optical elements.


3. Documentation, support and examples
------------------------------------------------------------

The program is easy to use for students: For the basic use, including
graphical output, no commercial software is required. The implemented 
physics is well documented in a 200 pages manual. Simple examples are 
provided as well as detailed input files for all main interferometric 
gravitational-wave detectors. The manual and examples can be found on
the main Finesse page at http://www.gwoptics.org/finesse/

In addition we provide resources and self-study material on laser
interferometry in the form of Jupyter notebooks using Finesse
simulations: http://www.gwoptics.org/learn/

For questions and discussions related to Finesse we are hosting
a mailing in Birmingham and LIGO chat channel. Instructions on how
to join these are provided at:
https://git.ligo.org/finesse/finesse/wikis/home

The simulation code has been developed and improved continuously 
over the last ten years. It has been frequently and successfully
tested against experimental data from GEO 600, LIGO and Virgo.
The code is under version control and is executed within a nightly
test-suite to maintain stability during the ongoing development.


4. Examples of Finesse usage for commissioning tasks
------------------------------------------------------------

The following examples highlight Finesse analyses of pressing problems 
in detector commissioning. Finesse predictions have been used to 
improve the detector performance and the Finesse results have been 
shown to match experimental results:

- lock acquisition of the power-recycled GEO 600 interferometer:
  a suspension tilt instability was discovered as the source of 
  severely distorted interferometer error signals [2]

- thermal compensation of GEO 600: a wrong radius of curvature was 
  discovered to cause unexpected beam patterns in the dark fringe. 
  Finesse results for the beam pattern as a function of heater power 
  were used to find the current operating point of the thermal 
  compensation. [3]

- detector characterisation of the Virgo arm cavities: Finesse has 
  been used to characterise all details of the Virgo north arm 
  cavity from the cavity Finesse to the astigmatism of the mode 
  matching telescope. [4]

- thermal lensing induced bi-stable operating point in Virgo: Finesse 
  results were crucial in understanding the origins of a double zero
  crossing in a longitudinal error signal of Virgo. [5]

- RF modulation induced change in interferometer noise couplings:
  Detailed measurements and Finesse simulations were used to 
  understand the laser power noise coupling due to RF sidebands in 
  higher order modes and how it limits the detector sensitivity. [6]

- simulations of the alignment control signal of the Advanced LIGO 
  input mode cleaner [7]

- Advanced LIGO commissioning investigation into power loss at the 
  central beam-splitter [8]


5. Finesse with Python and MATLAB
------------------------------------------------------------

Finesse is a stand-alone executable written in C. It is, however,
well interfaced with Python and MATLAB. A number of MATLAB tools 
(m files and mex files) are provided to run Finesse simulations 
from MATLAB or to communicate with a running Finesse process from 
within MATLAB. In addition a new suite of Python tools called
PyKat (http://www.gwoptics.org/pykat/) is available to interact
with Finesse from Python.

6. References
------------------------------------------------------------

[1] A. Freise, G. Heinzel, H. Lueck, R. Schilling, B. Willke and 
    K. Danzmann, "Frequency-domain interferometer simulation with 
    higher-order spatial modes", Classical and Quantum Gravity, Vol.21, 
    (2004), available at http://www.gwoptics.org/finesse

[2] A. Freise: "The Next Generation of Interferometry: Multi-Frequency 
    Optical Modeling, Control Concepts and Implementation", Ph.D. 
    Thesis, University of Hannover (2003), 
    http://www.amps.uni-hannover.de/dissertationen/freise_diss.pdf

[3] H. Lueck, A. Freise, S. Gossler, S. Hild, K. Kawabe and K. Danzmann, 
    "Thermal correction of the radii of curvature of mirrors for 
    GEO 600", Classical and Quantum Gravity, Vol.21, (2004)

[4] A. Freise, M. Loupias : "The VIRGO north arm cavity: Examples for 
    the use of the interferometer simulation Finesse", VIRGO note 
    VIR-NOT-EGO-1390-269 (2004)

[5] J. Marque: 'Input mirrors thermal lensing effect Frequency 
    modulation PRCL length in Virgo' talk at LSC meeting, LIGO 
    document number LIGO-G070338-00-Z (2007)

[6] J. R. Smith, J. Degallaix, A. Freise, H. Grote, M. Hewitson, 
    S. Hild, H. Lueck, K. A. Strain and B. Willke, "Measurement 
    and simulation of laser power noise in GEO 600", Classical 
    and Quantum Gravity, Vol.25, (2008)

[7] K. Kokeyama, K. Arai, P. Fulda, S. Doravari, L. Carbone, 
    D. Brown, C. Bond and A. Freise, ‘Finesse simulation for the 
    alignment control signal of the aLIGO in- put mode cleaner’, 
    LIGO note T1300074, https://dcc.ligo.org/LIGO-T1300074, (2013)

[8] C. Bond, P. Fulda, D. Brown and A. Freise: ‘Investigation of beam 
    clipping in the Power Recycling Cavity of Advanced LIGO using Finesse’, 
    LIGO note T1300954, https://dcc.ligo.org/LIGO-T1300954, (2013)
    
[9] D. Brown, R. J. E. Smith, and A. Freise:
    Fast simulation of Gaussian-mode scattering for precision interferometry
    Journal of Optics, 2016, http://stacks.iop.org/2040-8986/18/i=2/a=025604
    
[10] Daniel David Brown
     Interactions of light and mirrors: advanced techniques for modelling
     future gravitational wave detectors
     Ph.D. thesis, University of Birmingham, 2016
     https://doi.org/10.5281/zenodo.821380
     