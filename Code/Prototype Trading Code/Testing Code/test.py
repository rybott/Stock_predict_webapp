import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import alpaca
from alpaca.data.live.option import *
from alpaca.data.historical.option import *
from alpaca.data.requests import *
from alpaca.data.timeframe import *
from alpaca.trading.client import *
from alpaca.trading.stream import *
from alpaca.trading.requests import *
from alpaca.trading.enums import *
from alpaca.common.exceptions import APIError
import os
from dotenv import load_dotenv

trade_api_url = None
trade_api_wss = None
data_api_url = None
option_stream_data_wss = None


load_dotenv()

api_key = os.getenv("Alpaca_API")
secret_key = os.getenv("Alpaca_Secret")


option_data_stream_client = OptionDataStream(api_key, secret_key, url_override = option_stream_data_wss)

# get put options contracts
underlying_symbols = ["SPY"]

# specify expiration date range
now = datetime.now(tz = ZoneInfo("America/New_York"))
day1 = now + timedelta(days = 1)
day60 = now + timedelta(days = 60)

req = GetOptionContractsRequest(
    underlying_symbols = underlying_symbols,                     # specify underlying symbols
    status = AssetStatus.ACTIVE,                                 # specify asset status: active (default)
    expiration_date = None,                                      # specify expiration date (specified date + 1 day range)
    expiration_date_gte = day1.date(),                           # we can pass date object
    expiration_date_lte = day60.strftime(format = "%Y-%m-%d"),   # or string
    root_symbol = None,                                          # specify root symbol
    type = "put",                                                # specify option type: put
    style = ExerciseStyle.AMERICAN,                              # specify option style: american
    strike_price_gte = None,                                     # specify strike price range
    strike_price_lte = None,                                     # specify strike price range
    limit = 100,                                                 # specify limit
    page_token = None,                                           # specify page
)
res = trade_client.get_option_contracts(req)
res.option_contracts[:2]



# get high open_interest contract
open_interest = 0
high_open_interest_contract = None
for contract in res.option_contracts:
    if (contract.open_interest is not None) and (int(contract.open_interest) > open_interest):
        open_interest = int(contract.open_interest)
        high_open_interest_contract = contract
high_open_interest_contract




async def option_data_stream_handler(data):
    print(data)

symbols = [
    high_open_interest_contract.symbol,
]

option_data_stream_client.subscribe_quotes(option_data_stream_handler, *symbols) 
option_data_stream_client.subscribe_trades(option_data_stream_handler, *symbols)

option_data_stream_client.run()