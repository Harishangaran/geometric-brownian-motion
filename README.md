# geometric-brownian-motion
Forecasting stock price movement using a stochastic calculus process: Geometric Brownian Motion

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

    Output
        matplotlib plot of the forecasted price and the actual stock price
        movement over history period.

# Getting the values of the stock price movement
        stockPriceVals = gbm('AMZN',history_period='100d',
                        forecast_period=252,seed=10).geometricBrownianMotion()

        Output
        tuple of forecasted stock prices and x axis values for plotting.
    
    
#GBM parameters

 So    :   initial stock price
 
 dt    :   time increment - daily in this case
 
 T     :   length of the prediction time horizon(how many time points to predict, same unit with dt(days))
 
 N     :   number of time points in the prediction time horizon -> T/dt
 
 t     :   array for time points in the prediction time horizon [1, 2, 3, .. , N]
 
 mu    :   mean of historical daily returns (drift coefficient)
 
 sigma :   standard deviation of historical daily returns (diffusion coefficient)
 
 b     :   array for brownian increments
 
 W     :   array for brownian path
 
 #Sample Output
 ![GBM Plot](/Sample_output3.png)
 

You are welcome to use this code. Any contribution to improve this model is appreciated.
