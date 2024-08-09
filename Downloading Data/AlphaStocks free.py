import requests
import os
from dotenv import load_dotenv
import pandas as pd
import duckdb as ddb
import time
import datetime

load_dotenv()
api_key = '0S92QX7GKGAOSWED'
con = ddb.connect('datadump.duckdb')


# Finshed Stocks AAPL AMZN SPY
listof_stocks = ['AAPL']
listof_intervals = [1,5]
first_year = 2024
current_year = 2024
current_month = 8


con.execute('''
    CREATE TABLE IF NOT EXISTS Stocks (
        Datetime TIMESTAMP,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume FLOAT,
        Stock VARCHAR(10),
        interval FLOAT
    )''') 


    
def getstockdata(ticker,inter, yr, mth):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={inter}min&month={yr}-{mth}&apikey={api_key}'
    r = requests.get(url)
    print(r)
    key = f'Time Series ({inter}min)'
    data = r.json().get(key, {})
    df = pd.DataFrame.from_dict(data, orient='index')


    df.index = pd.to_datetime(df.index)
    df['Datetime'] = df.index.strftime('%Y-%m-%d %H:%M:%S.%f')
    df['Interval'] = inter
    df['Stock'] = ticker
    
    df = df[["Datetime","1. open", "2. high", "3. low", "4. close", "5. volume", "Stock","Interval"]].copy()

    time.sleep(.5)

    print(df.info())

    con.register('df', df)
    con.execute(
        '''
        INSERT INTO Stocks
        SELECT 
            strptime(Datetime, '%Y-%m-%d %H:%M:%S.%f') as Datetime,
            "1. open" as open,
            "2. high" as high,
            "3. low" as low, 
            "4. close" as close, 
            "5. volume" as volume,
            Stock,
            Interval,
        FROM df
        WHERE Datetime NOT IN (SELECT Datetime FROM Stocks)
        ''')
    print('inserted')

counter = 0
for tick in listof_stocks:
    try:
        for interval in listof_intervals:
            for i in range(20):
                year = first_year+i
                if year > current_year:
                    break
                elif year == current_year:
                    for i in range(current_month):
                        month = i+1
                        month_str1 = str(month).zfill(2)
                        getstockdata(tick,interval,year,month_str1)
                        counter = counter +1
                        
                else:
                    for i in range(12):
                        month = i+1
                        month_str2 = str(month).zfill(2)
                        getstockdata(tick,interval,year,month_str2)
                        counter = counter +1
    except:                
        print(f"Error with ticker {tick}")
print("finished")







