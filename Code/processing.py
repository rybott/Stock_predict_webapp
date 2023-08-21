import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
# For Graphs
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



TIK = 'TSLA'
start = datetime.today() - timedelta(days=4)
start_date = start.date()
today = datetime.today().strftime('%Y-%m-%d')

def Stock_Graph(ticker,period):
  time = period
  ticker = yf.Ticker(ticker)
  history_stock = ticker.history(period=period)
  fig, ax = plt.subplots()
  ax.plot(history_stock.index,history_stock.Close, linewidth=.85)
  ax.set_xticks([])
  ax.set_yticks([])
  ax.set_xticklabels([])
  ax.set_yticklabels([])
  ax.set_xlabel('')
  ax.set_ylabel('')
  ax.set_title('')
  