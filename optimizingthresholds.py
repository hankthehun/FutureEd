import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from pmdarima.arima import ADFTest
from scipy.stats import pearsonr
import csv
from sklearn.metrics import r2_score
i =0
df = pd.read_csv('/home/saunaq/Desktop/FutureEf/eth-perp_train.csv')
day = np.array([])
d=0
stds = np.array([])
avgs = np.array([])
step_size = 286
count =0
freq =0
average_devs=np.array([])

#store std of t1 in an array, remove last element because its not used to predict anything 
while i<(835779-step_size):
    subset_df = df.iloc[i:i+step_size]
    close_prices = subset_df['close'].to_numpy()
    stds = np.append(stds, np.std(close_prices))
    avgs = np.append(avgs, np.mean(close_prices))
    i+=207
    day = np.append(day,d)
    d+=1
stds = stds[:-1]


#divide data into t2 step chunks, and calculate the average deviation of the negative/positive peaks
#we used the same loop for both of these because the code is relatively similar
#runtime of this algorithme is very large because of the nested for loop so we printed values to a csv after each run to save time for further computation with them 
average_sigmas = np.array([])
for i in range(286, 835779-207,207):
    subset_df = df.iloc[i:i+207]
    close_prices = subset_df['close'].to_numpy()    
    negative = np.array([])  # keeps track of negative values before it tips over moving avg
    negativePeaks = np.array([])  #keeps track of negative/positive peaks
    sigmas = np.array([])   #keeps track of std/moving average ratio
    for j in range(30,203):
        subset_df2 = df.iloc[i+j-30:i+j]
        subset_df3 = df.iloc[i+j+1:i+j+4]
        mvavg = subset_df2['close'].to_numpy()   #contains values that are part of the moving average
        metric = close_prices[j]/np.mean(mvavg)  #metric to predict if it will tip over moving average
        sigmas = np.append(sigmas, stds[int(i/207)-1]/np.mean(mvavg))   #std/moving average ratio
        if(metric>1.01 and len(negative)>0):
            negativePeaks = np.append(negativePeaks, np.min(negative))  #if it tips over moving average, add the minimum negative value to negativePeaks and reset negative
            negative = np.array([])
        if(metric<0.99):
            negative = np.append(negative, metric)  #else keep adding to negative
    if len(negative) > 0:
        negativePeaks = np.append(negativePeaks, np.min(negative))     #if there are still negative values left in negative, add the minimum to negativePeaks

    if len(negativePeaks) > 0:
        average_devs = np.append(average_devs, np.std(negativePeaks))
    average_sigmas = np.append(average_sigmas, np.mean(sigmas))


#In case you want to replicate our results for yourself without spending 5 minutes waiting, replace the file paths with the paths of the applicable csv files and run 
#Only the csvs used for parameter estimation were actually used, and the data for buy side was ommitted because of the symmetric nature of the buy and sell data as shown by the graphs in our report
csv_file_path = 'RSigma_filteredfornewSellPrice.csv'  # Replace with your file path

data_rows = []

with open(csv_file_path, mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader) 
    for row in csv_reader:
        data_rows.append(row)

filtered_sigma = np.array(data_rows, dtype=float)  
csv_file_path = 'new_avg_dev_sell.csv'  

data_rows = []

with open(csv_file_path, mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    for row in csv_reader:
        data_rows.append(row)

average_devs = np.array(data_rows, dtype=float)


array1 = filtered_sigma[:, 0]
array2 = average_devs[:, 0]

combined_data = np.column_stack((array1, array2))

sorted_data = combined_data[combined_data[:, 0].argsort()]

num_buckets = 20

quantiles = np.array_split(sorted_data, num_buckets)

bucket_averages = np.array([bucket[:, 1].mean() for bucket in quantiles])

x_values = [bucket[0, 0] for bucket in quantiles]  
y_values = bucket_averages  

plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, marker='o')

plt.xlabel('Sigma Quantile Boundaries')
plt.ylabel('RelSigma Average Values')
plt.title('Sigma Average Values vs. RelSigma Quantile Boundaries')

plt.grid(True)
plt.show()


