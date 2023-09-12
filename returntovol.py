import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from pmdarima.arima import ADFTest
from scipy import stats

import statsmodels.api as sm

#We didn't use any of the results from this file in the final report so it is left uncommented, but you can take a look at it if you want 
i =2
df = pd.read_csv('/home/saunaq/Desktop/FutureEf/eth-perp_train.csv')
day = np.array([])
d=0
evs = np.array([])
stds = np.array([])
step_size = 15
while i<(835779-step_size):
    subset_df = df.iloc[i:i+ step_size]
    close_prices = subset_df['close'].to_numpy()
    evs = np.append(evs, np.std(close_prices))
    day = np.append(day,d)
    d+=1
    i+=step_size
step_size2 = 5
j = 2 + step_size2
while j<(835779-step_size2):
        subset_df = df.iloc[j:j+ step_size2]
        close_prices = subset_df['close'].to_numpy()
        stds = np.append(stds, close_prices[-1]-close_prices[0])
        j+=step_size2



differences =np.array([])
for i in range(4,len(evs)):
    differences = np.append(differences, evs[i]-((evs[i-1])/1))
bin_size =5
hist, bins = np.histogram(evs, bins=np.arange(min(evs) -bin_size, max(evs) + bin_size, bin_size))

# plt.hist(evs, bins=np.arange(min(evs)-bin_size, max(evs) + bin_size, bin_size), alpha=0.5, color='b', edgecolor='black')
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('Histogram with Bins of Size 10 (Float Data)')
# plt.grid(True)
# plt.show()
# stds = stds[1:]
evs = evs[1:]
# plt.scatter(stds, evs, marker='o', color='blue', label='Data Points')
# plt.xlabel('stds')
# plt.ylabel('evs')
# plt.title('Scatter Plot of Two Arrays')
# plt.legend()
# plt.grid(True)
# plt.show()
bucket_size = 10

array1 = evs
array2 = stds
num_buckets = int(np.ceil(array1.max() / bucket_size))
bucket_counts = np.zeros(num_buckets, dtype=int)
bucket_avgs = np.zeros(num_buckets, dtype=int)
for value1, value2 in zip(array1, array2):
    bucket_index = int(value1 / bucket_size)
    bucket_counts[bucket_index] += 1
    bucket_avgs[bucket_index] += value2

for i in range(len(bucket_avgs)):
    if(bucket_counts[i] == 0):
        bucket_avgs[i] = 0
    else: 
        bucket_avgs[i] = bucket_avgs[i]/bucket_counts[i]

# bucket_centers = [(i + 0.5) * bucket_size for i in range(num_buckets)]
# plt.bar(bucket_centers, bucket_avgs, width=bucket_size, align='center')
# plt.xlabel('Bucket Center')
# plt.ylabel('avg')
# plt.title('Counts in Buckets')
# plt.show()
num_quantiles = 50  
quantile_boundaries = np.percentile(array1, np.linspace(0, 100, num_quantiles + 1))
bucket_indices = np.digitize(array1, quantile_boundaries)
bucket_sum = np.bincount(bucket_indices, weights=array2)
bucket_count = np.bincount(bucket_indices)
bucket_average = np.zeros(num_quantiles)
for i in range(1, num_quantiles + 1):
    if bucket_count[i] > 0:
        bucket_average[i - 1] = bucket_sum[i] / bucket_count[i]

quantile_labels = [f'{int(quantile_boundaries[i])}-{int(quantile_boundaries[i+1])}' for i in range(num_quantiles)]
plt.bar(quantile_labels, bucket_average, align='center')
plt.xlabel('Quantile')
plt.ylabel('Average of Values in Quantile')
plt.title(f'Average of Values in {num_quantiles} Quantiles of array1')
# plt.show()
correlation_matrix = np.corrcoef(array1, array2)
correlation_coefficient = correlation_matrix[0, 1]
print(correlation_coefficient)