import os
from dotenv import load_dotenv
import pandas as pd
import duckdb as ddb
import requests
import datetime
import time
import pandas_ta as ta

load_dotenv()
api_key = os.getenv("Alpha_API")
symbol = 'AAPL'
interval = '1'
Stock_lookback_period = 100
Increasing_Mins = 2

#url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&month=2024-07&outputsize=full&apikey={api_key}"

stock_api = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&month=2024-06&entitlement=realtime&outputsize=full&apikey={api_key}'


r = requests.get(stock_api)
key = f'Time Series (1min)'
data = r.json().get(key, {})



df = pd.DataFrame.from_dict(data, orient='index')

df['1. open'] = pd.to_numeric(df['1. open'])
df['2. high'] = pd.to_numeric(df['2. high'])
df['3. low'] = pd.to_numeric(df['3. low'])
df['4. close'] = pd.to_numeric(df['4. close'])
df['5. volume'] = pd.to_numeric(df['5. volume'])

with pd.ExcelWriter('Alpha Vantage Data.xlsx') as writer:
    df.to_excel(writer, sheet_name='sheet1', index=True)