#import numpy as np
from event import (get_catalog, get_eventids, get_eventtimes,
                   get_eventdepths, get_eventmags,
                   calc_distance_from_eq, get_arrivals, get_eventgps,
                   )
from main import make_eventcsv
from plot import (main_plot_eqmap, plot_arrivals)
from arrival import get_first_arrival_times

import numpy as np
import pandas as pd
   

    
if __name__=='__main__':
    kwargs = {}
    kwargs['minmagnitude'] = 7
    #kwargs['minlatitude'] = 0
    #kwargs['maxlatitude'] = 45
    #kwargs['minlongitude'] = 120
    #kwargs['maxlongitude'] = 180
    #kwargs['maxmagnitude'] = 8    
    start_str = '2018-09-01'
    end_str = '2018-11-01'
    main_plot_eqmap(start_str,end_str,**kwargs)
    #df = make_eventcsv(start_str,end_str,to_csv=True,**kwargs)
    #plot_arrivals(eventid=10953070)    
    #print df
