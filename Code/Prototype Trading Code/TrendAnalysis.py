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
        self.price = candle['low']
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

    def DumbtradeAnalysis(self):
        # Looks at the last four candles, three increases
        Last_Candles = 4

        last_VWAPs = self.Buffer['vwap'].iloc[-Last_Candles:]
        last_lows = self.Buffer['low'].iloc[-Last_Candles:]

        VWAP_differences = last_VWAPs.diff().dropna()
        lows_differences = last_lows.diff().dropna()

        NumberOf_Positives = (VWAP_differences > 0).sum() + (lows_differences > 0).sum()
        
        return NumberOf_Positives >= 5


    def TradeAnalysis(self):

        '''
        Good Trade Analysis

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
        
        '''

        self.TradeStat = self.DumbtradeAnalysis()
        return self.TradeStat
    



class ProtoflioStatus():
    def __init__(self):
        self.counter = 1
        self.buffer = pd.DataFrame(columns=["Position_ID","EntryTime", "ExitTime", "Ticker", "Entry_Price", "Purchase Price", "Quantity", "Adj_Basis", "Current_Price", "FeeAdj_Basis", "Sell"])
        
    def RecordPurchase(ticker):
        Current_Time = time.strftime("%Y-%h-%d %H:%M:%S",time.localtime())
        EntryTime = pd.to_datetime(Current_Time)
        symbol = ticker
        # Figure out how to get all the trades you made not poisitions(There is only one position)
        pass

    def GetPositionData():
    # This is where you will calculate the P/L
        pass

    def Tru(self, client):
        self.positions = client.get_all_positions()
        if self.counter == 1:
            self.counter = self.counter + 1
            return True
        elif len(self.positions) == 0:
            self.counter = self.counter + 1
            return True
        else:
            self.counter = self.counter + 1
            Quantity = float(self.positions[0].qty)
            PL_percent = float(self.positions[0].unrealized_intraday_plpc)

            # If Loosing Money Close all Positions (Which is just BTC)
            if PL_percent < -.02: # Two Percent
                req = MarketOrderRequest(
                    symbol = symbol,
                    qty = Quantity,
                    side = OrderSide.SELL,
                    type = OrderType.MARKET,
                    time_in_force = TimeInForce.GTC)
                self.res = client.submit_order(req)
                return False
            else:
                return True
            
    def MakeMarketOrder(Ticker,Amount):
        req = MarketOrderRequest(
                symbol = Ticker,
                notional = Amount,
                side = OrderSide.BUY,
                type = OrderType.MARKET,
                time_in_force = TimeInForce.GTC)
        trade_client.submit_order(req)
        print("Made Trade")






api_key = "PKCCX01QH75BPKJDIR4Y"
secret_key = "xkJ9Ylyc6phDftfiPXL11sMMpT2vzgEnL2BudWJA"
paper = True 
trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=None)

Buffer = TradeBuffer()
PortflioStatus = ProtoflioStatus()
symbol = "BTC/USD"
trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=None)

Portfolio = PortflioStatus()

# Function to process each trade
async def process_trade(trade):
    t1 = time.time()
    Buffer.append(trade)
    Buffer.dump_data(trade)
    
    Buffer_df = Buffer.get_data()

    
    Portfolio_Flag = Portfolio.Tru(trade_client)

    if len(Buffer_df) >=15:
        Analysis_Flag = TrendAnalysis(Buffer_df).TradeAnalysis()

        if Portfolio_Flag == True and Analysis_Flag == True:
            Portfolio.MakeMarketOrder(10)

    t2 = time.time()- t1
    print(t2)


