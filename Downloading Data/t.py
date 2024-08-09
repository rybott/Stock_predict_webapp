# Finshed Stocks AAPL AMZN SPY
listof_stocks = ['AAPL']
listof_intervals = [1,5]
first_year = 2024
current_year = 2024
current_month = 8



url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={inter}min&month={yr}-{mth}&apikey={api_key}'
r = requests.get(url)
print(r)
key = f'Time Series ({inter}min)'
data = r.json().get(key, {})
df = pd.DataFrame.from_dict(data, orient='index')


df.index = pd.to_datetime(df.index)
df['Datetime'] = df.index.strftime('%Y-%m-%d %H:%M:%S.%f')
df['Interval'] = inter
df['Stock'] = ticker

df = df[["Datetime","1. open", "2. high", "3. low", "4. close", "5. volume", "Stock","Interval"]].copy()

print(df.info())
time.sleep(.5)

con.register('df', df)
con.execute(
    '''
    INSERT INTO Stocks
    SELECT 
        strptime(Datetime, '%Y-%m-%d %H:%M:%S.%f') as Datetime,
        "1. open" as open,
        "2. high" as high,
        "3. low" as low, 
        "4. close" as close, 
        "5. volume" as volume,
        Stock,
        Interval,
    FROM df
    WHERE Datetime NOT IN (SELECT Datetime FROM Stocks)
    ''')
print('inserted')
