import sqlite3
import numpy as np
from gwpy.time import tconvert,from_gps
from datetime import timedelta
from progressbar import progressbar
from astropy.time import Time,TimezoneInfo
from miyopy.gif.files  import fname_fmt
from gwpy.timeseries import TimeSeries
from astropy import units as u
import os
import multiprocessing
from tqdm import tqdm
from multiprocessing import Pool, freeze_support, RLock

''' DQflag database format

Channel(
    gps integer unique, 
    utc text unique, 
    gifjst text unique,
    flag bit)
'''

CHECK_BIT           = 0b1        # 1
LACK_OF_DATA        = 0b10       # 2
LASER_IS_NOT_LOCKED = 0b1000     # 8
LOW_PPOL_CONTRAST   = 0b10000    # 16
LOW_SPOL_CONTRAST   = 0b100000   # 32
STRAIN_STEPS        = 0b1000000  # 64

_dict = {2:'LACK_OF_DATA',
         8:'LASER_IS_NOT_LOCKED',
         16:'LOW_PPOL_CONTRAST',
         32:'LOW_SPOL_CONTRAST',
         64:'STRAIN_STEP'}

def gps2gifjst(gps):
    ''' Convert gps to jst
    
    Parameters
    ----------
    gps : `int`
        gpstime

    Returns
    -------
    date_str : `str`
        JST
    '''
    #
    # Fix me
    #
    utc_plus_one_hour = TimezoneInfo(utc_offset=1*u.hour)
    date = Time(int(gps),format='gps',scale='utc')
    
    if gps>=1167264017-3600*9: # due to a leap second at 2016-12-31T23:59:60
        date = date + timedelta(hours=9,minutes=0,seconds=1) #UTC -> JST
    else:
        date = date + timedelta(hours=9,minutes=0,seconds=0) #UTC -> JST
        pass
    date_str = date.strftime('%Y/%m/%d/%H/%y%m%d%H%M')
    return date_str


def gps2utc(gps):
    ''' Convert gps to jst
    
    Parameters
    ----------
    gps : `int`
        gpstime

    Returns
    -------
    date_str : `str`
        JST
    '''
    date = Time(int(gps),format='gps',scale='utc')
    date_str = date.strftime('%Y/%m/%d/%H/%y%m%d%H%M%S')
    return date_str

def hoge(idx):
    try:
        if idx==1:
            text = 'CHECKED'
        elif idx==0:
            text = 'NOT_CHECKED'            
        else:
            idx-=1
            text = _dict[idx]
    except Exception as e:
        text = str(idx)
    return text

# ------------------------------------------------------------------------------

