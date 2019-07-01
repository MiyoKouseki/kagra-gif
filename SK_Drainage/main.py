
import pandas as pd

read_original_file = True
resample = True


if read_original_file:
    my_parser = lambda date: pd.datetime.strptime(date, '%y/%m/%d-%H:%M:%S')    
    data = pd.read_csv("./data/clean.dat",names=["DateTime","Height[m]"],
                    sep=' ',index_col='DateTime',
                    parse_dates=True,
                    date_parser=my_parser)
    data = data.asfreq('S')
    if resample:
        data = data.resample('D').mean()
        print data
        data.to_csv('./data/clean_htrend.csv')
else:
    data = pd.read_csv("./data/clean_htrend.csv",names=["DateTime","Height[m]"],
                       sep=' ',index_col='DateTime',
                       parse_dates=True)
    print data
