import matplotlib.pyplot as plt
from matplotlib import colorbar,colors
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable

from numpy import asarray
from distutils.version import StrictVersion


import mpl_toolkits.basemap as basemap
_basemap_version = basemap.__version__
if StrictVersion(_basemap_version) <= StrictVersion('1.1.0'):
    print 'this basemap is old {0}'.format(_basemap_version)
    import warnings
    import matplotlib.cbook
    warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


from event import get_arrivals    


def plot_eqmap(catalog,lat_0=36.43,lon_0=137.31,radius=None,title='None',**kwargs):
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
    # get data from catalog
    #origin = catalog[0].origins[0]
    eq_lat = [event.origins[0].latitude for event in catalog]
    eq_lon = [event.origins[0].longitude for event in catalog]
    eq_depth = asarray([event.origins[0].depth for event in catalog])/1e3 # km
    eq_mag = asarray([event.magnitudes[0].mag for event in catalog])
    #print len(eq_lat),len(eq_lon),len(eq_depth),len(eq_mag)
    
    # setup figure, axes
    fig,ax1 = plt.subplots(1,1,figsize=(8,8))
    fig.subplots_adjust(right=0.80,bottom=0.1)
    divider = make_axes_locatable(ax1)
    ax_cb = divider.append_axes('right',size="2%", pad=0.05)
    fig.add_axes(ax_cb)    

    # plot basemap    
    if radius != None:
        kwargs['width'] = radius*2.0
        kwargs['height'] = radius*2.0
        
    bmap = Basemap(projection='aeqd',
                   lat_0=lat_0,
                   lon_0=lon_0,
                   ax=ax1,
                   **kwargs)        
    bmap.drawmapboundary(fill_color='lightcyan')
    bmap.drawcoastlines(linewidth=0.5)
    bmap.fillcontinents(color='lightgoldenrodyellow',zorder=1)
    
    # plot center of the map
    xpt_0, ypt_0 = bmap(lon_0, lat_0)
    bmap.plot([xpt_0],[ypt_0],'kx')

    # plot earthquake event
    xpt_eq, ypt_eq = bmap(eq_lon,eq_lat)
    scattersize = lambda mag: 5.0**(mag-5.0)*15.0
    sc = ax1.scatter(xpt_eq, ypt_eq, s=scattersize(eq_mag), c=eq_depth, zorder=2,
                     alpha=0.7, cmap='Dark2')

    # draw colormap
    norm1 = colors.Normalize(0,800) # 0-800 km
    cb1= colorbar.ColorbarBase(ax_cb, cmap='Dark2', norm=norm1, orientation='vertical')
    cb1.ax.invert_yaxis()
    cb1.set_label('Depth [km]')

    # draw legend 
    l1 = ax1.scatter([],[], s=scattersize(5), edgecolors='none',color='k')
    l2 = ax1.scatter([],[], s=scattersize(6), edgecolors='none',color='k')
    l3 = ax1.scatter([],[], s=scattersize(7), edgecolors='none',color='k')
    labels = ["M5", "M6", "M7"]
    leg = ax1.legend([l1, l2, l3], labels, ncol=3, frameon=True, fontsize=12,
                     bbox_to_anchor=(0.5,-0.15),
                     handlelength=2, loc = 8, borderpad = 0.8,
                     handletextpad=1, title='Magnitude',
                     scatterpoints = 1)
    
    # plot circle
    if radius != None:
        N = 4
        dr = int(radius/N)
        dr = round(dr,1-len(str(dr)))
        r = dr
        while r <= radius:
            circle = plt.Circle((xpt_0, ypt_0), r,color='black',
                                 fill=False,linestyle='--')
            ax1.text(xpt_0,ypt_0-r,'{0:d} km'.format(int(r/1e3)),
                    ha='center',va='bottom',alpha=0.8,
                    bbox=dict(boxstyle="round",
                              facecolor='white', edgecolor='black',)
                   )
            ax1.add_patch(circle)
            r += dr
        
    # close figure
    ax1.set_title(title)
    fig.savefig('eqmap.png')
    plt.close()
    print('plot eqmap.png')


def plot_arrivals(eventid,model='iasp91',**kwargs):
    # - plot only one specified arrival -----
    import matplotlib.pyplot as plt


    from obspy.clients.fdsn import Client    
    client = Client("IRIS")
    catalog = client.get_events(eventid=eventid)    
    arrival = get_arrivals(catalog)[0]
    
    # setup figure 
    fig = plt.figure(figsize=(12,12))
    ax1 = fig.add_subplot(221,polar=True)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(224)
    ax2.invert_yaxis()
    
    # plot
    ax1 = arrival.plot_rays(fig=fig,ax=ax1)
    ax2 = arrival.plot_rays(plot_type='cartesian',fig=fig,ax=ax2)
    ax3 = arrival.plot_times(ax=ax3)
         
    # close
    ax3.legend(loc='lower right')
    plt.savefig('hoge.png')
    plt.close()
    
    
def main_plot_eqmap(start_str,end_str,**kwargs):
    '''
    
    '''
    from event import get_catalog
    catalog = get_catalog(start_str,end_str,**kwargs)
    #print catalog
    lat_kamioka=36.43
    lon_kamioka=137.31
    title = 'Azimuthal Equidistant Projection \n'\
            '{1} - {2}, Above M{0}'.format(kwargs['minmagnitude'],start_str,end_str)
            
    plot_eqmap(catalog,title=title,lat_0=lat_kamioka,lon_0=lon_kamioka,radius=4000e3)
