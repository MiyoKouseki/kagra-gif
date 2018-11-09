#!/usr/bin/env python
#!coding:utf-8

'''Generate result file which is readable from python on current directory.


Usage
-----
./run_gotic <start> <end>

<start> : datetime format
    start time. in UTC.
    Example -> 201810011500 or 2018-10-01 15:00

<end> : datetime format
    end time. in UTC.
    Example -> 201810301459 or 2018-10-30 14:59


Result
------
.gotic file

'''

from datetime import datetime as dt
import subprocess
import os
import sys
    

setting_template = '''
# tide.txt
*********************[ Mandatory Cards ]**********************
STAPOSD KAMIOKA, 137.31, 36.43, 358.0, 0.19
WAVE    MAJOR8
KIND    ST
**********************[ Option Cards ]************************
PREDICT 1, {start}, {end}, 1 
PREFMT  3, 1
UNIT20  {output_fname}
END
'''



path_to_goticpy = '/Users/miyo/Dropbox/Git/goticpy'
path_to_gotic2 = path_to_goticpy + '/gotic2/gotic2'
setting_fname = path_to_gotic2 + '/tides.txt'
output_fname = 'tides.out'


def make_settingfile(start,end,**kwargs):
    '''
    
    '''
    
    text = setting_template.format(start=start,end=end,
                                   output_fname=output_fname)    
    with open(setting_fname,'w') as f:
        f.write(text)
    print('Make setting file; {}'.format(setting_fname))

    
def run_gotic():
    
    path_to_current = os.getcwd()
    
    os.chdir(path_to_gotic2)
    print('Move to {}'.format(path_to_gotic2))
    
    cmd = "./gotic2 < tides.txt > tides.log"
    print('Run "{}"'.format(cmd))
    proc = subprocess.call( cmd , shell=True)
    
    os.chdir(path_to_current)
    print('Move to {}'.format(path_to_current))
    
    
def make_resultfile(start,end,**kwargs):
    
    cmd = "mv {path}/{output_fname} ./".format(path=path_to_gotic2,
                                               output_fname=output_fname)
    proc = subprocess.call( cmd , shell=True)

    with open(output_fname,'r') as f:
        text = f.read()

    result_fname = './{start}_{end}.gotic'.format(start=start,end=end)
    
    with open(result_fname,'w') as f:
        f.write(text.replace('D','E'))   
    print('Make result file; {}'.format(result_fname))
          
    
if __name__ == '__main__':    

    argvs = sys.argv 
    if (len(argvs) != 3): 
        raise ValueError('Usage : ./run_gotic.py 2018-10-19-15:00 2018-10-20-14:59 ')
    else:
        start = argvs[1]
        end = argvs[2]

    if ':' in start and ':' in end:
        try:
            start_datetime = dt.strptime(start, '%Y-%m-%d-%H:%M')
            end_datetime = dt.strptime(end, '%Y-%m-%d-%H:%M')
            if start>=end:
                raise ValueError('Invalid time option; start >= end')
            start = start_datetime.strftime('%Y%m%d%H%M')
            end = end_datetime.strftime('%Y%m%d%H%M')
        except Exception as e:
            print e
            exit()
    else:
        if (len(start) - 12 + len(end)) != 12:
            raise ValueError('Invalid time option; \n'\
                            'start : {start}\n' \
                            'end   : {end}'.format(start=start,end=end))
        try:        
            start_datetime = dt.strptime(start, '%Y%m%d%H%M')
            end_datetime = dt.strptime(end, '%Y%m%d%H%M')
        except Exception as e:
            print e
            exit()
        
        if start>=end:
            raise ValueError('Invalid time option; start >= end')

    make_settingfile(start,end)
    run_gotic()
    make_resultfile(start,end)