class DataQualityDB(object):
    def __init__(self,dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self
        
    def __exit__(self, ex_type, ex_value, trace):
        self.conn.commit()
        self.conn.close()
        

class GifDataQuality(object):
    def __init__(self,dbname):
        self.start = tconvert('Jan 02 2017 00:00 JST')
        self.end   = tconvert('Jan 01 2021 00:00 JST')
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        #self.check_db()
        
    def __enter__(self):
        return self
    
    def __exit__(self, ex_type, ex_value, trace):
        self.conn.commit()
        self.conn.close()
        
    def bals(self):
        '''Initialize only TEST table
        '''
        # Find all tables and delete completely       
        ans = self.ask("select name from sqlite_master where type='table'")
        tables = list(np.array(ans).flatten())
        for name in tables:
            self.cursor.execute('drop table {0}'.format(name))
        self.cursor.execute('vacuum')
        
        # Make TEST table
        self.add_newtable('TEST')        

    def info(self,**kwargs):
        ''' Print status
        
        Parameters
        ----------
        _s : `int`, optional
            start gps time
        _e : `int`, optional
            end gps time
        '''
        _s = kwargs.pop('_s',self.start)
        _e = kwargs.pop('_e',self.end)
        #random = kwargs.pop('random',True)
        
        cmd_fmt = 'select gps from TEST where gps>={0} and gps<{1}'
        all_n = len(self.ask(cmd_fmt.format(_s,_e)))

        cmd_fmt = cmd_fmt + ' and flag=={2}'
        flag_n = [len(self.ask(cmd_fmt.format(_s,_e,_f))) for _f in range(0,100)]
        flag_idx = np.nonzero(np.array(flag_n))[0]

        print('--------------------------------------------')
        print('{0} - {1}'.format(from_gps(_s),from_gps(_e)))
        print('All                  {1:010d}'.format(0,all_n))
        for idx in flag_idx:
            print('{0:20s} {1:010d}'.format(hoge(idx),flag_n[idx]))
        print('--------------------------------------------')
        if np.sum(flag_n) != all_n:
            print('{0}!= {1}'.format(np.sum(flag_n),all_n))
            #raise ValueError('{0}!= {1}'.format(np.sum(flag_n),all_n))
        else:
            pass
        
    def add_newtable(self,name='TEST',verbose=True):
        '''
        '''
        gps = np.arange(self.start,self.end,60) # 1 minute
        if verbose:
            data = [(int(_gps),gps2utc(_gps),gps2gifjst(_gps),0)
                        for _gps in progressbar(gps)] 
        else:
            data = [(int(_gps),gps2utc(_gps),gps2gifjst(_gps),0)
                        for _gps in gps]
            
        cmd = 'create table {0}(gps integer unique, '\
          'utc text unique, gifjst text unique, flag bit)'.format(name)
        self.cursor.execute(cmd)        
        cmd = "insert into {0} values (?,?,?,?)".format(name)
        self.cursor.executemany(cmd, data)
                
    def ask(self,cmd,**kwargs):
        '''
        '''
        self.cursor.execute(cmd)
        ans = self.cursor.fetchall()
        return ans

    def get_data(self,cmd,**kwargs):
        '''
        '''
        self.cursor.execute(cmd)
        ans = self.cursor.fetchall()
        return ans
    

    def on_flag(self,name,start,flag):
        now = self.get_flag(name,start)
        #if off:
        #    now -= now & flag # OFF
        #else:
        now |= flag # ON
        now |= CHECK_BIT            
        # Update
        cmd = 'update {0} set flag = {1} where gps = {2}'.format(name,now,start)
        self.cursor.execute(cmd)

    def off_flag(self,name,start,flag):
        now = self.get_flag(name,start)
        now -= now & flag # OFF
        now |= CHECK_BIT            
        # Update
        cmd = 'update {0} set flag = {1} where gps = {2}'.format(name,now,start)
        self.cursor.execute(cmd)

    def check_bit(self,name,start):
        now = CHECK_BIT
        cmd = 'update {0} set flag = {1} where gps = {2}'.format(name,now,start)
        self.cursor.execute(cmd)
        
    def init_flag(self,name,start):
        now = self.get_flag(name,start)
        now = 0
        # Update
        cmd = 'update {0} set flag = {1} where gps = {2}'.format(name,now,start)
        self.cursor.execute(cmd)

    def delete_error_table(self,name):
        cmd = 'delete from {0} where gps = 1167264017'.format(name)
        self.cursor.execute(cmd)
            
    def override_flag(self,name,start,flag):
        ''' Update flag
        '''                
        # Read current flag
        now = flag
        now |= CHECK_BIT
            
        # Update
        cmd = 'update {0} set flag = {1} where gps = {2}'.format(name,now,start)
        self.cursor.execute(cmd)
                
    def get_flag(self,name,start,**kwargs):
        '''
        '''
        ans = self.ask('select flag from {0} where gps={1}'.format(name,start))
        flag = ans[0][0]
        return flag


def is_strain_steps(data,test=True):
    if test:
        print(data)
        plot = data.plot()
        plot.savefig('tmp.png')
        plot.close()
        print('test mode')
        exit()
    else:
        return ans

        
def check_status(ans):
    '''
    '''
    gps,fname,chname = ans
    start,end = gps, gps+60
    with GifDataQuality('filelist.db') as db:
        try:
            data = TimeSeries.read(fname,name=chname,
                                   start=start,end=end,
                                   format='gif',pad=0.0)
        except FileNotFoundError as e:
            db.on_flag('TEST',gps,LACK_OF_DATA)
            return None
        
        _min = data.min()       
        _max = data.max()
        if _max+_min == 0.0*u.V:
            _contrast = np.nan
            _pk2pk = np.nan
            db.on_flag('TEST',gps,LACK_OF_DATA)
            return None
        else:
            _contrast = (_max-_min)/(_max+_min)
            _pk2pk = (_max-_min)
            
        if 'ABSORP' in chname:
            if _min<0.02*u.V:
                db.on_flag('TEST',gps,LASER_IS_NOT_LOCKED)
            else:
                db.check_bit('TEST',gps)
        elif 'PPOL' in chname:
            if _pk2pk<0.003*u.V:
                db.on_flag('TEST',gps,LOW_PPOL_CONTRAST)
            else:
                db.check_bit('TEST',gps)
        elif 'SPOL' in chname:
            if _pk2pk<0.003*u.V:
                db.on_flag('TEST',gps,LOW_SPOL_CONTRAST)
            else:
                db.check_bit('TEST',gps)        
        elif 'STRAIN' in chname:
            if is_strain_steps(data):
                db.on_flag('TEST',gps,STRAIN_STEPS)
            else:
                db.check_bit('TEST',gps)                
        else:            
            raise ValueError('{0}'.format(chname))

def jstlist2fnamelist(jstlist,chname):
    fmt = fname_fmt[chname]
    fnamelist = map(lambda jst:fmt.replace('<fname>',jst),jstlist)
    prefix = '/Volumes/HDPF-UT/DATA'        
    fnamelist = list(map(lambda fname:prefix+fname,fnamelist))
    return fnamelist
        
def get_dataset(s,e,chname,flag=0,random=False):
    '''
    '''
    with GifDataQuality('filelist.db') as db:        
        cmd = 'select gps,utc,gifjst from TEST where '+\
          'gps>={0} and gps<{1} and flag=={2}'.format(s,e,flag)
        ans = np.array(db.ask(cmd))
    
    if not list(ans):
        return list(ans)
    else:
        jstlist = ans[:,2]
        fnamelist = np.array(jstlist2fnamelist(jstlist,chname),dtype='str')
        gpslist = np.array(ans[:,0], dtype='int64')
        chnamelist = np.array([chname]*len(jstlist),dtype='str')
        dataset = list(zip(gpslist,fnamelist,chnamelist))
        num = len(dataset)
    if random and num>100:
        np.random.seed(34)
        idx = np.random.choice(len(dataset),100,replace=False)
        dataset = [dataset[_idx] for _idx in idx]
        #print(flag,dataset[0][0],dataset[0][2])
        return dataset
    else:
        pass
    
    return dataset

def multi_check_status(dataset,nproc=4):
    with Pool(nproc) as p:
        imap = p.imap(check_status, dataset)
        result = list(tqdm(imap,total=len(dataset)))   
        
def is_laser_locked(s,e,flag=0,nproc=4):
    if flag in [0,1]:
        dataset = get_dataset(s,e,'PD_ABSORP_PXI01_5',flag=flag)
        if nproc>1:
            multi_check_status(dataset)
        else:
            check_status(dataset)

def is_ppol_contrast_high(s,e,flag=0,nproc=4):
    if flag in [0,1]:
        dataset = get_dataset(s,e,'PD_PPOL_PXI01_5',flag=flag)
        if nproc>1:
            multi_check_status(dataset)
        else:
            check_status(dataset)

def is_spol_contrast_high(s,e,flag=0,nproc=4):
    if flag in [0,1]:
        dataset = get_dataset(s,e,'PD_SPOL_PXI01_5',flag=flag)
        if nproc>1:
            multi_check_status(dataset)
        else:
            check_status(dataset)

def does_not_strain_step_exist(s,e,flag=0,nproc=4):
    if flag in [0,1]:
        dataset = get_dataset(s,e,'CALC_STRAIN',flag=flag)
        nproc = multiprocessing.cpu_count()
        nproc = 1
        if dataset:
            check_status(dataset[1])
        else:
            return None
        
        if nproc>1:
            multi_check_status(dataset)
        else:
            check_status(dataset)                
            
if __name__ == '__main__':
    
    start = tconvert('Jan 02 2018 00:00 JST')
    end   = tconvert('Feb 01 2018 00:00 JST')
    dbname = 'filelist.db'        

    # Prepare DB file
    if not os.path.exists(dbname):
        with GifDataQuality(dbname) as db:
            db.bals()           
    else:
        val = input('{0} exists. Do you remake DB file? yes/[No]'.\
                    format(dbname))
        if val in ['y','yes']:
            with GifDataQuality(dbname) as db:
                db.bals()           
        elif val in ['n','no',]:
            pass
        elif val == '':
            pass
        else:
            raise ValueError('{0} : Please input yes or no.'.format(val))
        
    # Print DB status
    with GifDataQuality(dbname) as db:
        db.info(_s=start,_e=end)

    # check all status
    for flag in [0,1,2,3,9,17]:
        print('- ',hoge(flag))
        is_laser_locked(start,end,flag=flag,nproc=4)
        is_ppol_contrast_high(start,end,flag=flag,nproc=4)
        is_spol_contrast_high(start,end,flag=flag,nproc=4)
        #does_not_strain_step_exist(s,e,flag=i,nproc=4)

    # Check DB status
    with GifDataQuality(dbname) as db:
        db.info(_s=start,_e=end)
