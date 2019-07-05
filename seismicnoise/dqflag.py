import traceback

FLAG = ['LACK_OF_FILE','LACK_OF_DATA','GLITCH']
    

segments = [[1211817600,1211821696],
            [1211821696,1211825792]]

segment = segments[0]


import pandas as pd


class SeisDataDB():
    def __init__(self,dbname):
        self.df = pd.read_csv(dbname)
        self.start = 1211817600
        self.end = 1245372032
        self.bins = 4096
        
    def bals(self):
        datetime = zip(range(self.start,self.end+1,self.bins),
                    range(self.start+self.bins,self.end+1,self.bins))
        df = pd.DataFrame(datetime,columns=['START','END'])
        df['LACK_OF_FILE'] = False
        df['LACK_OF_DATA'] = False
        df['GLITCH'] = False
        df.to_csv('sample.csv')
        

    def get_status(self,segment,flag='LACK_OF_DATA'):
        if not flag in FLAG:
            raise ValueError('!!')

        start,end = segment
        ans = self.df.loc[(self.df.START==start)&(self.df.END==end),flag].values[0]
        return ans

    def set_status(self,value,segment,flag='LACK_OF_DATA'):
        if not flag in FLAG:
            raise ValueError('!!')
        
        start,end = segment        
        self.df.loc[(self.df.START==start)&(self.df.END==end),flag] = value

    def save(self):
        self.df.to_csv('sample.csv')

    def import_gwpy(self,fname,path,flag='LACK_OF_FILE'):
        from gwpy.segments import DataQualityFlag
        total = DataQualityFlag.read(fname,path)
        for d in total.active:
            segment = [d[0],d[1]]
            exv.set_status(True,segment,flag)
        
        
if __name__ == "__main__":
    segments = [[1211817600,1211821696],
                [1211821696,1211825792]]
        
    segment = segments[0]
    
    exv = SeisDataDB('sample.csv')
    #exv.bals()
    exv.import_gwpy('./nodata.hdf5','nodata',flag='LACK_OF_FILE')
    #exv.save()
    print exv.df
    print exv.df[exv.df['LACK_OF_FILE']==True]
    
