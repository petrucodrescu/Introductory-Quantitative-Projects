%pip install alpha_vantage
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from alpha_vantage.timeseries import TimeSeries #This class used to retrieve stock market data

api = '' #API key goes here
time = TimeSeries(key = api, output_format = 'pandas')
ticker = 'AMZN' #can be changed to any stock on the market

data, meta_data = time.get_daily(symbol = ticker, outputsize = 'full') #meta_data stores the headers and non useful information
n = 20 #number of days used for the window

data['SMA'] = data['4. close'].rolling(window = n).mean()
data['Buysell'] = 0 #this creates a new column with our signal values

data.loc[data['4. close'] > data['SMA'], 'Buysell'] = 1 #if the program recommends to buy it, will use 1
data.loc[data['4. close'] < data['SMA'], 'Buysell'] = -1 #if the program recommends to sell, it will use -1

plt.figure(figsize = (20,8))
plt.plot(data.index, data['4. close'], label = 'Closing Price', color = 'orange')
plt.plot(data.index, data['SMA'], label = f'SMA({n} days)', color = 'blue')

plt.plot(data[data['Buysell'] == 1].index,
         data['4. close'][data['Buysell'] == 1],
         '^', markersize = 10, color = 'g', label = 'Buy') #adds markers for buy signals

plt.plot(data[data['Buysell'] == -1].index,
         data['4. close'][data['Buysell'] == -1],
         'v', markersize = 10, color = 'r', label = 'Sell') #add markers for sell signals

plt.title(f'{ticker} Closing Price and SMA')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc = 'best')

plt.grid(True)
plt.show()
