
from scipy.signal import iirdesign

fs = 16
nyq = fs/2.0

low = lowcut/nyq

wp = low
ws = low*1.5
gpass = 0.1
gstop = 60

ba_lowpass = iirdesign(wp,ws,gpass,gstop)
