#!/usr/bin/python
#!
# Start : 2018-06-01 00:59:42 (JST)
# End   : 2019-06-24 09:40:14 (JST)
#seis = 'MCF'
seis = ['EYV','BS','EXV','IXV','IXVTEST','MCE','MCF']
seis = seis[3]
#--------------------------------------------------------------------------------
tmp_headder = '''
Universe       = vanilla 
GetEnv         = True
Initialdir     = /home/kouseki.miyo/Git/kagra-gif/ugm/seismicnoise
Notification   = Never
+Group         = "Xc"
request_memory = {memory} GB

#Executable = /usr/bin/python 
Executable = /home/kouseki.miyo/anaconda3/envs/miyo-py37/bin/python 
Error      = ./log/main.$(Process).err
Log        = ./log/main.$(Process).log
Output     = ./log/main.$(Process).out
'''
tmp_que = '''
RequestCpus    = {nproc}
Arguments  = ./main.py --start {start} --end {end} --nproc {nproc} --seis {seis} {option}
Queue
'''
tmp_que2 = '''
RequestCpus    = {nproc}
Arguments  = ./main.py --start {start} --end {end} --nproc {nproc} {option}
Queue
'''
#--------------------------------------------------------------------------------

START_GPS = 1211817600 # UTC: 2018-05-31 15:59:42
END_GPS   = 1245372032 # UTC: 2019-06-24 00:40:14 (end=start+2**25)

# --- Main Job ---
headder = tmp_headder.format(memory=16)
que = tmp_que.format(start=START_GPS,end=END_GPS,
                 nproc=8,seis=seis,term='all',
                 option='--asd')
cmd = headder + que
with open('main.job','w') as f:
    f.write(cmd)

# download
headder = tmp_headder.format(memory=16)
que = tmp_que2.format(start=START_GPS,end=END_GPS,
                      nproc=8,option='--download_gwf')
cmd = headder + que
with open('main_download.job','w') as f:
    f.write(cmd)

# --- Multi Job ---
jobs = 256
tlen = 33554432 #2**25
bins = int(tlen/jobs)
segments = zip(range(START_GPS     ,END_GPS+1,bins),
               range(START_GPS+bins,END_GPS+1,bins))
# 1. main_multi_remakedb.job
cmd = tmp_headder.format(memory=4)
for start,end in segments:
    cmd += tmp_que.format(start=start,end=end,
                          nproc=4,seis=seis,option='--updatedb')
with open('main_multi_update.job','w') as f:
    f.write(cmd)
# 2. main_multi_savespecgram.job
cmd = tmp_headder.format(memory=4)
for start,end in segments:
    cmd += tmp_que.format(start=start,end=end,
                          nproc=4,seis=seis,option='--savespecgram')
with open('main_multi_savespecgram.job','w') as f:
    f.write(cmd)
