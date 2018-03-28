#
#! coding:utf-8
import pandas as pd
import datetime

def get_fw0_dataframe(fname='/users/DGS/Frame/fw0-latest.txt',ascending=False):
    """
    山本さんが用意した、fw0のデータリストをpandasのDataFrameで読み出す。
    
    Parameters
    ----------
    fname : str
       File name of the fw list Yamamoto-san made.

    Returns
    -------
    df : pandas.dataframe
        Sortted dataframe.

    Examples
    --------
    >>> get_fw0_dataframe()
    <pandas.dataframe>
    """    
    df = pd.read_csv(fname,
        header = None,
        names = ('GPS_START', 'GPS_END', 'JST_START', 'DURATION'),
        sep = ' ',
        )    
    df['JST_START'] = pd.to_datetime(df['JST_START'])    
    df = df.sort_values(by='GPS_START',ascending=ascending)
    df = df.reset_index()
    return df    

def is_record_in_fw0(start,duration):
    """
    指定した時間のデータがfw0に保存されているかどうか判別する。    
    
    Parameters
    ----------
    start : int
        Starting time of the data. Only GPS time
    duration : int
        Data time length. seconds.

    Returns
    -------
    start : int
        Available start time duaring requested time as a GPS time.
    duration : int
        Available time length.
    Examples
    --------
    >>> is_record_in_fw0('2018-03-15 10:37:50',3600)
    [1205113088, 3600]
    """
    #df = get_fw0_dataframe() #for k1ctr
    df = get_fw0_dataframe('./fw0-latest_0323.txt')  # for my mac
    df = df[df['GPS_START']<=start]
    df = df[(start+duration)<=df['GPS_END']]
    if df.empty:
        print 'No data'
        exit()
    else:        
        start,duration = start,duration
        return start, duration    
