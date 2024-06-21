from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderType, TimeInForce, OrderSide
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest, QueryOrderStatus

import ast
import pandas as pd
import os
from dotenv import load_dotenv
import duckdb as ddb


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

con = ddb.connect('TradingAlgoData.duckdb')

with open('data.txt', 'r') as file:
    content = file.read()
    Dict_list = ast.literal_eval(content)
    df = pd.DataFrame(Dict_list)
    df['start_timestamp'] = pd.to_datetime(df['start_timestamp'], unit='ms')
    df['end_timestamp'] = pd.to_datetime(df['end_timestamp'], unit='ms')
    print(df.info())

# Get the Last time for the order and last entry's time in the database 
# and if it is after then add to database FOR BOTH TABLES

req = GetOrdersRequest(
                status = QueryOrderStatus.ALL,
                symbols = [symbol],
                side = "buy")
Order_df = pd.DataFrame(client.get_orders(req))
print(Order_df.head())

'''
table = 'Price_Data'
con.execute(
    Add Comment 
    CREATE TABLE IF NOT EXISTS Price_Data (
        event_type VARCHAR,
        pair VARCHAR,
        open FLOAT,
        close FLOAT,
        high FLOAT,
        low FLOAT,
        volume FLOAT, 
        vwap FLOAT,
        start_timestamp TIMESTAMP,
        end_timestamp TIMESTAMP,
        avg_trade_size FLOAT
    )
    Add Comment
)



con.register('price_df', df)
con.execute("INSERT INTO Price_Data SELECT * FROM price_df")
con.close()

'''