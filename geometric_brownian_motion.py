# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 13:08:34 2020

@author: harishangaran

STOCK PRICE SIMULATION USING GEOMETRIC BROWNIAN MOTION

The following script uses the stochastic calculus model Geometric Brownian
Motion to simulate the possible path of the stock prices in discrete
time-context.

The path of the stock can vary based on the seed used from the numpy library.
Different seed sequences has differen fixed random block of data, so when you 
change the seed value the path of the stock price changes.

The following model dynamically calls stock prices from the yahoo finance.

Calling the class:

# Positional Arguments
    stock_ticker = Ticker symbol for the stock
    history_period = The time period in days you want to look back
    forecast_period = The time period in days you want to forecast
    seed = The random seed of the NumPy pseudo-random number generator

# Call eg:
    gbm('AMZN',history_period='100d',forecast_period=252,seed=10)

    # Output
        matplotlib plot of the forecasted price and the actual stock price
        movement over history period.

# Getting the values of the stock price movement
        stockPriceVals = gbm('AMZN',history_period='100d',
                        forecast_period=252,seed=10).geometricBrownianMotion()

    # Output
        tuple of forecasted stock prices and x axis values for plotting.
    
    
GBM parameters

# So    :   initial stock price
# dt    :   time increment - daily in this case
# T     :   length of the prediction time horizon(how many time points to predict, same unit with dt(days))
# N     :   number of time points in the prediction time horizon -> T/dt
# t     :   array for time points in the prediction time horizon [1, 2, 3, .. , N]
# mu    :   mean of historical daily returns (drift coefficient)
# sigma :   standard deviation of historical daily returns (diffusion coefficient)
# b     :   array for brownian increments
# W     :   array for brownian path


"""

import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


class gbm:
    def __init__(self,stock_ticker,history_period='100d',forecast_period=252,seed=20):
        self.stockTicker = stock_ticker
        self.historyPeriod = history_period
        self.forecastPeriod = forecast_period
        self.seed = seed
        self.callPrices()
        self.calMuSigma()
        self.brownianMotion()
        self.geometricBrownianMotion()  
        self.plot()
        
    def callPrices(self):
        
        # Calling the price from yahoo finance
        self.stockPrice = yf.Ticker(self.stockTicker).history(self.historyPeriod)
        
        # Later needed for plotting along the x axis of actual historical prices
        self.intOfHistoryPeriod = int(self.historyPeriod.split('d')[0])
        
        # Return dataframes of the stock
        return self.stockPrice,self.intOfHistoryPeriod
    
    def calMuSigma(self):
        
        # Calculate daily return of benchmark and stock
        self.stockPrice['Daily return'] = self.stockPrice['Close'].pct_change(1)
        
        # Calculate mean annualised return
        self.mu = self.stockPrice['Daily return'].mean() * 252
        
        # Calculate annualised standard deviation of the return
        self.sigma = self.stockPrice['Daily return'].std() * np.sqrt(252)
        
        return self.stockPrice,self.mu,self.sigma

    def brownianMotion(self):
        
        np.random.seed(self.seed)  

        # Time step                       
        dt = 1/self.forecastPeriod   
        
        # Brownian increments
        b = np.random.normal(0, 1, int(self.forecastPeriod))*np.sqrt(dt)
        
        # brownian path
        self.W = np.cumsum(b)                             
        return self.W
    
    def geometricBrownianMotion(self): 
        
        # Inital stock price to start with is the last trading day price
        self.So = self.stockPrice['Close'][-1]
        
        self.timeAxis = np.linspace(0,1,self.forecastPeriod + 1)
        
        # X-Axis to plot forecast price
        self.xAxis = np.linspace(
            self.intOfHistoryPeriod,self.forecastPeriod + self.intOfHistoryPeriod,
            self.forecastPeriod+1)
        
        # List of the forecasted prices
        self.S = []
        self.S.append(self.So)
        for i in range(1,int(self.forecastPeriod + 1)):
            drift = (self.mu - 0.5 * self.sigma**2) * self.timeAxis[i]
            diffusion = self.sigma * self.W[i-1]
            S_temp = self.So*np.exp(drift + diffusion)
            self.S.append(S_temp)
        return self.S, self.xAxis

    def plot(self):
        
        # X-Axis to plot actual price
        pt = np.linspace(0,self.intOfHistoryPeriod,self.intOfHistoryPeriod)

        plt.figure(figsize=(12,8),dpi=300)
        plt.plot(pt,self.stockPrice['Close'],label='Actual')
        plt.plot(self.xAxis, self.S,label='Forecast')
        plt.legend()
        plt.ylabel('Stock Price, $')
        plt.xlabel('Tradaing Days')
        plt.title(
            'Geometric Brownian Motion of {} over next {} trading days'.format(
                self.stockTicker,self.forecastPeriod))
        

gbm('MSFT',history_period='504d',forecast_period=252,seed=10)
