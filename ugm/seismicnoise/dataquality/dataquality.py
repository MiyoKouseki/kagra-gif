import sqlite3
import numpy as np

''' DQflag database format

Channel(
    startgps unique, 
    endgps unique, 
    flag bit)

BitFlag:
    0 bit : "CHECK_BIT", If checked, bit rise to 1. Default bit drop to 0.
    1 bit : "LACK_OF_FILE", If lack, bit rise to 1. Default bit drop to 0.
    2 bit : "LACK_OF_DATA", If lack, bit rise to 1. Default bit drop to 0.
    3 bit : "GLITCH", If existing, bit rise to 1. Default bit drop to 0.
'''

CHECK_BIT     = 0b1     # 1
LACK_OF_FILE  = 0b10    # 2
LACK_OF_DATA  = 0b100   # 4
NORMAL_REJECT = 0b1000  # 8

fmt_total = 'select startgps,endgps from {2} '+\
            'WHERE (startgps>={0} and endgps<={1})'
fmt_gauss = 'select startgps,endgps from {2} '+\
            'WHERE (flag=0)'+\
            ' and (startgps>={0} and endgps<={1})'

fmt_gauss_night = 'select startgps,endgps from {2} '+\
                  'WHERE flag=0' +\
                  ' and (startgps>={0} and endgps<={1})'+\
                  ' and ((startgps-18)%86400)>=43200'+\
                  ' and ((startgps-18)%86400)<86400'
fmt_gauss_day   = 'select startgps,endgps from {2} '+\
                  'WHERE flag=0' +\
                  ' and (startgps>={0} and endgps<={1})' +\
                  ' and ((startgps-18)%86400)>=0' +\
                  ' and ((startgps-18)%86400)<43200'
fmt_gauss_summer = 'select startgps,endgps from {2} ' +\
                   'WHERE flag=0' +\
                   ' and ('+\
                   '(startgps>=1211814018 and endgps<=1219676418) or '+\
                   '(startgps>=1243350018 and endgps<=1251212418)'+\
                   ')'
fmt_gauss_autumn = 'select startgps,endgps from {2} '+\
                   'WHERE flag=0'+\
                   ' and ('+\
                   '(startgps>=1219762818 and endgps<=1227538818) or '+\
                   '(startgps>=1251298818 and endgps<=1259074818)'+\
                   ')'
fmt_gauss_winter = 'select startgps,endgps from {2} '+\
                   'WHERE flag=0'+\
                   ' and ('+\
                   '(startgps>=1227625218 and endgps<=1235314818) or '+\
                   '(startgps>=1259161218 and endgps<=1266850818)'+\
                   ')'
fmt_gauss_spring = 'select startgps,endgps from {2} '+\
                   'WHERE flag=0'+\
                   ' and ('+\
                   '(startgps>=1203865218 and endgps<=1211727618) or ' +\
                   '(startgps>=1235401218 and endgps<=1243263618)'+\
                   ')'
fmt_gauss_2seis = 'select {2}.startgps,{2}.endgps '+\
                  'from {2} INNER JOIN {3} '+\
                  'ON ({2}.startgps ={3}.startgps) '+\
                  'WHERE ({2}.flag=0 and {3}.flag=0 )'+\
                  ' and ({2}.startgps>={0} and {2}.endgps<={1})'
fmt_gauss_3seis = 'select {2}.startgps,{2}.endgps '+\
                  'from {2} '+\
                  'INNER JOIN {3} '+\
                  'ON ({2}.startgps ={3}.startgps) '+\
                  'INNER JOIN {4} '+\
                  'ON ({2}.startgps ={4}.startgps) '+\
                  'WHERE ({2}.flag=0 and {3}.flag=0 and {4}.flag=0)'+\
                  ' and ({2}.startgps>={0} and {2}.endgps<={1})'

