#
#! coding:utf-8

import subprocess
print 'パスワード入力'
cmd = 'rsync -av -e ssh GIF@172.16.32.201:/NAS/cRIO01_data/2018/11/21/0* /Users/miyo/Dropbox/KagraData/gif/NAS/cRIO01_data/2018/11/21/'
ret  =  subprocess.check_call( cmd.split(" ") )

print 'パスワード入力'
cmd = 'rsync -av -e ssh GIF@172.16.32.201:/NAS/cRIO02_data/2018/11/21/0* /Users/miyo/Dropbox/KagraData/gif/NAS/cRIO02_data/2018/11/21/'
ret  =  subprocess.check_call( cmd.split(" ") )

print 'パスワード入力'
cmd = 'rsync -av -e ssh GIF@172.16.32.201:/NAS/cRIO03_data/2018/11/21/0* /Users/miyo/Dropbox/KagraData/gif/NAS/cRIO03_data/2018/11/21/'
ret  =  subprocess.check_call( cmd.split(" ") )

print 'パスワード入力'
cmd = 'rsync -av --include="*/" --include="*.STRAIN" --exclude="*" -e ssh GIF@172.16.32.201:/data1/PHASE/50000Hz/2018/11/21/0* /Users/miyo/Dropbox/KagraData/gif/data1/PHASE/50000Hz/2018/11/21/'
print cmd
ret  =  subprocess.check_call( cmd.split(" ") )


#print 'パスワード入力'
#cmd = 'rsync -av -e ssh GIF@172.16.32.201:/data2/CLIO/LIN/2018/11/21/0* /Users/miyo/Dropbox/KagraData/gif/data2/CLIO/LIN/2018/11/21/'
#ret  =  subprocess.check_call( cmd.split(" ") )

#print 'パスワード入力'
#cmd = 'rsync -av -e ssh GIF@172.16.32.201:/data2/CLIO/SHR/2018/11/21/0* /Users/miyo/Dropbox/KagraData/gif/data2/CLIO/SHR/2018/11/21/'
#ret  =  subprocess.check_call( cmd.split(" ") )
