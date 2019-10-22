#!/usr/bin/python
#!
# Start : 2018-06-01 00:59:42 (JST)
# End   : 2019-06-24 09:40:14 (JST)
seis = 'MCF'
#--------------------------------------------------------------------------------

# main.job
body = '''
Universe       = vanilla 
GetEnv         = True
Initialdir     = /home/kouseki.miyo/kagra-gif/ugm/seismicnoise
Notification   = Never
+Group         = "Xc"
request_memory = 4 GB

Executable = /usr/bin/python 
Error      = ./log/main.$(Process).err
Log        = ./log/main.$(Process).log
Output     = ./log/main.$(Process).out

RequestCpus    = 4
Arguments  = ./main.py --start 1211817600 --end 1245372032 --nproc 4 --percentile --seis {0} --term all
Queue
'''.format(seis)
with open('main.job','w') as f:
    f.write(body)


# main_multi_remakedb.job
body = '''
Universe       = vanilla 
GetEnv         = True
Initialdir     = /home/kouseki.miyo/kagra-gif/ugm/seismicnoise
Notification   = Never
+Group         = "Xc"
request_memory = 1 GB

Executable = /usr/bin/python 
Error      = ./log/main.$(Process).err
Log        = ./log/main.$(Process).log
Output     = ./log/main.$(Process).out
'''
queue = '''
RequestCpus = 2
Arguments  = ./main.py --start {0} --end {1} --nproc 2 --seis {2} --term all --remakedb
Queue
'''

jobs = 128
tlen = 2**25
bins = tlen/jobs
segments = zip(range(1211817600     ,1245372032+1,bins),
               range(1211817600+bins,1245372032+1,bins))
for start,end in segments:
    body += queue.format(start,end,seis)
with open('main_multi_remakedb.job','w') as f:
    f.write(body)


# main_multi_savespecgram.job
body = '''
Universe       = vanilla 
GetEnv         = True
Initialdir     = /home/kouseki.miyo/kagra-gif/ugm/seismicnoise
Notification   = Never
+Group         = "Xc"
request_memory = 1 GB

Executable = /usr/bin/python 
Error      = ./log/main.$(Process).err
Log        = ./log/main.$(Process).log
Output     = ./log/main.$(Process).out
'''
queue = '''
RequestCpus = 2
Arguments  = ./main.py --start {0} --end {1} --nproc 2 --seis {2} --term all --savespecgram --percentile
Queue
'''

jobs = 128
tlen = 2**25
bins = tlen/jobs
segments = zip(range(1211817600     ,1245372032+1,bins),
               range(1211817600+bins,1245372032+1,bins))
for start,end in segments:
    body += queue.format(start,end,seis)
with open('main_multi_savespecgram.job','w') as f:
    f.write(body)