class DataQuality(object):
    def __init__(self,dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        self.check_db()

    def check_db(self):
        fmt_total = 'select startgps,endgps from {seis}'
        fmt = 'select startgps,endgps from {seis} WHERE flag={flag}'
        seislist = ['EXV_SEIS','IXV_SEIS','IXVTEST_SEIS','EYV_SEIS',
                    'MCE_SEIS','MCF_SEIS','BS_SEIS']
        ans = self.ask("select name from sqlite_master where type='table'")
        
        for seis in seislist:                                
            total = len(self.ask(fmt_total.format(seis=seis)))
            #for i,flag in enumerate([0,2,4,8]): 
            for i,flag in enumerate([0,1,2,4,8]): # removeme
                total -= len(self.ask(fmt.format(seis=seis,flag=flag)))
            if total!=0:                
                raise ValueError('SegmentList Error: Missmatch the number '+\
                                 'of segments.')
        
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
        self.add_table('TEST')
        
    def add_table(self,name='TEST'):
        '''
        '''
        # Make new table
        self.cursor.execute('create table {0}('.format(name)+
                            'startgps unique, endgps unique, flag bit)')        
        # Insert TEST value        
        # segments = zip(range(1211817600     ,1245372032+1,4096),
        #                range(1211817600+4096,1245372032+1,4096))
        segments = zip(range(1211817600     ,1245372032+1,4096),
                       range(1211817600+4096,1245372032+1,4096))
        #data = [(start,end,0) for start,end in segments]
        data = [(start,end,1) for start,end in segments] # removeme
        self.cursor.executemany("insert into {0} values (?,?,?)".format(name), data)

        
    def update_flag(self,name,start,end,flag,**kwargs):
        ''' Update flag
        '''
        override = kwargs.pop('override',False)
        off = kwargs.pop('off',False)
        check = kwargs.pop('check',False)
        # Check GPS time
        ans = self.ask('select startgps,endgps from {0} '\
                       'where startgps={1}'.format(name,start))            
        if not (start,end) == ans[0]:
            raise ValueError('({0},{1}) is wrong.'.format(start,end))
        
        # Read current flag
        now = self.get_flag(name,start,end,**kwargs)
        if override:
            now = flag
        else:
            if off:
                now -= now & flag # OFF
            else:
                now |= flag # ON
        if check:
            now |= CHECK_BIT
            
        # Update
        cmd = 'update {0} set flag = {1} where '.format(name,now) +\
              'startgps = {0}'.format(start,end)
        self.cursor.execute(cmd)
        
        
    def get_flag(self,name,start,end,**kwargs):
        '''
        '''
        ans = self.ask('select flag from {0} where startgps={1} '\
                       'and endgps={2}'.format(name,start,end))
        flag = ans[0][0]
        return flag

        
    def to_csv(self,rows,fname='tmp'):
        ''' Write down all data to csv file.
        '''
        import csv
        with open("{0}.csv".format(fname), "w") as f:
            writer = csv.writer(f)
            for row in rows:                
                writer.writerow(row)

    def to_txt(self,rows,fname='tmp'):
        ''' Write down all data to csv file.
        '''
        import csv
        with open("{0}.txt".format(fname), "w") as f:            
            for row in rows:
                print(row)
                f.write('{0} {1} {2}\n'.format(*row))
                

    def table_to_csv(self,name='TEST'):
        ''' Write down all data to csv file.
        '''
        import csv
        rows = self.ask('select * from {0}'.format(name))
        with open("DQflag_{0}.csv".format(name), "w") as f:
            writer = csv.writer(f)
            writer.writerow(['STARTGPSTIME','ENDGPSTIME','FLAG'])
            for row in rows:                
                writer.writerow(row)
                
                
    def ask(self,cmd):
        '''
        '''
        self.cursor.execute(cmd)        
        return self.cursor.fetchall()


def danger():
    #data = np.loadtxt('total.txt',dtype=np.int)    
    #data = np.loadtxt('nodata.txt',dtype=np.int)
    #data = np.loadtxt('lackofdata.txt',dtype=np.int)
    #data = np.loadtxt('glitch.txt',dtype=np.int)
    # with DataQuality() as db:
    #     for _,start,end,value in data:
    #         #db.update_flag('EXV_SEIS',start,end,0,override=True)            
    #         #db.update_flag('EXV_SEIS',start,end,LACK_OF_FILE)
    #         db.update_flag('EXV_SEIS',start,end,GLITCH)
    #     z = len(db.ask('select * from EXV_SEIS'))
    #     a = len(db.ask('select * from EXV_SEIS WHERE flag=0'))
    #     b = len(db.ask('select * from EXV_SEIS WHERE flag=2'))
    #     c = len(db.ask('select * from EXV_SEIS WHERE flag=4'))
    #     d = len(db.ask('select * from EXV_SEIS WHERE flag=8'))
    #     print z-a-b-c-d        
    pass


def remake(fname,seis):
    segments = np.loadtxt(fname,dtype=[('col1','i8'),('col2','i8'),('col3','S30')])
    statusdict = {b'Normal':0b0,
                  b'Normal_Reject':NORMAL_REJECT,
                  b'BadData':NORMAL_REJECT,
                  b'NoData_LackofData':LACK_OF_DATA,
                  b'NoData_AnyZero':LACK_OF_DATA,
                  b'NoData_AllZero':LACK_OF_DATA,
                  b'NoData_Empty':LACK_OF_DATA,
                  b'NoData_NoChannel':LACK_OF_DATA,
                  b'NoData_FewData':LACK_OF_DATA,
                  b'Nodata_AnyNan':LACK_OF_DATA,
                  b'NoData_FailedtoRead':LACK_OF_FILE,
                  b'Nodata_FailedtoRead':LACK_OF_FILE,
                  b'NoData_InvalidFormat':LACK_OF_FILE,
    }
    with DataQuality('./dqflag.db') as db:
        # Remake
        db.cursor.execute('drop table {0}'.format(seis))
        db.cursor.execute('vacuum')
        db.add_table(seis)
        #exit()
        for start,end,status in segments:
            print(start,end,status,statusdict[status])
            db.update_flag(seis,start,end,statusdict[status],override=True)
    

if __name__ == '__main__':
    
    #remake('./result_MCE.txt','MCE_SEIS')
    #remake('./result_MCF.txt','MCF_SEIS')
    #remake('./result_BS.txt' ,'BS_SEIS')
    remake('./result_EXV.txt' ,'EXV_SEIS')
    remake('./result_IXV.txt' ,'IXV_SEIS')
    remake('./result_EYV.txt' ,'EYV_SEIS')
    #remake('./result_IXVTEST.txt' ,'IXVTEST_SEIS')
