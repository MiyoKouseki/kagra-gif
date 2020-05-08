from gwpy.timeseries import TimeSeries
from astropy import units as u


# ----------------------------------------------------------------------

def main(chname,**kwargs):
    color = kwargs.pop('color','k')
    calc = kwargs.pop('calc',True)
    plot = kwargs.pop('plot',True)
    source = GifData.findfiles(start,end,chname,prefix=prefix)
    data = TimeSeries.read(source[0],name=chname,**kwargs)
    if calc:
        _ave = data.mean()
        _min = data.min()
        _max = data.max()
        _std = data.std()
        print('Ave:{0:3.3f}\nMin:{1:3.3f}\nMax:{2:3.3f}\nStd:{3:3.3f}'.\
            format(_ave,_min,_max,_std))
    if plot:
        plot = data.plot(ylim=(0,0.5),epoch=start,figsize=(25,5),
                         color=color,label=chname)
        ax = plot.gca()
        ax.legend()
        if 'ABSORP' in chname:
            ax.hlines(0.2,start,end,linestyle='--',color=color)        
        fname = chname.split('_')[1].lower()
        plot.savefig('tmp_TimeSeries_{0}.png'.format(fname))
        plot.close()
    return ax, data
    
if __name__ == '__main__':
    from miyopy.gif.datatype import GifData
    from gwpy.time import tconvert
    chname = 'PD_PPOL_PXI01_5'

    # start = tconvert('Apr 16 2020 11:34:00 UTC')
    # end   = tconvert('Apr 16 2020 11:42:00 UTC')
    start = tconvert('Jan 01 2020 00:00:00 UTC')
    end   = tconvert('May 01 2020 00:00:00 UTC')        
    # start = tconvert('Apr 29 2020 23:00:00 UTC')    
    # end   = tconvert('Apr 30 2020 00:00:00 UTC')
    prefix = '/Users/miyo/Git/kagra-gif/strainmeter/dutycycle'
    kwargs={'start':start,
            'end':end,
            'verbose':True,
            'nproc':1,
            'format':'gif'}
    #
    ax1, absp = main('PD_ABSORP_PXI01_5',color='k',**kwargs)
    ax2, ppol = main('PD_PPOL_PXI01_5',color='b',**kwargs)
    ax3, spol = main('PD_SPOL_PXI01_5',color='r',**kwargs)
    #
    is_locked = absp > 0.200*u.V
    #is_good_contrast = ppol > 0.100*u.V      
    dc = (float(is_locked.sum())/float(is_locked.shape[0]))
    print('{2:d}/{1:d} = {0:3.3f}'.format(dc,
          is_locked.sum(),is_locked.shape[0]))
