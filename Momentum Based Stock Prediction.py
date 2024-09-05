#Work in Progress


#This code was originally written in a jupyter notebook
%pip install alpha_vantage scikit-learn
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

api = '' #API key goes here

time = TimeSeries(key = api, output_format = 'pandas')

def getdata(ticker): #this gets the daily information about the stock 
    data, meta_data = time.get_daily(symbol = ticker, outputsize = 'full')
    return data, meta_data

data['4. close'] = data['4. close'].astype(float)

def rsi(data):
    difference = data['4. close'].diff()
    gain = difference.where(difference > 0, 0)
    loss = difference.where(difference < 0, 0)
    
    averagegain = gain.rolling(window = 14, min_periods = 1).mean()
    averageloss = loss.rolling(window = 14, min_periods = 1).mean()
    
    rs = averagegain/(averageloss + 1e-10)
    rsi = 100 - (100/(1+rs))
    return rsi

stocks = ['AAPL', 'AMZN', 'MSFT', 'GOOGL']

sdata = {} #this will be where the data for our stocks will be located
smetadata = {}

for stock in stocks:
    data, meta_data = getdata(stock)
    data['RSI'] = rsi(data)
    data = data.dropna()

    data['Target'] = 0 #this sets all of the values in this column to zero and then will be changed with the buy and sell signals
    data.loc[data['RSI'] < 30, 'Target'] = 1 #the buy signal
    data.loc[data['RSI'] > 70, 'Target'] = -1 #the sell signal

    sdata[stock] = data
    smetadata[stock] = meta_data

models = {}
eval = {}

for stock, data in sdata.items(): #this loop trains the logistic model on the data for each of the 4 stocks
    input = data[['4. close', 'RSI']]
    prediction = data['Target']

    x_train, x_test, y_train, y_test = train_test_split(input, prediction, test_size = 0.2, random_state = 0)
    model = LogisticRegression()

    model.fit(x_train, y_train)

    models[stock] = model

    y_pred = model.predict(x_test)
    eval[stock]= classification_report(y_test, y_pred)

#for stock, data in sdata.items(): #this loop backtests the strategy
#    model = models[stock]
#    input = data[['4. close', 'RSI']]
#    data['Signal'] = model.predict(input)

#    data['Returns'] = data['4. close'].pct_change()

#    assert len(data['Returns']) == len(data['Signal']), "Mismatch in lengths of Returns and Signal"

#    data['Strategy_Returns'] = data['Returns'] * data['Signal'].shift(1)

#    assert len(data['Strategy_Returns']) == len(data['Returns']), "Mismatch in lengths after shifting"

#    data['Cumulative_Strategy_Returns'] = (1 + data['Strategy_Returns']).cumprod() - 1
#    data['Cumulative_Market_Returns'] = (1 + data['Returns']).cumprod() - 1

#    data[['Cumulative_Strategy_Returns', 'Cumulative_Market_Returns']].plot(figsize=(16, 8))
#    plt.title(f'Cumulative Returns for {stock}')
#    plt.xlabel('Date')
#    plt.ylabel('Cumulative Return')
#    plt.legend(['Strategy Returns', 'Market Returns'])
#    plt.show()

for stock, data, in sdata.items(): #this loop outputs the signalling and RSI values
    fig, ax1 = plt.subplots(figsize = (20, 10))

    ax1.plot(data.index, data['4. close'], color='blue', label='Stock Price')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price')
    ax1.legend(loc = 'upper left')

    buy = data[data['Target'] == 1]
    sell = data[data['Target'] == -1]
    ax1.plot(buy.index, buy['4. close'], '^', markersize = 5, color = 'green', label = 'Buy Signal')
    ax1.plot(sell.index, sell['4. close'], 'v', markersize = 5, color = 'red', label = 'Sell Signal')

    plt.title(f'Stock Price + Signals for {stock}')
    plt.show

    plt.figure(figsize = (20,10))
    plt.plot(data.index, data['RSI'], label = 'RSI', color = 'purple')
    plt.axhline(y = 30, color = 'green', linestyle = '--', label = 'Buy Threshold')
    plt.axhline(y = 70, color = 'red', linestyle = '-', label = 'Sell Threshold')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.title(f'RSI for {stock}')
    plt.legend()
    plt.show()

