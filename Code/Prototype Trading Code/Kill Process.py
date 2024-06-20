import asyncio
import pandas as pd
import time
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderType, TimeInForce, OrderSide
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest, QueryOrderStatus
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("Alpaca_API")
secret_key = os.getenv("Alpaca_Secret")
paper = True 
client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=None)
symbol = "BTC/USD"

positions = client.get_all_positions()
            
if len(positions) == 0:
    pass
else:
    Quantity = float(positions[0].qty)
    req = MarketOrderRequest(
        symbol = symbol,
        qty = Quantity,
        side = OrderSide.SELL,
        type = OrderType.MARKET,
        time_in_force = TimeInForce.GTC)
    res = client.submit_order(req)