import requests
import os
from dotenv import load_dotenv
import pandas as pd
import duckdb as ddb
import time
import datetime

load_dotenv()
api_key = os.getenv("Alpha_API")
con = ddb.connect('datadump.duckdb')
symbol = 'AAPL'

listof_stocks = ['AAPL','SPY','AMZN','TSLA','KO','BAC','NVDA','GE','XOM','JNJ','PG','WMT','BA','GS','MCD','AMD','WST']
listof_currencies = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'AUD/USD','USD/CHF','USD/CAD','NZD/USD0','EUR/GBP','GBP/JPY','EUR/JPY']
listof_intervals = [1,5]
first_year = 2010
current_year = 2024
current_month = 6


con.execute('''
    CREATE TABLE IF NOT EXISTS Stocks (
        Timestamp TIMESTAMP,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume FLOAT,
        interval FLOAT
    )''') 


def getstockdata(ticker,inter, yr, mth):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={inter}min&month={yr}-{mth}&entitlement=realtime&outputsize=full&apikey={api_key}'
    r = requests.get(url)
    key = f'Time Series ({inter}min)'
    data = r.json().get(key, {})
    df = pd.DataFrame.from_dict(data, orient='index')

    df.index = pd.to_datetime(df.index)
    df['Timestamp'] = df.index

    con.register('df', df)
    con.execute(
        '''
        INSERT INTO Stocks
        SELECT 
            Timestamp,
            "1. open" as open,
            "2. high" as high,
            "3. low" as low, 
            "4. close" as close, 
            "5. volume" as volume,
        FROM df
        WHERE Timestamp NOT IN (SELECT Timestamp FROM Stocks)
        ''')

    

for tick in listof_stocks:
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

            else:
                for i in range(12):
                    month = i+1
                    month_str2 = str(month).zfill(2)
                    getstockdata(tick,interval,year,month_str2)

        break





'''
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&month=2024-06&entitlement=realtime&outputsize=full&apikey={api_key}'
        
        r = requests.get(url)
        key = f'Time Series (1min)'
        data = r.json().get(key, {})

        print(data)

        df = pd.DataFrame.from_dict(data, orient='index')

        df.index = pd.to_datetime(df.index)


        con.register('df', df)
        con.execute(
            ```
            INSERT INTO Stocks
            SELECT 
                Timestamp,
                "1. open" as open,
                "2. high" as high,
                "3. low" as low, 
                "4. close" as close, 
                "5. volume" as volume,
            FROM df
            WHERE Timestamp NOT IN (SELECT Timestamp FROM Stocks)
            ````)
            
'''