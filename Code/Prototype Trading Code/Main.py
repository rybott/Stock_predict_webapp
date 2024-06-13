import asyncio
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, CryptoTrade
from typing import List
from polygon import RESTClient
import pandas as pd
import ast

import threading

from TrendAnalysis import process_trade

API_KEY = "s2zC3SQEf3MgBQzTygqvYc9QfLNI_ABq"

ws = WebSocketClient(api_key=API_KEY,market="crypto",subscriptions=["XAS.BTC-USD"])

stop_event = threading.Event()



#client = RESTClient(api_key=API_KEY)
#client.get_snapshot_crypto_book(ticker="BTC-USD")

print("Trading will Comense Now")

# Function to handle incoming messages
async def handle_msg(msg: List[WebSocketMessage]):
    for m in msg:
        m_dict = m.__dict__
        await process_trade(m_dict)

async def Reporting():
    with open('data.txt', 'r') as file:
        content = file.read()
    Dict_list = ast.literal_eval(content)
    df = pd.DataFrame(Dict_list)

    print(df.info())
    print(df.head())

# Function to run the WebSocket client
async def run_ws():
    await ws.connect(processor=handle_msg)

# Main function to run the event loop
async def main():

    await asyncio.gather(
        run_ws()
    )


# Standard boilerplate to run the main function
if __name__ == "__main__":
    asyncio.run(main())