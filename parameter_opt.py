import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from pmdarima.arima import ADFTest

i =0
df = pd.read_csv('/home/saunaq/Desktop/FutureEf/eth-perp_train.csv')
day = np.array([])
d=0
stds = np.array([])
avgs = np.array([])
step_size = 207
count =0
while i<(835779-step_size):
    subset_df = df.iloc[i:i+ step_size]
    close_prices = subset_df['close'].to_numpy()
    stds = np.append(stds, np.std(close_prices))
    avgs = np.append(avgs, np.mean(close_prices))
    i+=step_size
    day = np.append(day,d)
    d+=1
freq =0
valid_stds=np.array([])
for i in range(286, 835779-207,207):
    subset_df = df.iloc[i:i+207]
    close_prices = subset_df['close'].to_numpy()
    for j in range(30,203):
        subset_df2 = df.iloc[i+j-30:i+j]
        subset_df3 = df.iloc[i+j+1:i+j+4]
        mvavg = subset_df2['close'].to_numpy()
        nextavg = subset_df3['close'].to_numpy()
        if(close_prices[j]<1.1*np.mean(mvavg) and close_prices[j]<np.mean(nextavg)):
            valid_stds=np.append(valid_stds, np.std(close_prices))
            count+=1
        elif(close_prices[j]<np.mean(mvavg)):
            freq+=1


print(count/(count+freq))
print(np.mean(valid_stds))
print(np.std(valid_stds))
print(np.median(valid_stds))
print(np.median(valid_stds)**3/np.mean(valid_stds)**2)
