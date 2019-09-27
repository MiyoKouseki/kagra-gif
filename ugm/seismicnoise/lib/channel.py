import lib.logger
log = lib.logger.Logger(__name__)

def get_seis_chname(start,end,place='EXV',axis='all'):
    '''
    
    '''
    if start > 1232755218:                          # 01/29 00:00 2019 - Today
        chname = ['K1:PEM-SEIS_EXV_GND_EW_IN1_DQ',
                  'K1:PEM-SEIS_EXV_GND_NS_IN1_DQ',
                  'K1:PEM-SEIS_EXV_GND_UD_IN1_DQ']
    elif 1227441618 < start and start < 1232701218: # 11/28 12:00 2018 - 01/28 09:00 2019
        chname = ['K1:PEM-EXV_GND_TR120Q_X_IN1_DQ',
                  'K1:PEM-EXV_GND_TR120Q_Y_IN1_DQ',
                  'K1:PEM-EXV_GND_TR120Q_Z_IN1_DQ']
    elif 1216803618 < start and start < 1227438018: # 07/28 09:00 2018 - 11/28 11:00 2018
        chname = ['K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ',
                  'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ',
                  'K1:PEM-EXV_SEIS_Z_SENSINF_IN1_DQ']
    elif 1203897618 < start and start < 1216800000: # 03/01 00:00 2018 - 07/28 08:00 2018
        chname = ['K1:PEM-EX1_SEIS_WE_SENSINF_IN1_DQ',
                  'K1:PEM-EX1_SEIS_NS_SENSINF_IN1_DQ',
                  'K1:PEM-EX1_SEIS_Z_SENSINF_IN1_DQ']
    else:
        chname = None

    if not axis == 'all':
        dic = {'X':0,'Y':1,'Z':2}        
        return  chname[dic[axis]]
    
    return chname

