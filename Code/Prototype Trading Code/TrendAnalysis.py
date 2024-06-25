import asyncio
import pandas as pd
import time
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderType, TimeInForce, OrderSide
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest, QueryOrderStatus
import os
from dotenv import load_dotenv

load_dotenv()

class TradeBuffer:
    def __init__(self, size=15, dump_file='data.csv'):
        self.size = size
        self.Cached_Price = .0001 # Placeholder
        self.Max_Price = 0 # Placeholder
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
    
    def Update_Cache_Price(self, price):
        self.Cached_Price = price
    
    def Get_Cached_Price(self):
        return self.Cached_Price
    
    def Reset_Max_Price(self, price):
        self.Max_Price = price

    def Get_Max_TrailingLoss(self, price):
        if price > self.Max_Price:
            self.Max_Price = price
        return self.Max_Price - (self.Max_Price*.01)

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
        self.CurrentOrders = pd.DataFrame(columns=["EntryTime", "symbol", "PurchaseStockPriceActual", 
                                              "PurchaseStockPriceAvg", "quantity",
                                              "PurchasePrice", "Adj_CostBasis",
                                              "RollingCostBasis","Sell"])
        

    def RecordOrder(self,ticker, client, price):

        req = GetOrdersRequest(
                status = QueryOrderStatus.ALL,
                symbols = [ticker],
                side = "buy")
        last_order = client.get_orders(req)[0]
        try:
            self.EntryTime = pd.Timestamp.now()
            self.symbol = ticker
            self.PurchaseStockPriceActual = price
            self.PurchaseStockPriceAvg = float(last_order.filled_avg_price)
            self.quantity = float(last_order.filled_qty)
            self.PurchasePrice = float(last_order.notional)
            self.Adj_CostBasis = self.PurchaseStockPriceAvg / self.quantity
            self.RollingCostBasis = price 
            self.Sell = False

            next_index = len(self.CurrentOrders)

            self.CurrentOrders.loc[next_index] = [self.EntryTime, self.symbol, self.PurchaseStockPriceActual, 
                                                self.PurchaseStockPriceAvg, self.quantity,
                                                self.PurchasePrice, self.Adj_CostBasis,
                                                self.RollingCostBasis,self.Sell]
        except:
            print("Failed to Record Order")
        
    def DropOrder(self):
        pass

    def PositionAnalysis(self, client, Max_Price, New_price, buffer):
        '''
        # For the Future
        1. Apply a function to every row of the dataframe to see IF current Price < Rolling Cost Basis = Sell == True
        2. Otherwise Update rolling cost Basis
        '''
        if New_price >= Max_Price:
            return True
        else:
            self.positions = client.get_all_positions()
            if self.counter == 1:
                self.counter = self.counter + 1
                return True
            elif len(self.positions) == 0:
                self.counter = self.counter + 1
                return True
            else:
                buffer.Reset_Max_Price(New_price)
                print("Sold Positions")
                self.counter = self.counter + 1
                Quantity = float(self.positions[0].qty)
                req = MarketOrderRequest(
                    symbol = symbol,
                    qty = Quantity,
                    side = OrderSide.SELL,
                    type = OrderType.MARKET,
                    time_in_force = TimeInForce.GTC)
                self.res = client.submit_order(req)
                return False   
                 
            
    def MakeMarketOrder(self,Ticker, Client, Price, Amount):
        t1 = time.time()
        print("Made Trade")
        req = MarketOrderRequest(
                symbol = Ticker,
                notional = Amount,
                side = OrderSide.BUY,
                type = OrderType.MARKET,
                time_in_force = TimeInForce.GTC)
        Client.submit_order(req)
        self.RecordOrder(Ticker,Client, Price)
        t2 = t1 - time.time()
        

api_key = os.getenv("Alpaca_API")
secret_key = os.getenv("Alpaca_Secret")
paper = True 
trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=None)

Buffer = TradeBuffer()
PortfolioStatus = ProtoflioStatus()
symbol = os.getenv("Symbol")
trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=None)


# Function to process each trade
async def process_trade(trade):
    t1 = time.time()
    Buffer.append(trade)
    Buffer.dump_data(trade)
    
    Buffer_df = Buffer.get_data()
    price = Buffer.Get_Cached_Price()
    New_price = trade['low']

    
    Trailing_Price = Buffer.Get_Max_TrailingLoss(trade['low'])
    Max_Price = Trailing_Price / .99


    Portfolio_Flag = PortfolioStatus.PositionAnalysis(trade_client, Trailing_Price, New_price, Buffer)

    if len(Buffer_df) >=15:
        Analysis_Flag = TrendAnalysis(Buffer_df).TradeAnalysis()

        if Portfolio_Flag == True and Analysis_Flag == True:
            PortfolioStatus.MakeMarketOrder(symbol, trade_client, price, Amount= 10,)
    
    Buffer.Update_Cache_Price(New_price)

    t2 = time.time()- t1
    print(f"{t2} Seconds | Price = {New_price} | Max_Price = {Max_Price} | Trailing_Price = {Trailing_Price}")

