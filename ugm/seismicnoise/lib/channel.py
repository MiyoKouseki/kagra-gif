import lib.logger
log = lib.logger.Logger(__name__)

def _get_seis_chname(start,end,seis='EXV',axis='X'):
    ''' Return a channel name of a seismometer at the specified time.

    Parameters
    ----------
    start : `int`
        start GPS time.
    end : `int`
        end GPS time.
    seis : `str`, optional
        seis of the seismometer. default is 'EXV'
    axis : `str`
        axis of the seismometer. default is 'X'

    Returns
    -------
    chnamme : `str`
        channel name.
    '''
    chname_fmt = 'K1:PEM-{prefix}_{axis}_{suffix}'
    chname_fmt_test = 'K1:PEM-{prefix}TEST_{axis}_{suffix}'
    axis_num = {'X':0,'Y':1,'Z':2}        

    if not seis in ['EXV','IXV','IXVTEST','EYV','MCE','MCF','BS']:
        raise ValueError('known seis name {0}'.format(seis))
    else:
        if 'TEST' in seis:
            chname_fmt = chname_fmt_test
            seis = seis.split('TEST')[0]

    if not axis in ['X','Y','Z']:
        raise ValueError('known axis name {0}'.format(axis))

    if start > 1232755218:                          
        # 01/29 00:00 2019 - Today
        prefix = 'SEIS_{0}_GND'.format(seis)
        axes = ['EW','NS','UD']
        suffix = 'IN1_DQ'
    elif 1227441618 < start and start < 1232701218: 
        # 11/28 12:00 2018 - 01/28 09:00 2019
        prefix = '{0}_GND_TR120Q'.format(seis)
        axes = ['X','Y','Z']
        suffix = 'IN1_DQ'
    elif 1216803618 < start and start < 1227438018: 
        # 07/28 09:00 2018 - 11/28 11:00 2018
        prefix = '{0}_SEIS'.format(seis)
        axes = ['WE','NS','Z']
        suffix = 'SENSINF_IN1_DQ'
    elif 1203897618 < start and start < 1216800000: 
        # 03/01 00:00 2018 - 07/28 08:00 2018
        if 'V' in seis:
            seis = seis.replace('V','1')
            prefix = '{0}_SEIS'.format(seis)
        else:
            prefix = '{0}_SEIS'.format(seis)
        axes = ['WE','NS','Z']
        suffix = 'SENSINF_IN1_DQ'
    else:
        return 'Undefined_Channel_Name'

    num = axis_num[axis]
    chname = chname_fmt.format(prefix=prefix,axis=axes[num],suffix=suffix)    
    return chname


def get_seis_chname(start,end,seis='EXV',axis='all'):
    ''' Return a channel list of the seismometer with multiple axes.

    Parameters
    ----------
    start : `int`
        start GPS time.
    end : `int`
        end GPS time.
    seis : `str`, optional
        seis of the seismometer. default is 'EXV'
    axis : `str`
        axis of the seismometer. default is 'all'

    Returns
    -------
    chnamme : list of `str`
        channel name.
    '''
    if isinstance(axis,str):        
        if axis=='all':
            return [ _get_seis_chname(start,end,seis,_axis) for _axis in ['X','Y','Z']]
        elif axis in ['X','Y','Z']:
            return [_get_seis_chname(start,end,seis,axis)]
        else:
            raise ValueError('Unknown axis name {0}'.format(axis))
    elif isinstance(axis,list):
        return [ _get_seis_chname(start,end,seis,axis) for _axis in axis]
    else:
        raise ValueError('Unknown axis type {0}'.format(axis))
