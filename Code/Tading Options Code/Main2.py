import os
from dotenv import load_dotenv
import pandas as pd
import duckdb as ddb
import asyncio
import aiohttp
import datetime
import time

from SQL.Querys import DBconn
con = ddb.connect('testingalphaoptions.duckdb')
db = DBconn(con)

load_dotenv()
api_key = os.getenv("Alpha_API")
symbol = 'AAPL'
interval = '1'

stock_api = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&entitlement=realtime&apikey={api_key}'
options_api = f'https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol={symbol}&apikey={api_key}'

async def call_option_api(session):
    while True:
        async with session.get(options_api) as response:
            if response.status == 200:
                t1 = time.time()
                data = await response.json()
                key = 'data'
                option_data = data.get(key, {})
                df = pd.DataFrame(option_data)
                df['Logtime']= pd.Timestamp.now()
                db.InsertOptionQry(df)
                t2 = time.time() - t1

                print(f"Called first API in {t2} seconds:")
                await analyze_option_api(option_data)
            else:
                print(f"Error calling options API: {response.status}")
        await asyncio.sleep(5)

async def call_stock_api(session):
    while True:
        now = datetime.datetime.now()
        wait_time = 60 - now.second
        await asyncio.sleep(wait_time)

        call_now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f'Stock Called At: {call_now}')
        
        async with session.get(stock_api) as response:
            if response.status == 200:
                t1 = time.time()
                data = await response.json()
                key = f'Time Series ({interval}min)'
                stock_data = data.get(key, {})

                df = pd.DataFrame.from_dict(stock_data, orient='index').reset_index()
                df.rename(columns={'index': 'timestamp'}, inplace=True)

                df['Logtime']= pd.Timestamp.now()
                db.InsertStockQry(df)
                t2 = time.time() - t1
                print(f"Stock Added in {t2} seconds")

                await analyze_stock_api(stock_data)
            else:
                print(f"Error calling stock API: {response.status}")
        
        await asyncio.sleep(60 - datetime.datetime.now().second)

async def analyze_option_api(data):
    # Add your data analysis code here
    print("Analyzed data from first API:")

async def analyze_stock_api(data):
    # Add your data analysis code here
    print("Analyzed data from second API:")

async def main():
    async with aiohttp.ClientSession() as session:
        first_api_task = asyncio.create_task(call_option_api(session))
        second_api_task = asyncio.create_task(call_stock_api(session))
        await asyncio.gather(first_api_task, second_api_task)

# Run the main function
asyncio.run(main())
