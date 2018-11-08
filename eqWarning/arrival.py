import warnings
from functools import partial
from obspy.taup.tau import Arrivals
from numpy import vectorize
import numpy as np

def get_first_arrival_times(arrivals_list,phase_name='P'):
    '''
    '''
    vfunc = vectorize(_get_first_arrival_time,excluded=['phase_name'],otypes=[np.float])
    first_arrival_times = vfunc(arrivals_list)    
    return first_arrival_times


def _get_first_arrival_time(arrivals,phase_name='P'):
    '''
    '''
    
    filt_phase = lambda arrival,phase_name:arrival.name == phase_name
    try:
        _arrivals = Arrivals(filter(partial(filt_phase, phase_name=phase_name),
                                   arrivals),model=arrivals.model)    
        _arrivals.sort(key=lambda arrival:arrival.time,reverse=False)
        first_arrival_time = _arrivals[0].time
    except IndexError:
        message = "There are no {0}-phase. then, "\
                  "return None value".format(phase_name,arrivals)
        warnings.warn(message)            
        return np.nan
        
    return first_arrival_time

    

## momo
# when you filt only P-wave
