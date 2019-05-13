#!/usr/bin/env python
#! coding:utf-8

import argparse
import datetime
import subprocess
version = '0.0.1'
parser = argparse.ArgumentParser(description='aaa')
parser.add_argument('dtype', help='データの種類')
parser.add_argument('-s', '--start') #iso8601


# Parse arguments from command line
args = parser.parse_args()
dtype = args.dtype

start = args.start
try:
    start = datetime.datetime.strptime(start, '%Y-%m-%d')    
except:
    raise ValueError("Please use iso8601 format; '%Y-%m-%d'")


    
# Define parameter for rsync
rsync_fmt = 'rsync -av {option} -e ssh GIF@172.16.32.201:'\
  '{prefix_gif}/{yyyy:4d}/{mm:02d}/{dd:02d}/' + ' ' + \
  '{prefix_own}{prefix_gif}/{yyyy:4d}/{mm:02d}/{dd:02d}'

prefix_own = '/Users/miyo/Dropbox/KagraData/gif'

if dtype == 'cRIO01':
    option = ''    
    prefix_gif = '/NAS/cRIO01_data'
elif dtype == 'cRIO02':
    option = ''    
    prefix_gif = '/NAS/cRIO02_data'        
elif dtype == 'cRIO03':
    option = ''    
    prefix_gif = '/NAS/cRIO03_data'            
elif dtype == 'CLIO_LIN':
    option = ''    
    prefix_gif = '/data2/CLIO/LIN'                
elif dtype == 'CLIO_SHR':
    option = ''
    prefix_gif = '/data2/CLIO/SHR'                    
elif dtype == 'STRAIN':
    option = '--include="*/" --include="*.STRAIN" --exclude="*"'     
    prefix_gif = '/data1/PHASE/50000Hz'
elif dtype == 'PD_50k':
    option = '--include="*/" --include="*.AD0[0-2]" --exclude="*"'     
    prefix_gif = '/NAS/PXI1_data/50000Hz'    
else:
    raise ValueError('! no such type {0}'.format(dtype))

cmd = rsync_fmt.format(yyyy=start.year,mm=start.month,dd=start.day,hh=start.hour,
                       prefix_own=prefix_own,
                       prefix_gif=prefix_gif,
                       option=option)


# Comfirmation before run command
text = ''' 
**********************************************************************
***************** Rsync GIF data Version {version} ***********************
**********************************************************************

All {dtype} data when "{yyyy:4d}/{mm:02d}/{dd:02d}" are transfered to you.
 - From : ssh GIF@172.16.32.201:{prefix_gif}/{yyyy:4d}/{mm:2d}/{dd:02d}/{hh:02d}
 - To : {prefix_own}{prefix_gif}/{yyyy:4d}/{mm:02d}/{dd:02d}/

If you OK, press enter
'''.format(yyyy=start.year,mm=start.month,dd=start.day,hh=start.hour,
                       prefix_own=prefix_own,
                       prefix_gif=prefix_gif,
                       dtype=dtype,
                       option=option,version=version)
print text


# Run
yes = raw_input('[y]/n : ') 
if yes in ['','y']:
    print cmd
    #ret = subprocess.check_call( cmd.split(" ") )
elif yes in ['n']:
    print 'Not excute. Bye..'
else:
    raise ValueError('Please enter y or n')
