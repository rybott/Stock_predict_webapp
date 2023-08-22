import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os
# For News
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
# For Tweet_Sentiment
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import nest_asyncio
from transformers import pipeline


# Initialize Common Variables
start = datetime.today() - timedelta(days=4)
start_date = start.date()
today = datetime.today().strftime('%Y-%m-%d')
since1 = datetime.today() - timedelta(days=1)
since = since1.date()
load_dotenv()

def Stock_Graph(ticker,period):
  time = period
  ticker = yf.Ticker(ticker)
  history_stock = ticker.history(period=period)
  data = [{'date': date.strftime('%Y-%m-%d'), 'close': close
    } for date, close in zip(history_stock.index, history_stock.Close)]
  return data

def Stock_Price(ticker):
  #time.sleep(2)
  tick = yf.Ticker(ticker)
  data = tick.history(period="1d")
  close = round(float(list(data['Close'])[0]),3)
  return close

def News(ticker,n):
  url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
  fin_viz_req = Request(url=url, headers={'user-agent': 'app'})
  fin_viz_response = urlopen(fin_viz_req)
  html = soup(fin_viz_response,'html')
  news_tbl = html.find(id='news-table')
  rows = news_tbl.findAll('tr')
  headlines = []
  for index, row in enumerate(rows):
    try:
      title = row.a.text
      headlines.append([title])
    except:
      pass
  headlines = [item[0] for item in headlines if item]
  return headlines[:n]

nest_asyncio.apply()






  