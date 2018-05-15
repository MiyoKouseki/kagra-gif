import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_toyama1 = pd.read_csv("toyama0502.txt", header=0, delimiter='\t')
df_toyama2 = pd.read_csv("toyama0503.txt", header=0, delimiter='\t')
df_toyama = pd.concat([df_toyama1,df_toyama2])
df_toyama =  df_toyama.loc[:,'pressure']
df_toyama.reset_index(drop=True,inplace=True)
#
df_takayama1 = pd.read_csv("takayama0502.txt", header=0, delimiter='\t')
df_takayama2 = pd.read_csv("takayama0503.txt", header=0, delimiter='\t')
df_takayama = pd.concat([df_takayama1,df_takayama2])
df_takayama =  df_takayama.loc[:,'pressure']
df_takayama.reset_index(drop=True,inplace=True)




plt.figure()
ax = df_toyama.plot()
#ax = df_takayama.plot()
plt.savefig("hoge.png")
plt.close()



