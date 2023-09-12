import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from pmdarima.arima import ADFTest
from scipy import stats

#computes volatility over discrete intervals of 3 hours each. Our idea was to initially assume equal t1 and t2 and then optimize them later. 
#plan is to approximate the measure of volatility from the previous interval and use it to predict the next value by guessing a recursive stochastic process 
df = pd.read_csv('/home/saunaq/Desktop/FutureEf/eth-perp_train.csv')
day = np.array([])
d=0
stds = np.array([])
avgs = np.array([])
step_size = 3*60
count =0
i =0
while i<(835779-step_size):
    subset_df = df.iloc[i:i+ step_size]
    close_prices = subset_df['close'].to_numpy()
    stds = np.append(stds, np.std(close_prices))
    avgs = np.append(avgs, np.mean(close_prices))
    i+=step_size
    day = np.append(day,d)
    d+=1

# plotted some essential features to get a better idea of the data 
print(np.mean(stds))
print(np.std(stds))
print (np.median(stds))
print(np.median(stds)**3/np.mean(stds)**2)


#created a histogram to get a better idea of the probability density function of the data
num_bins = 346
plt.hist(stds, bins=num_bins, edgecolor='k')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of Data')
plt.show()
#visually appears to be a log normal distribution
statistic, p_value = stats.shapiro(stds)
significance_level = 0.05

print(p_value)
if p_value > significance_level:
    print("Log Normal.")
else:
    print("Not Log Normal.")
#returned false but this could be because of many outliers of sigma = 0 so removing these could make the data log normal

#plotted difference with past value to see if it could be used to predict the next value
differences =np.array([])
for i in range(1,len(stds)):
    differences = np.append(differences, (stds[i]-stds[i-1]))


# print(np.std(stds))
# print(np.min(stds))
# print(np.max(stds))
# print(np.mean(stds))
# print(np.median(stds))


num_bins = 346

plt.hist(stds, bins=num_bins, edgecolor='k')

# Add labels and a title
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of Data')

plt.show()

