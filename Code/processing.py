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
# Fundamental Data
import json
import requests

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

def News(ticker, n):
  url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
  fin_viz_req = Request(url=url, headers={'user-agent': 'app'})
  fin_viz_response = urlopen(fin_viz_req)
  html = soup(fin_viz_response,'html')
  news_tbl = html.find(id='news-table')
  rows = news_tbl.findAll('tr')
  headlines = []
  urls = []
  for index, row in enumerate(rows):
    try:
      title = row.a.text
      title1 = row.a['href']
      headlines.append([title])
      urls.append([title1])
    except:
      pass
  headlines = [item[0] for item in headlines if item]
  headlines = headlines[:n]
  urls = [item[0] for item in urls if item]
  urls = urls[:n]
  news = list(zip(urls, headlines))
  return news

def ratio_analysis(ticker):
  API_KEY = "S92QLGEMJK6MDSD1"

  def Overview(Ticker,API_KEY):
    Function = "OVERVIEW"
    url = f'https://www.alphavantage.co/query?function={Function}&symbol={Ticker}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    High52 = float(data['52WeekHigh'])
    Low52 = float(data['52WeekLow'])
    Mid52 = (High52 + Low52)/2
    DilutedEPS = float(data['DilutedEPSTTM'])
    QuarterlyEarningsGrowthYOY = float(data['QuarterlyEarningsGrowthYOY'])
    QuarterlyRevenueGrowthYOY = float(data['QuarterlyRevenueGrowthYOY'])
    AnalystTargetPrice = float(data['AnalystTargetPrice'])
    OverviewDict = {"High52":High52,"low52":Low52,"Mid52":Mid52,"DilutedEPS":DilutedEPS,"QuarterlyEarningsGrowthYOY":QuarterlyEarningsGrowthYOY,
                    "QuarterlyRevenueGrowthYOY":QuarterlyRevenueGrowthYOY,"AnalystTargetPrice":AnalystTargetPrice}
    return OverviewDict

  def Income(Ticker,API_KEY):
    Function = "INCOME_STATEMENT"
    url = f'https://www.alphavantage.co/query?function={Function}&symbol={Ticker}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    key_val = data["annualReports"]
    x = key_val[0]
    grossProfit = float(x['grossProfit'])
    totalRevenue = float(x['totalRevenue'])
    costofGoodsAndServicesSold = float(x['costofGoodsAndServicesSold'])
    costOfRevenue = float(x['costOfRevenue'])
    ebit = float(x['ebit'])
    netIncome = x['netIncome']
    Gross_Margin_COGS = (totalRevenue - costofGoodsAndServicesSold) / totalRevenue

    IncomeDict = {'ebit':ebit,'netIncome':netIncome, 'Gross_Margin_COGS':Gross_Margin_COGS}
    return IncomeDict

  def Balance(Ticker,API_KEY):
    Function = "BALANCE_SHEET"
    url = f'https://www.alphavantage.co/query?function={Function}&symbol={Ticker}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    key_val = data["annualReports"]
    key_val = key_val[0]
    totalAssets = float(key_val['totalAssets'])
    totalCurrentAssets = float(key_val['totalCurrentAssets'])
    cashAndCashEquivalents = float(key_val['cashAndCashEquivalentsAtCarryingValue'])+float(key_val['cashAndShortTermInvestments'])
    inventory = float(key_val['inventory'])
    currentNetReceivables = float(key_val['currentNetReceivables'])
    totalLiabilities = float(key_val['totalLiabilities'])
    totalCurrentLiabilities = float(key_val['totalCurrentLiabilities'])
    totalShareholderEquity = float(key_val['totalShareholderEquity'])
    commonStockSharesOutstanding = float(key_val['commonStockSharesOutstanding'])
    Current = totalCurrentAssets/totalCurrentLiabilities
    Quick = (cashAndCashEquivalents + currentNetReceivables)/totalCurrentAssets
    Debt_Equity = totalLiabilities / totalShareholderEquity
    Debt_Ratio = totalLiabilities / totalAssets
    BalanceDict = {"totalAssets":totalAssets,"totalShareholderEquity":totalShareholderEquity,"Current":Current,"Quick":Quick,
                  "Debt_Equity":Debt_Equity, "Debt_Ratio":Debt_Ratio}
    return BalanceDict

  O = Overview(ticker,API_KEY)
  I = Income(ticker,API_KEY)
  B = Balance(ticker,API_KEY)

  High52 = O['High52']
  low52 = O['low52']
  Mid52 = O['Mid52']
  DilutedEPS = O['DilutedEPS']
  QuarterlyRevGrowthYOY = O['QuarterlyRevenueGrowthYOY']
  AnalystTargetPrice = O['AnalystTargetPrice']
  ebit = I['ebit']
  netIncome = I['netIncome']
  Gross_Margin = I["Gross_Margin_COGS"]
  totalAssets = B['totalAssets']
  totalShareholderEquity = B['totalShareholderEquity'] 
  Current = B['Current'] 
  Quick = B['Quick'] 
  Debt_Equity = B['Debt_Equity'] 
  Debt_Ratio = B['Debt_Ratio'] 

  AnalysisDict = {"High52":High52 ,"low52":low52 ,"Mid52":Mid52 ,"DilutedEPS":DilutedEPS ,"QuarterlyRevGrowthYOY":QuarterlyRevGrowthYOY ,"AnalystTargetPrice":AnalystTargetPrice ,
                  "ebit":ebit ,"netIncome":netIncome ,"Gross_Margin":Gross_Margin ,"totalAssets":totalAssets ,"totalShareholderEquity":totalShareholderEquity ,"Current":Current ,
                  "Quick":Quick ,"Debt_Equity":Debt_Equity ,"Debt_Ratio":Debt_Ratio}

  return AnalysisDict