
from gwpy.frequencyseries import FrequencySeries

def kagra_seis(axis='X',pctl=90):
    if axis in ['X','Y','Z']:
        prefix = '/Users/miyo/Dropbox/Git/kagra-gif/armLengthCompensationSystem/seismodel/JGW-T1910436-v1/'
        fname = 'LongTerm_{axis}_{pctl}_VELO.txt'.format(axis=axis,pctl=pctl)
        vel_asd = FrequencySeries.read(prefix+fname)
        return vel_asd
    elif axis == 'H':
        vel_x = kagra_seis('X',pctl)
        vel_y = kagra_seis('Y',pctl)
        vel_h = (vel_x**2+vel_y**2)**(1./2)
        return vel_h
    elif axis == 'V':
        return kagra_seis('Z',pctl)   
    else:
        raise ValueError('hoge')

if __name__ == '__main__':
    x = kagra_seis('X',90)
    y = kagra_seis('Y',90)
    print kagra_seis('H',90)
