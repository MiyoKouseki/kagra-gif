from event import (get_catalog, get_eventids, get_eventtimes,
                   get_eventdepths, get_eventmags,
                   calc_distance_from_eq, get_arrivals, get_eventgps,
                   )
from arrival import (get_first_arrival_times,get_incidentangles, filt_arrivals)
import pandas as pd
import numpy as np



def make_eventcsv(start_str,end_str,**kwargs):
    '''

    Parameters
    ----------


    Returns
    -------
    df : 

    '''
    to_csv = kwargs.pop('to_csv',False)
    csv_fname = kwargs.pop('csv_fname','tmp.csv')
    phase_list = kwargs.pop('phase_list','P')
    
    # get catalog
    catalog = get_catalog(start_str,end_str,**kwargs)
    
    # get some information from catalog
    eventids = get_eventids(catalog)
    eventtimes = get_eventtimes(catalog)
    eventgps = get_eventgps(catalog)
    eventdepths = get_eventdepths(catalog)
    eventmags = get_eventmags(catalog)
    eventdists,eventazimuthA2Bs,eventazimuthB2As = calc_distance_from_eq(catalog)
    arrivals_list = get_arrivals(catalog,phase_list=phase_list)
    pwave_first_arrival_times = get_first_arrival_times(arrivals_list,phase_list='P')
    pwave_first_arrival_gps = eventgps + pwave_first_arrival_times
    incident_angles = get_incidentangles(arrivals_list,first_arrival=True)
    
    # make pandas dataframe
    df = pd.DataFrame(data=np.asarray([eventids,
                                       eventtimes,
                                       eventgps,
                                       pwave_first_arrival_gps,
                                       eventmags,
                                       eventdists,
                                       eventdepths,
                                       eventazimuthB2As,
                                       incident_angles]
                                      ).T ,
                      columns=['EventId',
                               'EventTime[UTC]',
                               'EventGPS',
                               'PwaveFirstArrivalGPS',
                               'EventMagnitude',
                               'EventDistance[km]',
                               'EventDepth[km]',
                               'EventAzimuthA2B[degree]',
                               'EventIncidentAngle[degree]']
                      )    
    if to_csv:
        df.to_csv(csv_fname,sep=",",index=False)        
    return df



