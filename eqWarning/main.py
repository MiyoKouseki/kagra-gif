from event import (get_catalog, get_eventids, get_eventtimes,
                   get_eventdepths, get_eventmags,
                   calc_distance_from_eq, get_arrivals, get_eventgps,
                   )
from arrival import get_first_arrival_times
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
    
    # get catalog
    catalog = get_catalog(start_str,end_str,**kwargs)
    
    # get some information from catalog
    eventids = get_eventids(catalog)
    eventtimes = get_eventtimes(catalog)
    eventdepths = get_eventdepths(catalog)
    eventmags = get_eventmags(catalog)
    eventdists,eventdegA2Bs,eventdegB2As = calc_distance_from_eq(catalog)
    arrivals = get_arrivals(catalog,phase_list=['ttbasic'])
    pwave_first_arrival_times = get_first_arrival_times(arrivals,phase_name='P')
    eventgps = get_eventgps(catalog)
    pwave_first_arrival_gps = eventgps + pwave_first_arrival_times

    # make pandas dataframe
    df = pd.DataFrame(data=np.asarray([eventids,
                                       eventtimes,
                                       eventgps,
                                       pwave_first_arrival_gps,
                                       eventmags,
                                       eventdists,
                                       eventdepths,
                                       eventdegA2Bs]
                                      ).T ,
                      columns=['EventId',
                               'EventTime[UTC]',
                               'EventGPS',
                               'PwaveFirstArrivalGPS',
                               'EventMagnitude',
                               'EventDistance[km]',
                               'EventDepth[km]',
                               'EventDegreeA2B[degree]']
                      )    
    if to_csv:
        df.to_csv(csv_fname,sep=",",index=False)        
    return df



