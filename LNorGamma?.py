import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from pmdarima.arima import ADFTest
from scipy import stats

import statsmodels.api as sm



i =2
df = pd.read_csv('/home/saunaq/Desktop/FutureEf/eth-perp_train.csv')
day = np.array([])
d=0
stds = np.array([])
step_size = 12*60
while i<(835779-step_size):
    subset_df = df.iloc[i:i+ step_size]
    close_prices = subset_df['close'].to_numpy()
    stds = np.append(stds, np.std(close_prices))
    i+=step_size
    day = np.append(day,d)
    d+=1

bin_size = 5
hist, bins = np.histogram(stds, bins=np.arange(min(stds) -bin_size, max(stds) + bin_size, bin_size))

plt.hist(stds, bins=np.arange(min(stds)-bin_size, max(stds) + bin_size, bin_size), alpha=0.5, color='b', edgecolor='black')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram with Bins of Size 10 (Float Data)')
plt.grid(True)
plt.show()
