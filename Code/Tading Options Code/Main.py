import requests
import os
from dotenv import load_dotenv
import pandas as pd
import duckdb as ddb
import time
import asyncio
import aiohttp
import datetime

from SQL.Querys import DBconn
con = ddb.connect('testingalphaoptions.duckdb')
db = DBconn(con)

load_dotenv()
api_key = os.getenv("Alpha_API")
symbol = 'AAPL'
interval = '1'

stock_api = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&entitlement=realtime&apikey={api_key}'
options_api = f'https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol={symbol}&entitlement=realtime&apikey={api_key}'

'''
--NOTES--
07/02/24
- Match up the Timestamps for each option call with the timestamp for each
  Batch of stocks to easily match them up
- Make a loop which first checks all the contracts, but when it finds the best
  one then it starts running the below code on just that contract number
  When a buy and sell has occured, we then reset the loop, look for a new best 
  contract that isn't the last contract we traded, and repeats the process

'''

async def call_option_api(session):
    while True:
        # Call the first API
        async with session.get(options_api) as response:
            data = await response.json()
            print("Called first API:", data)
            await analyze_option_api(data)
        # Sleep for 1 second before the next call, yielding control to the event loop
        await asyncio.sleep(5)

# Match up the Timestamps for each option call with the timestamp for each
# Batch of stocks to easily match them up

async def call_stock_api(session):
    while True:
        now = datetime.datetime.now()
        wait_time = 60 - now.second 
        await asyncio.sleep(wait_time)

        call_now = datetime.datetime.now()
        print(f'Stock Called At: {call_now.strftime('%H:%M:%S')}.{call_now.microsecond // 1000:03d}')
        async with session.get(stock_api) as response:
            key = f'Time Series ({interval}min)'
            data = await response.json().get(key,{})

            await analyze_stock_api(data)
        
        await asyncio.sleep(60 - datetime.datetime.now().second)


async def analyze_option_api(data):
    # Add your data analysis code here
    print("Analyzed data from first API:", data)

async def analyze_stock_api(data):
    # Add your data analysis code here
    print("Analyzed data from second API:", data)


async def main():
    async with aiohttp.ClientSession() as session:
        first_api_task = asyncio.create_task(call_option_api(session))
        second_api_task = asyncio.create_task(call_stock_api(session))
        # Run both tasks concurrently
        await asyncio.gather(first_api_task, second_api_task)

# Run the main function
asyncio.run(main())