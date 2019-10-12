
head = '''
Universe       = vanilla 
GetEnv         = True
Initialdir     = /home/kouseki.miyo/kagra-gif/ugm/cdmr 
Notification   = Never
+Group         = "Xc"
request_memory = 2 GB

Executable = /usr/bin/python
Error      = ./log/main.$(Process).err
Log        = ./log/main.$(Process).log
Output     = ./log/main.$(Process).out

'''

que = '''
RequestCpus    = 4
Arguments  = ./main_m31.py cd{0:02d}_{1:02d}
Queue

'''

txt = head

for i in range(4,9,1): # cd4_  - cd8_
    for j in range(1,32,1): # cd1_1 - cd1_31
        txt += '# ------------------------------'
        txt += que.format(i,j)

with open('main_multi.job','w') as f:
    f.write(txt)
