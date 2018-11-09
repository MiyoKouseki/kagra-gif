
from obspy.clients.fdsn import Client
from obspy.core.event import Catalog
from obspy import UTCDateTime

from obspy.taup import TauPyModel
from obspy.geodetics.base import gps2dist_azimuth

from gwpy.time import to_gps

from numpy import asarray,vectorize
import numpy as np 

from functools import partial

def get_catalog(starttime,endtime,base_url='IRIS',_catalog='NEIC PDE',**kwargs):
    ''' Get catalog in specified time


    Parameters
    ----------
    starttime : str
        start time.

    endtime : str
        end time
    
    base_url : str, optional
        base url. default is 'IRIS'
        
    catalog : str, optional
        catalog


    Returns
    -------
    catalog : `obspy.core.event.catalog.Catalog'

    '''
    client = Client(base_url)
    starttime = UTCDateTime(starttime)
    endtime = UTCDateTime(endtime)
    catalog = client.get_events(starttime=starttime,
                                endtime=endtime,
                                catalog=_catalog,**kwargs)
    return catalog


def calc_distance_from_eq(catalog,lat_0=36.43,lon_0=137.31,**kwargs):
    '''

    Parameters
    ----------
    catalog : `obspy.core.event.catalog.Catalog'
        catalog.
    
    lat_0 : float, optional
        latitude of home location. default is kamioka; 36.43.

    lon_0 : float, optional
        longitude of home location. default is kamioka; 137.31.


    Returns
    -------
    

    '''
    
    lat_eq = [event.origins[0].latitude for event in catalog]
    lon_eq = [event.origins[0].longitude for event in catalog]
    lon_0 = [lon_0]*len(catalog)
    lat_0 = [lat_0]*len(catalog)

    vfunc = vectorize(gps2dist_azimuth)
    dist,degreeA2B,degreeB2A = vfunc(lat_eq, lon_eq,lat_0, lon_0)
    return dist/1e3, degreeA2B, degreeB2A


def get_arrivals(*args,**kwargs):
    #def get_arrivals(model='iasp91',phase_list=['P'],*args,**kwargs):    
    #def get_arrivals(depth,degree,model='iasp91',phase_list=['P'],**kwargs):
    ''' Get arrivals with depth and degree    
    

    Prameters
    ---------
    *arg : arguments 
        * 1 : `obspy.core.event.catalog.Catalog' : catalog
        * 2 : `depth, degree` : (depth, degree)
    
    Returns
    -------
    arrivals : list of `obspy.taup.tau.Arrivals`
        obspy arrivals.

        
    '''
    N = len(args)
    if N == 2:
        depth, degree = args
    elif N == 1 and isinstance(args[0],Catalog):
        catalog = args[0]
        depth = get_eventdepths(catalog)
        _, degree, _ = calc_distance_from_eq(catalog)        
    else:
        raise ValueError('`arg` error')

    
    if len(depth)!=len(degree):
        raise ValueError(' {0} != {1}'.format(len(depth),len(degree)))
    
    _model = kwargs.pop('model','iasp91')
    model = TauPyModel(model=_model)       
    mapfunc = partial(model.get_ray_paths, **kwargs)
    arrivals = map(mapfunc,depth,degree)
    return arrivals


def get_eventids(cls):
    '''

    Parameters
    ----------
    cls : `obspy.core.event.catalog.Catalog'
        catalog

    Returns
    -------
    eventids : lisst of str
        eventids

    '''
    eventids = [event.resource_id.id.split('=')[-1] for event in cls]    
    return eventids


def get_eventtimes(cls):
    '''

    Parameters
    ----------
    cls : `obspy.core.event.catalog.Catalog'
        catalog


    Returns
    -------
    eventtimes : lisst of `obspy.core.utcdatetime.UTCDateTime`
        eventtimes

    '''
    eventtimes = [event.origins[0].time for event in cls]
    return eventtimes


def get_eventdepths(cls):
    '''

    Parameters
    ----------
    cls : `obspy.core.event.catalog.Catalog'
        catalog


    Returns
    -------
    eventdepth : lisst of float
        eventdepth

    '''
    eventdepth = [event.origins[0].depth/1e3 for event in cls] # km    
    return eventdepth


def get_eventmags(cls):
    '''

    Parameters
    ----------
    cls : `obspy.core.event.catalog.Catalog'
        catalog


    Returns
    -------
    eventmags : lisst of float
        event magnitude

    '''
    eventmags = [event.magnitudes[0].mag for event in cls]
    return eventmags


def get_eventgps(cls):
    '''

    Parameters
    ----------
    cls : `obspy.core.event.catalog.Catalog'
        catalog


    Returns
    -------
    eventgps : lisst of `LIGOTimeGPS`
        the number of GPS seconds (non-integer) since the start of the
        epoch (January 6 1980).

    '''
    
    eventtimes = get_eventtimes(cls)
    datetime = [eventtime.datetime for eventtime in eventtimes]
    vfunc = vectorize(to_gps,otypes=[np.float])
    eventgps = vfunc(datetime)
    return eventgps
