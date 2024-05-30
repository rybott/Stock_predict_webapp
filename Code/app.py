from alpaca.data.live import CryptoDataStream
import time

stream = CryptoDataStream("PKW7DQECIZLURTL0KOAA","tkNL2VUeS6lSVtWT6BosI4nfm0sgZw37z6HDllKj")

async def handle_trade(data):
    print(data)

stream.subscribe_trades(handle_trade, "ETH/USD")

stream.run()


