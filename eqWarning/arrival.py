import warnings
from functools import partial
from obspy.taup.tau import Arrivals
from numpy import vectorize
import numpy as np

def get_first_arrival_times(arrivals_list,**kwargs):
    '''
    '''
    vfunc = vectorize(_get_first_arrival_time,
                      excluded=['phase_list'],otypes=[np.float])
    first_arrival_times = vfunc(arrivals_list,**kwargs)
    return first_arrival_times


def filt_arrivals(arrivals_list,**kwargs):
    '''
    '''
    vfunc = vectorize(_filt_arrivals,excluded=['phase_list'])
    filt_arrivals = vfunc(arrivals_list,**kwargs)
    return filt_arrivals


def _get_first_arrival_time(arrivals,**kwargs):
    '''
    '''
    try:
        _arrivals = _filt_arrivals(arrivals,**kwargs)
        _arrivals.sort(key=lambda arrival:arrival.time,reverse=False)
        first_arrival_time = _arrivals[0].time
    except IndexError:
        phase_list = kwargs.pop('phase_list')
        message = "There are no {0}-phase. then, "\
                  "return None value".format(phase_list,arrivals)
        warnings.warn(message)            
        return np.nan
        
    return first_arrival_time


def _filt_arrivals(arrivals,**kwargs):
    ''' filt arrivals

    Parameters
    ----------
    arrivals : `Arrivals`
    
    phase_name : str, optional
        default is only 'P' phase


    Returns
    -------
    filt_arrivals : `Arrivals`    
    '''
    phase_list = kwargs.pop('phase_list','P')
    filt_phase = lambda arrival,phase_list:arrival.name == phase_list
    _list = filter(partial(filt_phase, phase_list=phase_list),arrivals)
    filt_arrivals = Arrivals(_list,model=arrivals.model)    
    return filt_arrivals


def get_incidentangles(arrivals_list,**kwargs):
    first_arrival = kwargs.pop('first_arrival',True)
    vfunc = vectorize(_get_incidentangles,otypes=[object])
    angles = vfunc(arrivals_list,**kwargs)
    return angles


def _get_incidentangles(arrivals,**kwargs):

    if not arrivals:
        return np.nan
    
    first_arrival = kwargs.pop('first_arrival',True)
    if first_arrival:
        arrivals.sort(key=lambda arrival:arrival.time,reverse=False)        
        angles = arrivals[0].incident_angle
    else:
        angles = np.asarray([arrival.incident_angle for arrival in arrivals])

    return angles
