import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import alpaca
from alpaca.data.live.crypto import *
from alpaca.data.historical.crypto import *
from alpaca.data.requests import *
from alpaca.data.timeframe import *
from alpaca.trading.client import *
from alpaca.trading.stream import *
from alpaca.trading.requests import *
from alpaca.trading.enums import *
from alpaca.common.exceptions import APIError


api_key = "PKYBOP7WCHJG8U2UWBVB"
secret_key = "WyL7X8v4OBkuFFT4urOPMLZ9EG88HBAFxWRsuRE5"
paper = True 

trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=None)

#acct = trade_client.get_account()
#print(acct)

# get all open positions
# ref. https://docs.alpaca.markets/reference/getallopenpositions-1
positions = trade_client.get_all_positions()
Quantity = float(positions[0].qty)
print(Quantity)