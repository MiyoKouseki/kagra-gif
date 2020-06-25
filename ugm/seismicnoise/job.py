#!/usr/bin/python
#!
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
#--------------------------------------------------------------------------------

def write_single_job(jobname,seis='EXV',memory=16,option='--asd',nproc=8):
    '''
    '''
    headder = tmp_headder.format(memory=memory)
    que = tmp_que.format(start=START_GPS,end=END_GPS,nproc=8,
                         seis=seis,option=option)
    cmd = headder + que
    with open(jobname,'w') as f:
        f.write(cmd)

def write_multi_jobs(jobname,jobs,seis='EXV',memory=4,option='--updatedb',nproc=4):
    '''
    '''
    bins = int(TLEN/jobs)
    segments = zip(range(START_GPS     ,END_GPS+1,bins),
                   range(START_GPS+bins,END_GPS+1,bins))    
    #
    cmd = tmp_headder.format(memory=memory)
    for start,end in segments:
        cmd += tmp_que.format(start=start,end=end,
                              nproc=nproc,seis=seis,option=option)
    with open(jobname,'w') as f:
        f.write(cmd)

if __name__=='__main__':    
    START_GPS = 1211817600 # UTC: 2018-05-31 15:59:42
    END_GPS   = 1278926464 # UTC: 2020-07-16 09:20:46 (end=start+2**26)
    TLEN = 2**26
    #
    #1277087360 1277091456 Normal
    seis = 'EXV'
    write_single_job('asd.job',seis=seis,memory=16,nproc=8,option='--asd')
    write_single_job('download.job',seis=seis,memory=16,nproc=8,option='--download_gwf')
    #
    write_multi_jobs('update_multi.job',256,seis=seis,memory=4,nproc=4,option='--updatedb')
    write_multi_jobs('savespecgram_multi.job',256,seis=seis,memory=4,nproc=4,option='--savespecgram')
