class Bot:
    def __init__(self, df):
        self.df = df
        self.initial_capital = 10000 # in dollar units
        self.max_positions = 9000 # in dollar units
        
        self.bought_ethereums = 0
        self.cumulative_prices = 0 
        self.positions = 0 # in dollar units
        self.average_buy_price = 0

        self.earned_ethereums = 0

        '''
        TODO: You can make the following variables dynamic
        '''
        self.static_upsilon = 0.002
        self.static_psi = 0.025
        self.static_chi = 0.02
        self.sigma = 0
       
    def buy(self, price, amount):
        self.bought_ethereums += amount / price
        self.positions += amount
        self.cumulative_prices += price * amount
        self.average_buy_price = self.cumulative_prices / self.positions
        # self.printBuyLogs(price, amount)

    def printBuyLogs(self, price, amount):
        print('Current ETH price is: ', price)
        print('amount is: ', amount)
        print('bought ethereums: ', self.bought_ethereums)
        print('average buy price: ', self.average_buy_price)

    def sell(self, price):
        sold_ethereums = self.positions / price
        self.earned_ethereums += (self.bought_ethereums - sold_ethereums)
        self.bought_ethereums = 0
        self.cumulative_prices = 0
        self.positions = 0
        self.average_buy_price = 0
        # self.printSellLogs(price, sold_ethereums)

    def printSellLogs(self, price, sold_ethereums):
        print('Current ETH price is: ', price)
        print('amount is: ', self.positions)
        print('sold ethereums: ', sold_ethereums)
        print('earned ethereums: ', self.earned_ethereums)

    def currentMadeProfit(self, price):
        return ((self.earned_ethereums * price) / self.initial_capital) * 100

    def clearPositions(self, price):
        if self.positions > 0:
            self.sell(price)

    def printResults(self, price):
        print('Amount of Ethereum gained from trading: ', self.earned_ethereums)
        print('Return: ',self.currentMadeProfit(price), '%')


    def determineBuythreshold(self):
        '''
        TODO: Implement the adjustment based on sigma
        '''

        ######################################
        ########### Random example ###########
        ######################################
        # if self.sigma > 0.01:
        #     new_psi = self.static_psi + 0.01
        # elif self.sigma <= 0.01:
        #     new_psi = self.static_psi - 0.01
        ######################################

        new_upsilon = self.static_upsilon # currently using the static upsilon
        
        return self.average_buy_price * (1 - new_upsilon)
    
    
    def determineBuyamount(self):
        '''
        TODO: can be optimized
        '''
        new_chi = self.static_chi
        self.amount = self.initial_capital * new_chi
        return self.amount
    

    def determineSellthreshold(self):
        '''
        TODO: Implement the adjustment based on sigma
        '''

        new_psi = self.static_psi # currently using the static psi

        return self.average_buy_price * (1 + new_psi)
    

    def predictSigma(self):
        '''
        TODO Implement the function that predicts sigma
        '''
        pass


    ##########################################################
    ################ This is the main loop ###################
    ##########################################################
    def run(self):
        for row in self.df.itertuples():
            price = row.close

            buy_amount = self.determineBuyamount()
            
            if self.positions == 0:
                self.buy(price, buy_amount)
                
            elif self.positions > 0:

                buy_threshold = self.determineBuythreshold()
                sell_threshold = self.determineSellthreshold()

                if price <= buy_threshold and self.positions < self.max_positions:
                    self.buy(price, buy_amount)

                elif price >= sell_threshold:
                    self.sell(price)

            '''
            TODO: if you want to adjust the sigma based on predictions, you could do it here for the next iteration
            Example: self.sigma = self.predictSigma() 
            Note: it might not be neccessary to call the model every iteration since the data is minute based
            '''
                    
        self.clearPositions(price)
        self.printResults(price)

        