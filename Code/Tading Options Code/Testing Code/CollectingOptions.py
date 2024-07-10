import requests
import os
from dotenv import load_dotenv
import pandas as pd
import duckdb as ddb
import time
import datetime


load_dotenv()
api_key = os.getenv("Alpha_API")
con = ddb.connect(r'C:\Design Folder\RBGithub\Trading_Algo_Data\testingalphaoptions.duckdb')
symbol = 'AAPL'
function = 'REALTIME_OPTIONS'
contract = 'AAPL240628C00100000'

#url = f'https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol={symbol}&apikey={api_key}'
#url = f'https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol={symbol}&entitlement=realtime&apikey={api_key}'

url = f'https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol={symbol}&entitlement=realtime&apikey={api_key}'

def is_market_open():
    now = datetime.datetime.now()
    start_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
    end_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
    return start_time <= now <= end_time

while True:
    if is_market_open():
        r = requests.get(url)
        key = f'data'
        data = r.json().get(key, {})

        df = pd.DataFrame(data)
        df['Logtime'] = pd.Timestamp.now()

        con.execute(
            '''
            CREATE TABLE IF NOT EXISTS Options (
                contractID VARCHAR,
                symbol VARCHAR,
                expiration VARCHAR,
                strike VARCHAR,
                type VARCHAR,
                last VARCHAR,
                mark VARCHAR,
                bid VARCHAR,
                bid_size VARCHAR,
                ask VARCHAR,
                ask_size VARCHAR,
                volume VARCHAR,
                open_interest VARCHAR,
                date VARCHAR,
                Logtime TIMESTAMP
            )
            '''
        )

        con.register('df', df)
        con.execute(
            '''
            INSERT INTO Options
            SELECT 
                contractID,
                symbol,
                expiration,
                strike,
                type,
                last,
                mark,
                bid,
                bid_size,
                ask,
                ask_size,
                volume,
                open_interest,
                date,
                CAST(Logtime as TIMESTAMP) as Logtime
            FROM df
            WHERE Logtime NOT IN (SELECT Logtime FROM Options)
            ''')
        
        time.sleep(5)
    else:
        print("Market Not Open")
        break

con.close()
