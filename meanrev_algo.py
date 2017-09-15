import pandas as pd
import numpy as np
import time as t
import datetime
from datetime import datetime
from datetime import timedelta
import talib

t0 = t.time()


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


long_period = 120
short_period = 5
stocks = []

def converter(start_date):
    convert=datetime.strptime(start_date, "%Y-%m-%d")
    return convert

def delta_time(converter,n_days):
    new_date = converter + timedelta(days=n_days)
    return new_date


def data(symbol):
    dates=pd.date_range(start_date,end_date) 
    df=pd.DataFrame(index=dates)
    df_temp=pd.read_csv('/home/furqan/Desktop/python_data/{}.csv'.format(str(symbol)),usecols=['Date','Close','Low','Open','High','Volume'],
                            parse_dates=True,index_col='Date',na_values=['nan'])
    df=df.join(df_temp)
    df=df.fillna(method='ffill')
    df=df.fillna(method='bfill')
    return df

def close_price(df):
    close = df['Close']
    close = close.as_matrix()
    float_close=[float(x) for x in close]
    np_float_close = np.array(float_close)
    return np_float_close

def sma_close(closeprice,time_period):
    smaclose = talib.SMA(closeprice,timeperiod = time_period)
    current_smaclose = smaclose[-1]
    return current_smaclose
    
start_date = '2016-01-01'
end_date = '2017-08-14'
start_date = converter(start_date)
end_date = converter(end_date)

for symbol in symbols:
    
    #Get data
    df = data(symbol)


    #Arranging Data
    closeprice = close_price(df)

    #Calculating current close
    current_close = closeprice[-1]

    #Long run average
    long_average = sma_close(closeprice,long_period)
    

    #Short run average
    short_average = sma_close(closeprice, short_period)
    

    if current_close > long_average:
        if current_close <  short_average:
            stocks.append(symbol)
            
print(stocks)
t1 =t.time()
print('Exec time is ', t1-t0)         