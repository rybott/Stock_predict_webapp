import os
from dotenv import load_dotenv
import pandas as pd
import duckdb as ddb
import datetime
import time
import pandas_ta as ta


def EMA(packet, value):
    # PAcket = df
    # value = EMA8, EMA200, etc.
    # Returns = an EMA value and the name of the TA

    packet_reversed =  packet.iloc[::-1].copy()
    packet_reversed[f'ema{value}'] = ta.ema(close=packet_reversed['close'], length=value)
    packet[f'ema{value}'] = packet_reversed[f'ema{value}'].iloc[::-1].values

    df = packet[['timeframe',f'ema{value}']]

    return [f'ema{value}',df]