import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import alpaca
from alpaca.trading.client import TradingClient

from alpaca.trading.enums import 

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
PL_percent = float(positions[0].unrealized_intraday_plpc)
