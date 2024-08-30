import asyncio
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from typing import List
import os
from dotenv import load_dotenv
from TrendAnalysis import process_trade

load_dotenv()

API_KEY = os.getenv("Websocket_API")

ws = WebSocketClient(api_key=API_KEY,market="crypto",subscriptions=["XAS.AAVE-USD"])

print("Trading will Comense Now")

# Function to handle incoming messages
async def handle_msg(msg: List[WebSocketMessage]):
    for m in msg:
        m_dict = m.__dict__
        await process_trade(m_dict)

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