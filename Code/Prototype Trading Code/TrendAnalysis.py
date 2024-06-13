import asyncio
from polygon.websocket.models import CryptoTrade
import pandas as pd
import time

from alpaca.trading.requests import TrailingStopOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

class TradeBuffer:
    def __init__(self, size=15, dump_file='data.csv'):
        self.size = size
        self.buffer = pd.DataFrame(columns=["event_type", "pair", "open", "close", "high", "low", "volume", "vwap", "start_timestamp", "end_timestamp", "avg_trade_size"])  # Adjusted columns
        open('data.txt', 'w').close()

    def append(self, trade):
        # Convert trade to pandas Series
        trade_series = pd.Series(trade, index=self.buffer.columns)
        if len(self.buffer) == self.size:
            self.buffer = self.buffer.shift(-1)
            self.buffer.iloc[-1] = trade_series
        elif len(self.buffer) < self.size:
            self.buffer = pd.concat([self.buffer, trade_series.to_frame().T], ignore_index=True)
        else:
            print(f"Trade Buffer Error - Buffer size {len(self.buffer)}")

    def dump_data(self, trade):
        open('data.txt', 'a').write(f"{trade},")

    def get_data(self):
        return self.buffer
    
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
        # This is where you will call the API to determine losses
        self.Status = True
    def Tru(self):
        return self.Status




Buffer = TradeBuffer()
symbol = "BTC/USD"

# Function to process each trade
async def process_trade(trade):
    t1 = time.time()
    Buffer.append(trade)
    Buffer.dump_data(trade)
    
    Buffer_df = Buffer.get_data()

    if len(Buffer_df) >=15:
        Analysis = TrendAnalysis(Buffer_df).TradeAnalysis()
        Portfolio = ProtoflioStatus().Tru()
        # print(Analysis)

        test_df = Buffer.get_data()
        print(test_df.info())
        print(test_df)

        req = TrailingStopOrderRequest(
            symbol = symbol,
            notional = 10,
            side = OrderSide.BUY,
            time_in_force = TimeInForce.DAY,
            trail_price = 6.15
        )

        print(req)

    t2 = time.time()- t1
    print(t2)


