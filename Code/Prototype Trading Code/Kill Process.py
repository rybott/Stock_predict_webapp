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
symbol = os.getenv("Symbol")

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
    df['start_timestamp'] = pd.to_datetime(df['start_timestamp'], unit='ms').dt.tz_localize('UTC')
    df['end_timestamp'] = pd.to_datetime(df['end_timestamp'], unit='ms').dt.tz_localize('UTC')

df = df[['start_timestamp', 'end_timestamp', 'event_type', 'pair', 'open', 'close', 'high', 'low', 'volume', 'vwap', 'avg_trade_size']]
print(df.info())

req = GetOrdersRequest(
                status = QueryOrderStatus.ALL,
                symbols = [symbol],
                side = "buy")

orders = client.get_orders(req)

order_data = []
for order in orders:
    order_data.append({
        'id': order.id, # Primary Key
        'client_order_id': order.client_order_id,
        'created_at': pd.to_datetime(order.created_at),
        'updated_at': pd.to_datetime(order.updated_at),
        'submitted_at': pd.to_datetime(order.submitted_at),
        'filled_at': pd.to_datetime(order.filled_at) if order.filled_at else None,
        'expired_at': pd.to_datetime(order.expired_at) if order.expired_at else None,
        'canceled_at': pd.to_datetime(order.canceled_at) if order.canceled_at else None,
        'failed_at': pd.to_datetime(order.failed_at) if order.failed_at else None,
        'asset_id': order.asset_id,
        'symbol': order.symbol,
        'asset_class': order.asset_class,
        'qty': order.qty,
        'filled_qty': order.filled_qty,
        'type': order.type,
        'side': order.side,
        'time_in_force': order.time_in_force,
        'limit_price': order.limit_price,
        'stop_price': order.stop_price,
        'filled_avg_price': order.filled_avg_price,
        'status': order.status,
        'extended_hours': order.extended_hours,
        'legs': order.legs
    })

df_orders = pd.DataFrame(order_data)
print(df_orders.info())

con.execute(
    '''
    CREATE TABLE IF NOT EXISTS Price_Data (
        start_timestamp TIMESTAMP PRIMARY KEY,
        end_timestamp TIMESTAMP,
        event_type VARCHAR,
        pair VARCHAR,
        open FLOAT,
        close FLOAT,
        high FLOAT,
        low FLOAT,
        volume FLOAT, 
        vwap FLOAT,
        avg_trade_size FLOAT
    )
    '''
)

con.execute(
    '''
    CREATE TABLE IF NOT EXISTS Order_Data (
        id VARCHAR PRIMARY KEY,
        client_order_id VARCHAR,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        submitted_at TIMESTAMP,
        filled_at TIMESTAMP,
        expired_at TIMESTAMP,
        canceled_at TIMESTAMP,
        failed_at TIMESTAMP,
        asset_id VARCHAR,
        symbol VARCHAR,
        asset_class VARCHAR,
        qty FLOAT,
        filled_qty FLOAT,
        type VARCHAR,
        side VARCHAR,
        time_in_force VARCHAR,
        limit_price FLOAT,
        stop_price FLOAT,
        filled_avg_price FLOAT,
        status VARCHAR,
        extended_hours BOOLEAN,
        legs VARCHAR
    )
    '''
)

con.register('price_df', df)
con.execute(
    '''
    INSERT INTO Price_Data
    SELECT 
        CAST(start_timestamp AS TIMESTAMP) AS start_timestamp,
        end_timestamp,
        event_type,
        pair,
        open,
        close,
        high,
        low,
        volume,
        vwap,
        avg_trade_size
    FROM price_df
    WHERE start_timestamp NOT IN (SELECT start_timestamp FROM Price_Data)
    '''
)

con.register('orders_df', df_orders)
con.execute(
    '''
    INSERT INTO Order_Data
    SELECT * FROM orders_df
    WHERE id NOT IN (SELECT id FROM Order_Data)
    '''
)