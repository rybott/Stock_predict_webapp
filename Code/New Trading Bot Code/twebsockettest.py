'''
import asyncio
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, CryptoTrade
from typing import List
from polygon import RESTClient

from TrendAnalysis import process_trade

API_KEY = "s2zC3SQEf3MgBQzTygqvYc9QfLNI_ABq"

ws = WebSocketClient(api_key=API_KEY,market="crypto")
ws = WebSocketClient(api_key=API_KEY,market="crypto",subscriptions=["XAS.BTC-USD"])

async def handle_msg(msg: List[WebSocketMessage]):
    for m in msg: 
        print(m)


async def run_ws():
    #ws.subscribe("X.BTC")
    await ws.connect(processor=handle_msg)

# Main function to run the event loop
async def main():
    await asyncio.gather(
        run_ws()
    )

# Standard boilerplate to run the main function
if __name__ == "__main__":
    asyncio.run(main())
'''

import pandas as pd
import pyarrow.feather as feather

# Path to the Feather file
file_path = r'Code\New Trading Bot Code\data.feather'

# Read the Feather file into a Pandas DataFrame
df = feather.read_feather(file_path)

# Print the DataFrame
print(df)