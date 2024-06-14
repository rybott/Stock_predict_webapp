import asyncio
from polygon.websocket.models import CryptoTrade
import pandas as pd
import time

import alpaca
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderType, TimeInForce, OrderSide
from alpaca.trading.requests import MarketOrderRequest

class TradeBuffer:
    def __init__(self, size=15, dump_file='data.csv'):
        self.size = size
        self.buffer = pd.DataFrame(columns=["event_type", "pair", "open", "close", "high", "low", "volume", "vwap", "start_timestamp", "end_timestamp", "avg_trade_size"])  # Adjusted columns
        open('data.txt', 'w').close()

    def append(self, candle):
        # Convert trade to pandas Series
        trade_series = pd.Series(candle, index=self.buffer.columns)
        if len(self.buffer) == self.size:
            self.buffer = self.buffer.shift(-1)
            self.buffer.iloc[-1] = trade_series
        elif len(self.buffer) < self.size:
            self.buffer = pd.concat([self.buffer, trade_series.to_frame().T], ignore_index=True)
        else:
            print(f"Trade Buffer Error - Buffer size {len(self.buffer)}")

    def dump_data(self, candle):
        open('data.txt', 'a').write(f"{candle},")

    def get_data(self):
        return self.buffer
    
    def get_price(self, candle):
        self.price = candle['high']
        return self.price

class TrendAnalysis():
    def __init__(self, buffer_df):
        self.TradeStat = False
        self.Buffer = buffer_df

    def calculate_moving_average(self):
        # Calculate moving average
        pass

    # Placeholder for calculating RSI
    def calculate_rsi(self):
        # Calculate RSI
        pass

    # Placeholder for calculating Bollinger Bands
    def calculate_bollinger_bands(self):
        # Calculate Bollinger Bands
        pass

    def TradeAnalysis(self):
        if not self.calculate_bollinger_bands():
            self.TradeStat = False
            return self.TradeStat

        if not self.calculate_rsi():
            self.TradeStat = False
            return self.TradeStat

        if not self.calculate_moving_average():
            self.TradeStat = False
            return self.TradeStat

        self.TradeStat = True
        return self.TradeStat




class ProtoflioStatus():
    def __init__(self):
        pass

    def Tru(self, client):
        positions = client.get_all_positions()
        Quantity = float(positions[0].qty)
        PL_percent = float(positions[0].unrealized_intraday_plpc)

        # If Loosing Money Close all Positions (Which is just BTC)
        if PL_percent < -.02: # Two Percent
            req = MarketOrderRequest(
            symbol = symbol,
            qty = Quantity,
            side = OrderSide.SELL,
            type = OrderType.MARKET,
            time_in_force = TimeInForce.DAY)
            res = client.submit_order(req)
            return False
        else:
            return True
            



api_key = "PKYBOP7WCHJG8U2UWBVB"
secret_key = "WyL7X8v4OBkuFFT4urOPMLZ9EG88HBAFxWRsuRE5"
paper = True 

Buffer = TradeBuffer()
symbol = "BTC/USD"
trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=None)


# Function to process each trade
async def process_trade(trade):
    t1 = time.time()
    Buffer.append(trade)
    Buffer.dump_data(trade)
    
    Buffer_df = Buffer.get_data()

    Portfolio = ProtoflioStatus().Tru()

    if len(Buffer_df) >=15:
        Analysis = TrendAnalysis(Buffer_df).TradeAnalysis()

        if Portfolio == True and Analysis == True:
            req = MarketOrderRequest(
            symbol = symbol,
            qty = 0.01,
            side = OrderSide.BUY,
            type = OrderType.MARKET,
            time_in_force = TimeInForce.DAY)

        res = trade_client.submit_order(req)

        print("Made Trade")

    t2 = time.time()- t1
    print(t2)


