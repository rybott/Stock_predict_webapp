import asyncio
from polygon.websocket.models import CryptoTrade
import pandas as pd
import time

class TradeBuffer:
    def __init__(self, size=15, dump_file='data.csv'):
        self.size = size
        self.buffer = pd.DataFrame(columns=["timestamp", "price", "volume"])  # Adjust columns as needed
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
            print(f"Tade Buffer Error - Buffer size {len(self.buffer)}")

    def dump_data(self, trade):
        open('data.txt', 'a').write(f"{trade},")

Buffer = TradeBuffer()

# Function to process each trade
async def process_trade(trade):

    t1 = time.time()
    Buffer.append(trade)
    Buffer.dump_data(trade)
    t2 = time.time()- t1
    print(t2)

    await asyncio.gather(
        save_to_database(trade),
        calculate_moving_average(trade),
        calculate_rsi(trade),
        calculate_bollinger_bands(trade)
    )

# Placeholder for saving to database
async def save_to_database(trade):
    # Save trade data to database
    pass

# Placeholder for calculating moving average
async def calculate_moving_average(trade):
    # Calculate moving average
    pass

# Placeholder for calculating RSI
async def calculate_rsi(trade):
    # Calculate RSI
    pass

# Placeholder for calculating Bollinger Bands
async def calculate_bollinger_bands(trade):
    # Calculate Bollinger Bands
    pass