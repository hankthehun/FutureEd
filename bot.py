import numpy as np
import csv

class Bot:

    def __init__(self, df):
        self.df = df
        self.initial_capital = 10000 # in dollar units
        self.max_positions = 9000 # in dollar units
        self.order_id =0
        self.bought_ethereums = 0
        self.cumulative_prices = 0 
        self.positions = 0 # in dollar units
        self.average_buy_price = 0
        self.pnls=([])
        self.earned_ethereums = 0

        # Output file to track performance
        self.outputfile = 'output.csv'

        # Adjusting static parameters
        self.static_chi = 0.45
        k = 11.2 # Multiple for dynamic upsilon and psi, as data is symmetrical(Higher K reduces number of trades)
        self.b = k # Multiple for Upsilon
        self.s = k # Multiple for psi
        self.l = 30 # Length of rolling average price

        # Cacl sigma
        self.sigma = 0 # For first iteration
        self.window_size = 285  # Define the window size for calculating volatility
        self.price_history = []  # Store historical price data for calculating volatility
        self.sigma_measurement_interval = 207  # Specify the interval for measuring sigma
        self.row_count = 0  # Initialize the row count
        self.next_sigma_measurement_row = 207  # Initialize the next sigma measurement row

    def buy(self, price, amount):
        self.order_id+=1
        self.bought_ethereums += amount / price
        self.positions += amount
        self.cumulative_prices += price * amount
        self.average_buy_price = self.cumulative_prices / self.positions
        # self.printBuyLogs(price, amount)

    def printBuyLogs(self, price, amount):
        self.order_id+=1
        print('Current ETH price is: ', price)
        print('amount is: ', amount)
        print('bought ethereums: ', self.bought_ethereums)
        print('average buy price: ', self.average_buy_price)
        print('position:', self.positions)
        print('order number: ', self.order_id)

    def sell(self, price):
        self.order_id+=1
        sold_ethereums = self.positions / price
        self.earned_ethereums += (self.bought_ethereums - sold_ethereums)
        self.bought_ethereums = 0
        self.cumulative_prices = 0
        self.positions = 0
        self.average_buy_price = 0
        # self.printSellLogs(price, sold_ethereums) #Used for tracking perfomance

    def printSellLogs(self, price, sold_ethereums):
        self.order_id+=1
        print('Current ETH price is: ', price)
        print('amount is: ', self.positions)
        print('sold ethereums: ', sold_ethereums)
        print('earned ethereums: ', self.earned_ethereums)
        print('position:', self.positions)
        print('order number: ', self.order_id)
        self.pnls.append(self.earned_ethereums)


    def currentMadeProfit(self, price):
        return ((self.earned_ethereums * price) / self.initial_capital) * 100

    def clearPositions(self, price):
        if self.positions > 0:
            self.sell(price)

    def printResults(self, price):
        print('Amount of Ethereum gained from trading: ', self.earned_ethereums)
        print('Return: ',self.currentMadeProfit(price), '%')
        print('order no: ', self.order_id)


    def determineBuythreshold(self):
       
        # Calc rolling average
        avg =0
        if len(self.price_history)<self.l+1:
            for i in range(1,-len(self.price_history)+1):
                avg+= self.price_history[-i]
            return (avg/len(self.price_history)) * (1-0.006)    
        
        for i in range(1,self.l):
           avg+= self.price_history[-i]
        avg = avg/(self.l)

        # Calc relative volatility
        re_sigma = self.sigma/(avg)

        # Intervals for dynamic upsilon, intervals are found from average max deviations from avg before reversal
        if re_sigma>0.016:
            new_upsilon = 0.012*self.b/2
        elif re_sigma >0.08:
            new_upsilon = 0.0055*self.b/1.5
        elif re_sigma>0.004:
            new_upsilon = 0.005*self.b
        elif re_sigma >0.0025:
            new_upsilon = 0.004*self.b
        else:
            new_upsilon = 0.006*self.b

        return (avg) * (1-new_upsilon)
    
    
    def determineBuyamount(self):

        new_chi =self.static_chi # Chi is taken as static

        self.amount = self.initial_capital * new_chi
        return min(self.amount, self.max_positions-self.positions)  #modified this formula to ensure position limit was never reached
    

    def determineSellthreshold(self):

        # Calc rolling average
        avg =0
        if len(self.price_history)<self.l+1:
            for i in range(1,-len(self.price_history)+1):
                avg+= self.price_history[-i]
            return (avg/len(self.price_history)) * (1-0.006)    
        
        for i in range(1,self.l):
           avg+= self.price_history[-i]
        avg = avg/(self.l)

        # Calc relative volatility
        re_sigma = self.sigma/(avg)

        #Intervals for dynamic psi
        if re_sigma>0.016:
            new_psi = 0.012*self.s/2
        elif re_sigma >0.08:
            new_psi = 0.0055*self.s/1.5
        elif re_sigma>0.004:
            new_psi = 0.005*self.s
        elif re_sigma >0.0025:
            new_psi = 0.004*self.s
        else:
            new_psi = 0.006*self.s

        return (avg) * (1+new_psi)
    
    # Calc volatility for T1(standard deviation) and make static for T2
    def predictSigma(self):
        if(len(self.price_history)>self.window_size):
            self.sigma = np.std(self.price_history[-self.window_size:])-3.11  # Set self.sigma to the calculated volatility
        else:
            self.sigma = np.std(self.price_history)
        pass


    ##########################################################
    ################ This is the main loop ###################
    ##########################################################

    def run(self):
        for row in self.df.itertuples():
            price = row.close
            self.price_history.append(price)

            buy_amount = self.determineBuyamount()
            
            if self.positions == 0:
                self.buy(price, buy_amount)
                
            elif self.positions > 0:

                buy_threshold = self.determineBuythreshold()
                sell_threshold = self.determineSellthreshold()

                if price <= buy_threshold and self.positions< self.max_positions:
                    self.buy(price, buy_amount)

                elif price >= sell_threshold:
                    self.sell(price)

            self.row_count += 1
            if self.row_count % self.sigma_measurement_interval ==0:
                self.predictSigma()

            
        self.clearPositions(price)
        self.printResults(price)
        #The below code was to track return over time to make sure it was not highly volatile we commented it out for the convenience of the reader but it
        #can be uncommented to see the results
        
        # with open(self.outputfile, mode='w', newline='') as file:
        #     writer = csv.writer(file)
    
        #     for x in self.pnls:
        #         writer.writerow([x])
