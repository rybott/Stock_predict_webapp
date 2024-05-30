import asyncio
from alpaca.trading.client import TradingClient
from alpaca.data.live import CryptoDataStream
import time

API_KEY = "PKW7DQECIZLURTL0KOAA"
S_Key = "tkNL2VUeS6lSVtWT6BosI4nfm0sgZw37z6HDllKj"
trading_client = TradingClient(API_KEY,S_Key, paper=True)

stream = CryptoDataStream(API_KEY, S_Key)

print(stream)

last_bar_time = None
last_trade_time = None
last_quote_time = None

async def on_crypto_bar(data):
    global last_bar_time
    current_time = time.time()
    if last_bar_time is not None:
        time_diff = current_time -last_bar_time
        print(f"Time since last Bar: {time_diff} seconds")
    last_bar_time = current_time
    print(f"Received bar data: {data}")

async def on_crypto_trade(data):
    global last_trade_time
    current_time = time.time()
    if last_trade_time is not None:
        time_diff = current_time - last_trade_time
        print(f"Time since last trade update: {time_diff} seconds")
    last_trade_time = current_time
    print(f"Received trade data: {data}")

async def on_crypto_quote(data):
    global last_quote_time
    current_time = time.time()
    if last_quote_time is not None:
        time_diff = current_time - last_quote_time
        print(f"Time since last quote update: {time_diff} seconds")
    last_quote_time = current_time
    print(f"Received quote data: {data}")

async def main():
    await stream.subscribe_bars(on_crypto_bar,"ETH/USD", "BTC/USD")

    await stream.subscribe_trades(on_crypto_trade, 'ETH/USD', 'BTC/USD')

    await stream.subscribe_quotes(on_crypto_quote, 'ETH/USD', 'BTC/USD')

    await stream.run()

asyncio.run(main())