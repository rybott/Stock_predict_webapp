import os
from dotenv import load_dotenv
import pandas as pd
import duckdb as ddb
import requests
import datetime
import time
import pandas_ta as ta

from SQL.Querys import DBconn
#con = ddb.connect(r'C:\Design Folder\RBGithub\Trading_Algo_Data\testingalphaoptions.duckdb')
#db = DBconn(con)

date = '2024-07-08'

# Get Data--------------------------------------------------------------

load_dotenv()
api_key = os.getenv("Alpha_API")
symbol = 'AAPL'
interval = '1'
Stock_lookback_period = 100
Increasing_Mins = 2

#url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&month=2024-07&outputsize=full&apikey={api_key}"

stock_api = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}min&month=2024-07&entitlement=realtime&outputsize=full&apikey={api_key}'


r = requests.get(stock_api)
key = f'Time Series (1min)'
data = r.json().get(key, {})

df = pd.DataFrame.from_dict(data, orient='index')

df.index = pd.to_datetime(df.index)

stock_df = df
#stock_df = df.loc[date]

new_column_names = ['open', 'high', 'low', 'close', 'volume']
stock_df.columns = new_column_names


stock_df = stock_df.copy()
stock_df['timestamp'] = stock_df.index
stock_df.reset_index(drop=True,inplace=True)

stock_df['Trade'] = False
stock_df['close'] = pd.to_numeric(stock_df['close'])
stock_df['open'] = pd.to_numeric(stock_df['open'])
clean_stock_df = stock_df


# Analyze -----------------------------------------------------------------------

print(stock_df.info())




REC_df = clean_stock_df

Max_index = len(REC_df['timestamp'])-100

# Calculate Engulfing Candles
REC_df['WasRed'] = REC_df['close'].shift(-1) < REC_df['open'].shift(-1)
REC_df['Engulfing Candle'] = REC_df['WasRed'] & (REC_df['open'] < REC_df['close'].shift(-1)) & (REC_df['close'] > REC_df['open'].shift(-1))

REC_df_Reversed = REC_df.iloc[::-1].copy()
REC_df_Reversed['EMA100'] = ta.ema(close=REC_df_Reversed['close'], length=100)
REC_df['EMA100'] = REC_df_Reversed['EMA100'].iloc[::-1].values

REC_df['Found_EMA100'] = 0

Engulfing_df = REC_df[REC_df['Engulfing Candle']]


for index, row in Engulfing_df.iterrows():
    if index < Max_index:
        Engulfing_range = REC_df.iloc[index:index+100].copy()

        Engulfing_range_reversed = Engulfing_range.iloc[::-1].copy()
        Engulfing_range_reversed['EMA100'] = ta.ema(close=Engulfing_range_reversed['close'], length=100)
        Engulfing_range_reversed['EMA8'] = ta.ema(close=Engulfing_range_reversed['close'], length=8)

        Engulfing_range['EMA100'] = Engulfing_range_reversed['EMA100'].iloc[::-1].values
        Engulfing_range['EMA8'] = Engulfing_range_reversed['EMA8'].iloc[::-1].values

        REC_df['Found_EMA100'].update(Engulfing_range['EMA100'])

        if Engulfing_range['close'].iloc[0] > Engulfing_range['EMA100'].iloc[0]:
            REC_df.at[index, 'Trade'] = True

Tradable_df = REC_df[REC_df['Trade']]

print(Tradable_df.info())

# --------------------------------------------------------------------------------

import pandas as pd
import plotly.graph_objects as go

REC_df['adj_high'] = REC_df[['open', 'close']].max(axis=1)
REC_df['adj_low'] = REC_df[['open', 'close']].min(axis=1)

# Create the figure
fig = go.Figure()

# Add candle price trace
fig.add_trace(go.Candlestick(x=REC_df['timestamp'],
                             open=REC_df['open'],
                             high=REC_df['adj_high'],
                             low=REC_df['adj_low'],
                             close=REC_df['close'],
                             name='Candlesticks'))

# Add EMA100 trace
fig.add_trace(go.Scatter(x=REC_df['timestamp'], y=REC_df['EMA100'], mode='lines', name='EMA100'))

# Add trade signals trace
trade_points = REC_df[REC_df['Trade'] == True]
fig.add_trace(go.Scatter(x=trade_points['timestamp'], y=trade_points['close'], mode='markers', 
                         name='Trade Signal', marker=dict(color='red', size=10)))

# Update layout
fig.update_layout(
    title=f'Close Price, EMA8, and EMA100 over Time with Trade Signals {date}',
    xaxis_title='Timestamp',
    yaxis_title='Price',
    showlegend=True
)

# Show the plot
fig.show()








ddb.close()
