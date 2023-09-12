import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from pmdarima.arima import ADFTest
from scipy import stats
from pmdarima.arima import ADFTest
from scipy.stats import kurtosis

import statsmodels.api as sm

df = pd.read_csv('/home/saunaq/Desktop/FutureEf/eth-perp_train.csv')
day = np.array([])
d=0
t1 = 285
t2 = 207
sigmat1 = np.array([])
sigmat2 = np.array([])
i=t1

#compute the standard deviation of the first t1 minutes of the day and the standard deviation of the next t2 minutes of the day
#and stores in two different arrays
while(i<(835781-t2)):
    subset_t1 = df.iloc[i-t1:i]
    subset_t2 = df.iloc[i:i+t2]
    close_prices_t1 = subset_t1['close'].to_numpy()
    close_prices_t2 = subset_t2['close'].to_numpy()
    sigmat1 = np.append(sigmat1, np.std(close_prices_t1))
    sigmat2 = np.append(sigmat2, np.std(close_prices_t2))
    i+=t2
    day = np.append(day,d)
    d+=1
    # if np.std(close_prices) == 0.0:
    #     print(i)

difference = np.array([])
for i in range(0,len(sigmat1)):
    difference = np.append(difference, sigmat2[i]-(sigmat1[i]-3.11))


#plots the histogram of the difference between the standard deviations of the two time periods and prints some important values 
stds = difference
std_dev = np.std(stds)
num_data_points = len(stds)
bin_size = (3.5 * std_dev) / (num_data_points ** (1/3))
hist, bins = np.histogram(stds, bins=np.arange(min(stds) -bin_size, max(stds) + bin_size, bin_size))
plt.hist(stds, bins=np.arange(min(stds)-bin_size, max(stds) + bin_size, bin_size), alpha=0.5, color='b', edgecolor='black')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram with Bins of Size 10 (Float Data)')
plt.grid(True)
plt.show()

print(np.mean(stds))
# print(np.std(stds))
# print (np.median(stds))
# print(np.max(stds)-np.min(stds)) 
# print(np.median(stds)**3/np.mean(stds)**2)
# print(kurtosis(stds))
