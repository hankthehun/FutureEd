import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from pmdarima.arima import ADFTest
from scipy import stats
from pmdarima.arima import ADFTest
from scipy.optimize import minimize
import statsmodels.api as sm
from scipy.stats import kurtosis

df = pd.read_csv('/home/saunaq/Desktop/FutureEf/eth-perp_train.csv')

def blackbox_function(params):
    t1, t2 = params
    if t1 <= 2 or t2 <= 2:
        return 9999999999.0
    if t1 > 24*60 or t2 > 24*60:
        return 9999999999.0
    t1 = int(t1)
    t2 = int(t2)
    day = np.array([])
    d=0
    sigmat1 = np.array([])
    sigmat2 = np.array([])
    i=t1
    while(i<(835781-t2)):
        subset_t1 = df.iloc[i-t1:i]
        subset_t2 = df.iloc[i:i+t2]
        close_prices_t1 = subset_t1['close'].to_numpy()
        close_prices_t2 = subset_t2['close'].to_numpy()
        sigmat1 = np.append(sigmat1, np.std(close_prices_t1)/np.mean(close_prices_t1))
        sigmat2 = np.append(sigmat2, np.std(close_prices_t2)/np.mean(close_prices_t2))
        i+=t2
        day = np.append(day,d)
        d+=1
    difference = np.array([])
    for i in range(0,len(sigmat1)):
        difference = np.append(difference, sigmat2[i]-sigmat1[i])
    return -kurtosis(difference)



initial_guess = [10,10]

# Perform optimization to find the global minimum
result = minimize(blackbox_function, initial_guess, method='Nelder-Mead')

# Extract the optimized parameters and minimum function value
optimal_params = result.x
minimum_value = result.fun


print(f"Optimal Parameters: {optimal_params}")
print(f"Minimum Value: {minimum_value}")