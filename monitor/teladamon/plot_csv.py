import datetime
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('./2018Nov01-2019Jan01.csv')
df = df.drop("sec", axis=1)
df['Date Time'] = pd.to_datetime(df['Date Time'])
df = df[df['Date Time'] > datetime.date(2018, 12, 20)]
data = df.iloc[:,0:2]
data = df[['Date Time','Ch4']]
ax = data.set_index('Date Time').plot(figsize=(14,8))
ax.set(xlabel='Date Time', ylabel='Voltage [V]')
plt.savefig('tmp.png')

