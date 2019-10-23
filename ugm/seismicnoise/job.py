#!/usr/bin/python
#!
# Start : 2018-06-01 00:59:42 (JST)
# End   : 2019-06-24 09:40:14 (JST)
#seis = 'MCF'
seis = ['EYV','BS','EXV','IXV','IXVTEST','MCE','MCF']
seis = seis[6]
#--------------------------------------------------------------------------------
tmp_headder = '''
Universe       = vanilla 
GetEnv         = True
Initialdir     = /home/kouseki.miyo/kagra-gif/ugm/seismicnoise
Notification   = Never
+Group         = "Xc"
request_memory = {memory} GB

Executable = /usr/bin/python 
Error      = ./log/main.$(Process).err
Log        = ./log/main.$(Process).log
Output     = ./log/main.$(Process).out
'''
tmp_que = '''
RequestCpus    = {nproc}
Arguments  = ./main.py --start {start} --end {end} --nproc {nproc} --seis {seis} --term {term} {option}
Queue
'''
#--------------------------------------------------------------------------------

# --- Main Job ---
headder = tmp_headder.format(memory=4)
que = tmp.format(start=1211817600,end=1245372032,
                 nproc=4,seis=seis,term='all',
                 option='--percentile')
cmd = headder + que
with open('main.job','w') as f:
    f.write(cmd)


# --- Multi Job ---
jobs = 128
tlen = 2**25
bins = tlen/jobs
segments = zip(range(1211817600     ,1245372032+1,bins),
               range(1211817600+bins,1245372032+1,bins))
# 1. main_multi_remakedb.job
cmd = tmp_headder.format(memory=1)
for start,end in segments:
    cmd += tmp_que.format(start=start,end=end,
                         nproc=1,seis=seis,term='all',
                         option='--remakedb')
with open('main_multi_remakedb.job','w') as f:
    f.write(cmd)
# 2. main_multi_savespecgram.job
cmd = tmp_headder.format(memory=1)
for start,end in segments:
    cmd += tmp_que.format(start=start,end=end,
                     nproc=1,seis=seis,term='all',
                     option='--savespecgram')
with open('main_multi_savespecgram.job','w') as f:
    f.write(cmd)
