import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import nest_asyncio
from transformers import pipeline
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# This is what youll put your views code in if it works again one day
'''
Senti = Get_TW(stock,since)
session['TW_Sentiment'] = Senti[0]
session['TW_Score'] = Senti[1]

'''




nest_asyncio.apply()

since1 = datetime.today() - timedelta(days=1)
since = since1.date()
Date = []
Content = []
sentiment_pipeline = pipeline("sentiment-analysis", "distilbert-base-uncased-finetuned-sst-2-english")
TSV = []
Sentiment = []

stock = 'TSLA'
ticker = 'TSLA'
sin = since

def Get_TW(ticker, sin):
    
    async def add():
        api = API()
        await api.pool.add_account("rybott5000","Botkins1125!","rybott5000.5@gmail.com","SamGon1125!")
        await api.pool.add_account("bryan94790278","Botkins1125!","henrygon737@gmail.com","Botkins1125!")
        await api.pool.add_account("sam505059","Botkins1125!","Bottryan123@gmail.com","SamGon1125!")
        await api.pool.login_all()
    async def search(ticker_, sin_):
        api = API()
        q = f"${ticker_} lang:en since:{sin_}_17:00:00_EST min_faves:20"
        q = f"${ticker_} lang:en since:{sin_}_17:00:00_EST"
        async for tweet in api.search(q, limit=500):
            Content.append(tweet.rawContent)
    if __name__ == "__main__":
        #asyncio.run(add())
        asyncio.run(search(ticker,sin))
    tweets_df = pd.DataFrame({
                            'Content': Content})
    print(tweets_df.info())
    for tweet in tweets_df['Content']:
        tsv = sentiment_pipeline(tweet)
        tsvd = tsv[0]
        label = tsvd['label']
        score = tsvd['score']
        TSV.append(score)
        Sentiment.append(label)
        
    print("senti:",len(Sentiment)," tsv:",len(TSV))
    df = pd.DataFrame()
    df['TSV'] = TSV
    df['Sentiment'] = Sentiment
    df['multiplier'] = df['Sentiment'].apply(lambda x: 1 if x == 'POSITIVE' else -1)
    tw_combinedsentiment = (df['TSV'] * tweets_df['multiplier']).sum()
    tweet_direction = "Positive" if tw_combinedsentiment > 0 else "Negative"
    tweet_confidence = abs(tw_combinedsentiment)

    TW_Sentiment = tweet_direction
    TW_Score = tweet_confidence

    TW_List = [TW_Sentiment,TW_Score]
    return TW_List

stock = "GOOG"


Senti = Get_TW(stock,since)
sent = Senti[0]
scor = Senti[1]

print(sent,scor)