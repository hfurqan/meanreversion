import pandas as pd
import numpy as np
import datetime as dt
import pylab
import time as t
import datetime
from datetime import datetime
from datetime import timedelta
import talib



symbols =['PAEL','TPL','SING','DCL','POWER','FCCL','DGKC','LUCK',
          'THCCL','PIOC','GWLC','CHCC','MLCF','FLYNG','EPCL',
          'LOTCHEM','SPL','DOL','NRSL','AGL','GGL','ICL','AKZO','ICI',
           'WAHN','BAPL','FFC','EFERT','FFBL','ENGRO','AHCL','FATIMA',
          'EFOODS','QUICE','ASC','TREET','ZIL','FFL','CLOV',
          'BGL','STCL','GGGL','TGL','GHGL','OGDC','POL','PPL','MARI',
          'SSGC','SNGP','HTL','PSO','SHEL','APL','HASCOL','RPL','MERIT',
          'GLAXO','SEARL','FEROZ','HINOON','ABOT','KEL','JPGL','EPQL',
          'HUBC','PKGP','NCPL','LPL','KAPCO','TSPL','ATRL','BYCO','NRL','PRL',
          'DWSM','SML','MZSM','IMSL','SKRS','HWQS','DSFL','TRG','PTC','TELE',
          'WTL','MDTL','AVN','NETSOL','SYS','HUMNL','PAKD',
          'ANL','CRTM','NML','NCL','GATM','CLCPS','GFIL','CHBL',
          'DFSM','KOSM','AMTEX','HIRAT','NCML','CTM','HMIM',
           'CWSM','RAVT','PIBTL','PICT','PNSC','ASL',
          'DSL','ISL','CSAP','MUGHAL','DKL','ASTL','INIL','GAIL','MEBL']
start_date = '2016-01-01'
end_date = '2017-05-31'
long_period = 60
short_period = 5
back_test_dates = []

def converter(start_date):
    convert=datetime.strptime(start_date, "%Y-%m-%d")
    return convert

def delta_time(converter,n_days):
    new_date = converter + timedelta(days=n_days)
    return new_date


def data(symbol):
    dates=pd.date_range(start_date,date) 
    df=pd.DataFrame(index=dates)
    df_temp=pd.read_csv('/home/furqan/Desktop/python_data/{}.csv'.format(str(symbol)),usecols=['Date','Close','Low','Open','High','Volume'],
                            parse_dates=True,index_col='Date',na_values=['nan'])
    df=df.join(df_temp)
    df=df.fillna(method='ffill')
    df=df.fillna(method='bfill')
    return df

def selldata(symbol):
    dates=pd.date_range(start_date,end_date) 
    selldf=pd.DataFrame(index=dates)
    df_temp=pd.read_csv('/home/furqan/Desktop/python_data/{}.csv'.format(str(symbol)),usecols=['Date','Close'],
                            parse_dates=True,index_col='Date',na_values=['nan'])
    selldf=selldf.join(df_temp)
    selldf=selldf.fillna(method='ffill')
    selldf=selldf.fillna(method='bfill')
    return selldf

def open_price(df):
    open_price = df['Open']
    open_price = open_price.as_matrix()
    float_open=[float(x) for x in open_price]
    np_float_open = np.array(float_open)
    return np_float_open

def high_price(df):
    high_price = df['High']
    high_price = high_price.as_matrix()
    float_high=[float(x) for x in high_price]
    np_float_high = np.array(float_high)
    return np_float_high

def low_price(df):
    low_price = df['Low']
    low_price = low_price.as_matrix()
    float_low=[float(x) for x in low_price]
    np_float_low = np.array(float_low)
    return np_float_low

def close_price(df):
    close = df['Close']
    close = close.as_matrix()
    float_close=[float(x) for x in close]
    np_float_close = np.array(float_close)
    return np_float_close

def volume(df):
    volume = df['Volume']
    volume = volume.as_matrix()
    float_volume=[float(x) for x in volume]
    np_float_volume = np.array(float_volume)
    return np_float_volume


def rsi_val(closeprice,rsi_date):
    rsi = talib.RSI(closeprice, timeperiod=11)
    dates = pd.date_range(start_date, date)
    rsi = pd.DataFrame(rsi,index=dates)
    rsi.columns = ['RSI']
    rsi = rsi.ix[rsi_date: ,]
    return rsi

def sma_close(closeprice,time_period):
    smaclose = talib.SMA(closeprice,timeperiod = time_period)
    current_smaclose = smaclose[-1]
    return current_smaclose
            
start_date = converter(start_date)
end_date = converter(end_date)
num_days = long_period - 1
start_back_test = delta_time(start_date,num_days)
end_back_test = delta_time(end_date,-1)
delta = end_back_test - start_back_test
#print(delta)
#print('Enter delta plus 1: ')
#x = input()
#x = int(x)

for i in range(0,368):
    date = delta_time(start_back_test,i)
    back_test_dates.append(date)

    


for symbol in symbols:
    buy_date = []
    buy_price = []
    sell_price = []
    sell_date = []
    for date in back_test_dates:
    
        #Get data
        df = data(symbol)

        #RSI date
        rsi_date = delta_time(start_date,11)

        #Arranging Data
        openprice = open_price(df)
        closeprice = close_price(df)
        highprice = high_price(df)
        lowprice = low_price(df)
        volume_symbol = volume(df)

        #Calculating RSI
        rsi = rsi_val(closeprice,rsi_date)
        rsi_current = rsi.ix[-1,]
        rsi_current = rsi_current[0]
    
       #Calculating current close
        current_close = closeprice[-1]

        #Long run average
        long_average = sma_close(closeprice,long_period)
    

        #Short run average
        short_average = sma_close(closeprice, short_period)
    

        if current_close > long_average:
            if current_close <  short_average:
                if rsi_current < 30:
                    buy_date.append(date)
                    buy_price.append(current_close)
    for date in buy_date:
        append_date = delta_time(date,5)
        sell_date.append(append_date)
    sell_df = selldata(symbol)
    for date in sell_date:
        price_sell = sell_df.ix[date, ]
        price_sell = price_sell[0]
        sell_price.append(price_sell)
    win = 0
    loss = 0
    buy_range = len(buy_price)
    if buy_range == 0:
        break
    else:
        for i in range(0,buy_range):
            if buy_price[i] < sell_price[i]:
                win = win + 1
    win_prob = (win/(buy_range))*100
    loss_prob = 100 - win_prob
    print('Last bought on ',buy_date[-1])
    print('Winning Probability for {}'.format(symbol), ' is ', win_prob)
    print('Lossing Probability for {}'.format(symbol), ' is ', loss_prob)
